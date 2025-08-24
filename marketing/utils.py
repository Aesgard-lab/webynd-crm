import smtplib
from email.mime.text import MIMEText
from django.utils import timezone

from core.models import GymSettings
from clients.models import Client
from staff.models import Staff
from .models import CampaignRecipient


def send_email_with_smtp(gym, subject, html_content, to_email):
    """
    Envia un correo usando la configuración SMTP del gimnasio o su franquicia.
    """
    settings = gym.settings

    smtp_host = settings.get_value("smtp_host")
    smtp_port = settings.get_value("smtp_port") or 587
    smtp_user = settings.get_value("smtp_user")
    smtp_password = settings.get_value("smtp_password")

    if not smtp_host or not smtp_user or not smtp_password:
        raise Exception("SMTP no configurado correctamente")

    msg = MIMEText(html_content, "html")
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = to_email

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, [to_email], msg.as_string())
        return True
    except Exception as e:
        print(f"Error al enviar a {to_email}: {e}")
        return False


def execute_campaign(campaign):
    """
    Ejecuta una campaña: genera recipients y envía correos si es tipo email.
    """
    if campaign.sent:
        return

    for gym in campaign.target_gyms.all():
        recipients_qs = []

        if campaign.recipient_type in ["clients", "both"]:
            clients = Client.objects.filter(gym=gym)
            for client in clients:
                recipients_qs.append(CampaignRecipient(
                    campaign=campaign,
                    client=client
                ))

        if campaign.recipient_type in ["staff", "both"]:
            staff_members = Staff.objects.filter(gym=gym)
            for staff in staff_members:
                recipients_qs.append(CampaignRecipient(
                    campaign=campaign,
                    staff=staff
                ))

        # Guardamos en batch
        CampaignRecipient.objects.bulk_create(recipients_qs)

        if campaign.type == "email":
            for recipient in CampaignRecipient.objects.filter(campaign=campaign, status='pending'):
                email = recipient.client.email if recipient.client else recipient.staff.email
                success = send_email_with_smtp(
                    gym=gym,
                    subject=campaign.subject,
                    html_content=campaign.template.html_content,
                    to_email=email
                )

                recipient.status = "sent" if success else "failed"
                recipient.sent_at = timezone.now()
                recipient.save()

    campaign.sent = True
    campaign.save()


def send_notification_email(gym, template, subject, to_email):
    """
    Envía una notificación basada en una plantilla específica.
    """
    return send_email_with_smtp(
        gym=gym,
        subject=subject,
        html_content=template.html_content,
        to_email=to_email
    )
