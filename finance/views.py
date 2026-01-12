from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import require_gym_permission
from .models import TaxRate, PaymentMethod, FinanceSettings
from .forms import TaxRateForm, PaymentMethodForm, FinanceSettingsForm
from datetime import datetime, timedelta, date
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from sales.models import Order

@login_required
@require_gym_permission('finance.view_finance') 
def settings_view(request):
    gym = request.gym
    tax_rates = TaxRate.objects.filter(gym=gym)
    payment_methods = PaymentMethod.objects.filter(gym=gym)
    
    # Get or create finance settings
    finance_settings, created = FinanceSettings.objects.get_or_create(gym=gym)
    
    if request.method == 'POST' and 'save_settings' in request.POST:
        settings_form = FinanceSettingsForm(request.POST, instance=finance_settings)
        if settings_form.is_valid():
            s = settings_form.save(commit=False)
            
            # Validate Stripe Keys if present
            if s.stripe_public_key and s.stripe_secret_key:
                from .stripe_utils import validate_keys
                try:
                    validate_keys(s.stripe_public_key, s.stripe_secret_key)
                    messages.success(request, 'Configuración actualizada y conexión a Stripe correcta ✅')
                except Exception as e:
                    messages.warning(request, f'Configuración guardada, pero error en Stripe: {str(e)}')
            else:
                 messages.success(request, 'Configuración financiera actualizada.')
            
            s.save()
            return redirect('finance_settings')
    else:
        settings_form = FinanceSettingsForm(instance=finance_settings)
    
    context = {
        'title': 'Ajustes de Finanzas',
        'tax_rates': tax_rates,
        'payment_methods': payment_methods,
        'settings_form': settings_form,
    }
    return render(request, 'backoffice/finance/settings.html', context)

# --- Tax Rates ---

@login_required
@require_gym_permission('finance.change_taxrate')
def tax_create(request):
    gym = request.gym
    if request.method == 'POST':
        form = TaxRateForm(request.POST)
        if form.is_valid():
            tax = form.save(commit=False)
            tax.gym = gym
            tax.save()
            messages.success(request, 'Impuesto creado correctamente.')
            return redirect('finance_settings')
    else:
        form = TaxRateForm()
    
    return render(request, 'backoffice/finance/form.html', {
        'title': 'Nuevo Impuesto',
        'form': form,
        'back_url': 'finance_settings'
    })

@login_required
@require_gym_permission('finance.change_taxrate')
def tax_edit(request, pk):
    gym = request.gym
    tax = get_object_or_404(TaxRate, pk=pk, gym=gym)
    if request.method == 'POST':
        form = TaxRateForm(request.POST, instance=tax)
        if form.is_valid():
            form.save()
            messages.success(request, 'Impuesto actualizado correctamente.')
            return redirect('finance_settings')
    else:
        form = TaxRateForm(instance=tax)
    
    return render(request, 'backoffice/finance/form.html', {
        'title': f'Editar Impuesto: {tax.name}',
        'form': form,
        'back_url': 'finance_settings'
    })

@login_required
@require_gym_permission('finance.delete_taxrate')
def tax_delete(request, pk):
    gym = request.gym
    tax = get_object_or_404(TaxRate, pk=pk, gym=gym)
    if request.method == 'POST':
        tax.delete()
        messages.success(request, 'Impuesto eliminado.')
        return redirect('finance_settings')
    return render(request, 'backoffice/confirm_delete.html', {
        'title': 'Eliminar Impuesto',
        'object': tax,
        'back_url': 'finance_settings'
    })

# --- Payment Methods ---

@login_required
@require_gym_permission('finance.change_paymentmethod')
def method_create(request):
    gym = request.gym
    if request.method == 'POST':
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            pm = form.save(commit=False)
            pm.gym = gym
            pm.save()
            messages.success(request, 'Método de pago creado correctamente.')
            return redirect('finance_settings')
    else:
        form = PaymentMethodForm()
    
    return render(request, 'backoffice/finance/form.html', {
        'title': 'Nuevo Método de Pago',
        'form': form,
        'back_url': 'finance_settings'
    })

