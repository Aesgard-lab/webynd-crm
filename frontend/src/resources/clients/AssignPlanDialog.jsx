// frontend/src/resources/clients/AssignPlanDialog.jsx
import * as React from 'react';
import { useDataProvider, useNotify } from 'react-admin';
import {
  Box,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  MenuItem,
  Select,
  FormControl,
  InputLabel,
  RadioGroup,
  FormControlLabel,
  Radio,
  TextField as MuiTextField,
} from '@mui/material';
import { getActiveGymId, formatCurrency } from './helpers';

export const AssignPlanDialog = ({ open, onClose, client, onAssigned }) => {
  const dataProvider = useDataProvider();
  const notify = useNotify();

  const [planType, setPlanType] = React.useState('subscription'); // 'subscription' | 'bonus'
  const [plans, setPlans] = React.useState([]);
  const [plansLoading, setPlansLoading] = React.useState(false);
  const [plansError, setPlansError] = React.useState(null);

  const [planId, setPlanId] = React.useState('');
  const [startDate, setStartDate] = React.useState(() => {
    const today = new Date();
    return today.toISOString().slice(0, 10);
  });
  const [quantity, setQuantity] = React.useState(1);

  const [discountType, setDiscountType] = React.useState('none'); // 'none' | 'percent' | 'amount'
  const [discountValue, setDiscountValue] = React.useState('');

  const [paymentMethod, setPaymentMethod] = React.useState('cash'); // 'cash' | 'card_terminal' | 'saved_card' | 'other'
  const [chargeTiming, setChargeTiming] = React.useState('now');    // 'now' | 'on_start_date' | 'none'

  const [submitting, setSubmitting] = React.useState(false);

  const gymId = getActiveGymId();

  // Reset básico al abrir
  React.useEffect(() => {
    if (open) {
      const today = new Date();
      setPlanType('subscription');
      setPlanId('');
      setQuantity(1);
      setStartDate(today.toISOString().slice(0, 10));
      setDiscountType('none');
      setDiscountValue('');
      setPaymentMethod('cash');
      setChargeTiming('now');
    }
  }, [open]);

  // Cargar planes según tipo
  React.useEffect(() => {
    if (!open) return;
    let active = true;

    const load = async () => {
      setPlansLoading(true);
      setPlansError(null);
      setPlans([]);
      setPlanId('');

      const resource =
        planType === 'subscription'
          ? 'plans/subscription-plans'
          : 'plans/bonus-plans';

      try {
        const { data } = await dataProvider.getList(resource, {
          filter: gymId ? { gym: gymId } : {},
          pagination: { page: 1, perPage: 100 },
          sort: { field: 'name', order: 'ASC' },
        });
        if (!active) return;
        setPlans(data || []);
      } catch (error) {
        if (!active) return;
        setPlansError(error);
      } finally {
        if (active) setPlansLoading(false);
      }
    };

    load();

    return () => {
      active = false;
    };
  }, [open, planType, dataProvider, gymId]);

  const selectedPlan = React.useMemo(
    () => plans.find((p) => String(p.id) === String(planId)),
    [plans, planId],
  );

  const pricing = React.useMemo(() => {
    if (!selectedPlan) {
      return {
        base: 0,
        discountAmount: 0,
        netAfterDiscount: 0,
        iva: 0,
        total: 0,
        taxPercentage: 0,
      };
    }

    const basePrice = Number(selectedPlan.price || 0); // asumimos neto sin IVA
    const taxPercentage =
      selectedPlan.tax_percentage != null
        ? Number(selectedPlan.tax_percentage)
        : 21;

    let discountAmount = 0;
    const rawDiscount = Number(discountValue || 0);

    if (discountType === 'percent') {
      discountAmount = (basePrice * rawDiscount) / 100;
    } else if (discountType === 'amount') {
      discountAmount = rawDiscount;
    }

    if (discountAmount < 0) discountAmount = 0;
    if (discountAmount > basePrice) discountAmount = basePrice;

    const netAfterDiscount = basePrice - discountAmount;
    const iva = (netAfterDiscount * taxPercentage) / 100;
    const total = netAfterDiscount + iva;

    return {
      base: basePrice,
      discountAmount,
      netAfterDiscount,
      iva,
      total,
      taxPercentage,
    };
  }, [selectedPlan, discountType, discountValue]);

  const handleSubmit = async () => {
    if (!client?.id || !planId) {
      notify('Selecciona un plan antes de guardar', { type: 'warning' });
      return;
    }

    setSubmitting(true);

    const payload = {
      client_id: client.id,
      item_type: planType,
      plan_id: Number(planId),
      payment_method: paymentMethod,
      charge_timing: chargeTiming,
      discount_type: discountType,
      invoice_option: 'none',
    };

    if (gymId) payload.gym_id = Number(gymId);
    if (startDate) payload.start_date = startDate;
    if (planType === 'bonus') payload.bonus_quantity = quantity || 1;

    if (discountType !== 'none') {
      const parsed = Number(discountValue);
      payload.discount_value = Number.isNaN(parsed) ? 0 : parsed;
    }

    try {
      await dataProvider.create('billing/purchase', { data: payload });

      notify(
        planType === 'subscription'
          ? 'Suscripción asignada y compra registrada'
          : 'Bono asignado y compra registrada',
        { type: 'success' },
      );

      if (onAssigned) onAssigned();
      onClose();
    } catch (error) {
      console.error('Error en billing/purchase:', error);

      // Si el servidor ha respondido 201 pero el front falla al parsear el JSON,
      // normalmente el error es un SyntaxError: en ese caso tratamos la compra como hecha.
      if (error && error.name === 'SyntaxError') {
        notify(
          'Compra registrada, pero ha habido un pequeño error de parseo en el front.',
          { type: 'warning' },
        );
        if (onAssigned) onAssigned();
        onClose();
      } else {
        notify('No se ha podido completar la compra. Revisa la API.', {
          type: 'error',
        });
      }
    } finally {
      setSubmitting(false);
    }
  };

  const handleClose = () => {
    if (submitting) return;
    onClose();
  };

  const chargeLabel = React.useMemo(() => {
    if (!selectedPlan) return '';
    const totalTxt = formatCurrency(pricing.total);
    if (chargeTiming === 'now') {
      return `Se cobrará ahora: ${totalTxt}.`;
    }
    if (chargeTiming === 'on_start_date') {
      return `Se programará el cobro de ${totalTxt} para la fecha de inicio.`;
    }
    return `No se cobrará ahora. Se registrará solo el plan por un total de ${totalTxt}.`;
  }, [chargeTiming, selectedPlan, pricing.total]);

  return (
    <Dialog open={open} onClose={handleClose} fullWidth maxWidth="sm">
      <DialogTitle>Asignar plan al cliente</DialogTitle>
      <DialogContent dividers>
        {/* Tipo de plan */}
        <Box sx={{ mb: 2 }}>
          <RadioGroup
            row
            value={planType}
            onChange={(e) => setPlanType(e.target.value)}
          >
            <FormControlLabel
              value="subscription"
              control={<Radio />}
              label="Suscripción"
            />
            <FormControlLabel value="bonus" control={<Radio />} label="Bono" />
          </RadioGroup>
        </Box>

        {/* Plan */}
        <Box sx={{ mb: 2 }}>
          <FormControl fullWidth size="small">
            <InputLabel id="plan-select-label">Plan</InputLabel>
            <Select
              labelId="plan-select-label"
              label="Plan"
              value={planId}
              onChange={(e) => setPlanId(e.target.value)}
              disabled={plansLoading || !!plansError}
            >
              {plans.map((p) => {
                const basePrice = Number(p.price || 0);
                const labelName = p.name || p.label || `Plan #${p.id}`;
                const labelPrice =
                  basePrice && !Number.isNaN(basePrice)
                    ? ` · ${formatCurrency(basePrice)}`
                    : '';
                return (
                  <MenuItem key={p.id} value={p.id}>
                    {labelName}
                    {labelPrice}
                  </MenuItem>
                );
              })}
            </Select>
          </FormControl>
          {plansLoading && (
            <p className="mt-1 text-xs text-gray-500">Cargando planes…</p>
          )}
          {plansError && (
            <p className="mt-1 text-xs text-red-500">
              No se han podido cargar los planes (revisa el recurso de API para
              planes).
            </p>
          )}
        </Box>

        {/* Fecha inicio */}
        <Box sx={{ mb: 2 }}>
          <MuiTextField
            label="Fecha de inicio"
            type="date"
            size="small"
            fullWidth
            InputLabelProps={{ shrink: true }}
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
          />
        </Box>

        {/* Cantidad de bono */}
        {planType === 'bonus' && (
          <Box sx={{ mb: 2 }}>
            <MuiTextField
              label="Cantidad de usos del bono"
              type="number"
              size="small"
              fullWidth
              inputProps={{ min: 1 }}
              value={quantity}
              onChange={(e) =>
                setQuantity(Math.max(1, Number(e.target.value) || 1))
              }
            />
          </Box>
        )}

        {/* Descuento */}
        <Box sx={{ mb: 2 }}>
          <FormControl fullWidth size="small">
            <InputLabel id="discount-type-label">Descuento</InputLabel>
            <Select
              labelId="discount-type-label"
              label="Descuento"
              value={discountType}
              onChange={(e) => {
                setDiscountType(e.target.value);
                setDiscountValue('');
              }}
            >
              <MenuItem value="none">Sin descuento</MenuItem>
              <MenuItem value="percent">% Porcentaje</MenuItem>
              <MenuItem value="amount">€ Importe</MenuItem>
            </Select>
          </FormControl>

          {discountType !== 'none' && (
            <Box sx={{ mt: 1 }}>
              <MuiTextField
                label={discountType === 'percent' ? '% descuento' : '€ descuento'}
                type="number"
                size="small"
                fullWidth
                value={discountValue}
                onChange={(e) => setDiscountValue(e.target.value)}
              />
            </Box>
          )}
        </Box>

        {/* Método de pago */}
        <Box sx={{ mb: 2 }}>
          <FormControl fullWidth size="small">
            <InputLabel id="payment-method-label">Método de pago</InputLabel>
            <Select
              labelId="payment-method-label"
              label="Método de pago"
              value={paymentMethod}
              onChange={(e) => setPaymentMethod(e.target.value)}
            >
              <MenuItem value="cash">Efectivo</MenuItem>
              <MenuItem value="card_terminal">Tarjeta (TPV)</MenuItem>
              <MenuItem value="saved_card">Tarjeta vinculada</MenuItem>
              <MenuItem value="other">Otro</MenuItem>
            </Select>
          </FormControl>
        </Box>

        {/* Momento de cobro */}
        <Box sx={{ mb: 2 }}>
          <RadioGroup
            row
            value={chargeTiming}
            onChange={(e) => setChargeTiming(e.target.value)}
          >
            <FormControlLabel
              value="now"
              control={<Radio />}
              label="Cobrar ahora"
            />
            <FormControlLabel
              value="on_start_date"
              control={<Radio />}
              label="Cobrar en fecha de inicio"
            />
            <FormControlLabel
              value="none"
              control={<Radio />}
              label="No cobrar ahora (solo plan)"
            />
          </RadioGroup>
        </Box>

        {/* Resumen económico */}
        {selectedPlan ? (
          <Box
            sx={{
              mt: 1,
              p: 1.5,
              borderRadius: 2,
              bgcolor: '#f3f4f6',
              fontSize: '0.8rem',
            }}
          >
            <div className="flex justify-between">
              <span>Precio base</span>
              <span>{formatCurrency(pricing.base)}</span>
            </div>
            {pricing.discountAmount > 0 && (
              <div className="flex justify-between text-red-600">
                <span>Descuento</span>
                <span>-{formatCurrency(pricing.discountAmount)}</span>
              </div>
            )}
            <div className="flex justify-between">
              <span>Base imponible</span>
              <span>{formatCurrency(pricing.netAfterDiscount)}</span>
            </div>
            <div className="flex justify-between">
              <span>IVA ({pricing.taxPercentage}%)</span>
              <span>{formatCurrency(pricing.iva)}</span>
            </div>
            <div className="mt-1 flex justify-between font-semibold">
              <span>Total</span>
              <span>{formatCurrency(pricing.total)}</span>
            </div>

            {chargeLabel && (
              <p className="mt-1 text-[11px] text-gray-600">{chargeLabel}</p>
            )}
          </Box>
        ) : (
          <p className="mt-2 text-[11px] text-gray-500">
            Selecciona un plan para ver el precio final.
          </p>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={handleClose} disabled={submitting}>
          Cancelar
        </Button>
        <Button
          onClick={handleSubmit}
          variant="contained"
          disabled={submitting}
        >
          {submitting ? 'Guardando…' : 'Confirmar compra'}
        </Button>
      </DialogActions>
    </Dialog>
  );
};
