import smtplib, random, logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)

def smtp_generate_code():
    return ''.join(random.choices('0123456789', k=6))

def smtp_register_validation(user, validation_code):
    message: MIMEMultipart = MIMEMultipart()
    message['From'] = "fttranscendence.ft42@gmail.com"
    logger.debug(f"Sending validation code to user {user.username} {user.email}")
    message['To'] = user.email
    message['Subject'] = 'fttranscendence.ft42 - Validation code'

    body = f"""
    <h1>Welcome { user.username }</h1>
    <h2>Last step before you can start playing</h2>
    <p>Here's your validation code is: { validation_code }</p>
    """

    message.attach(MIMEText(body, 'html'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("fttranscendence.ft42@gmail.com", "tfdmlyvubuxsnbeg")
    server.sendmail("fttranscendence.ft42@gmail.com", user.email, message.as_string())
    server.quit()