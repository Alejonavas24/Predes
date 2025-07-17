
import smtplib

SMTP_HOST = 'smtp.sendgrid.net'
SMTP_PORT = 587
SMTP_USER = 'apikey'
SMTP_PASS = 'SENDGRID_API_KEY'
FROM_EMAIL = 'tuki@tuki.com'
TO_EMAIL   = 'tuki@tuki.com'



def notify_if_needed(node_id, ts, alerts):
     message = f"Alerta desde {node_id} a {ts}: {', '.join(alerts)} fuera de rango."
     server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
     server.starttls()
     server.login(SMTP_USER, SMTP_PASS)
     server.sendmail(FROM_EMAIL, TO_EMAIL, f"Subject:Alerta Incendio\n\n{message}")
     server.quit()
     print(f"[ALERTA] Enviado SMS y correo: {message}")