@login_required
@require_gym_permission('finance.change_paymentmethod')
def method_edit(request, pk):
    gym = request.gym
    pm = get_object_or_404(PaymentMethod, pk=pk, gym=gym)
    if request.method == 'POST':
        form = PaymentMethodForm(request.POST, instance=pm)
        if form.is_valid():
            form.save()
            messages.success(request, 'Método de pago actualizado.')
            return redirect('finance_settings')
    else:
        form = PaymentMethodForm(instance=pm)
    
    return render(request, 'backoffice/finance/form.html', {
        'title': f'Editar Método: {pm.name}',
        'form': form,
        'back_url': 'finance_settings'
    })

@login_required
@require_gym_permission('finance.delete_paymentmethod')
def method_delete(request, pk):
    gym = request.gym
    pm = get_object_or_404(PaymentMethod, pk=pk, gym=gym)
    if request.method == 'POST':
        pm.delete()
        messages.success(request, 'Método de pago eliminado.')
        return redirect('finance_settings')
    return render(request, 'backoffice/confirm_delete.html', {
        'title': 'Eliminar Método de Pago',
        'object': pm,
        'back_url': 'finance_settings'
    })

# --- Reports ---

@login_required
@require_gym_permission('finance.view_finance')
def billing_dashboard(request):
    gym = request.gym
    
    # 1. Date Filters
    date_range = request.GET.get('range', 'today') # today, yesterday, week, month, custom
    date_start_str = request.GET.get('start')
    date_end_str = request.GET.get('end')
    
    today = date.today()
    start_date = today
    end_date = today # Inclusive
    
    if date_range == 'yesterday':
        start_date = today - timedelta(days=1)
        end_date = start_date
    elif date_range == 'week':
        start_date = today - timedelta(days=7)
    elif date_range == 'month':
        start_date = today.replace(day=1)
    elif date_range == 'custom' and date_start_str:
        try:
            start_date = datetime.strptime(date_start_str, '%Y-%m-%d').date()
            if date_end_str:
                end_date = datetime.strptime(date_end_str, '%Y-%m-%d').date()
            else:
                end_date = start_date
        except ValueError:
            pass
            
    # Queryset
    # Filter by created_at range (inclusive)
    # created_at is DateTime, so we need (start 00:00, end 23:59)
    orders_qs = Order.objects.filter(
        gym=gym,
        created_at__date__gte=start_date,
        created_at__date__lte=end_date
    ).exclude(status='CANCELLED').select_related('client', 'created_by').prefetch_related('payments__payment_method')
    
    # 2. Aggregates (KPIs)
    # Use the base queryset for metrics
    aggregates = orders_qs.aggregate(
        total_income=Sum('total_amount'),
        total_tax=Sum('total_tax'),
        total_base=Sum('total_base'),
        count=Count('id')
    )
    
    # 3. Chart Data (Daily Trend)
    # Group by Date
    daily_data = orders_qs.annotate(day=TruncDate('created_at')).values('day').annotate(total=Sum('total_amount')).order_by('day')
    
    chart_labels = []
    chart_values = []
    
    # Fill gaps if needed, or just plot points
    for entry in daily_data:
        chart_labels.append(entry['day'].strftime('%d/%m'))
        chart_values.append(float(entry['total']))
        
    # 4. Filters (for dropdowns)
    payment_methods = PaymentMethod.objects.filter(gym=gym, is_active=True)
    
    # 5. Scheduled Payments (Cobros Futuros / Recurrentes)
    from clients.models import ClientMembership
    scheduled_payments = ClientMembership.objects.filter(
        client__gym=gym,
        is_recurring=True,
        # status__in=['ACTIVE', 'PENDING'] # Depending on definition
        status='ACTIVE'
    ).select_related('client').order_by('end_date')

    context = {
        'title': 'Informe de Facturación',
        'orders': orders_qs.order_by('-created_at'), # Pass explicit queryset
        'scheduled_payments': scheduled_payments,
        'metrics': {
            'total': aggregates['total_income'] or 0,
            'tax': aggregates['total_tax'] or 0,
            'base': aggregates['total_base'] or 0,
            'count': aggregates['count'] or 0
        },
        'chart': {
            'labels': chart_labels,
            'values': chart_values
        },
        'filters': {
            'range': date_range,
            'start': start_date.strftime('%Y-%m-%d'),
            'end': end_date.strftime('%Y-%m-%d'),
            'methods': payment_methods
        },
        'debug_start': start_date,
        'debug_end': end_date
    }
    
    return render(request, 'backoffice/finance/billing_dashboard.html', context)
