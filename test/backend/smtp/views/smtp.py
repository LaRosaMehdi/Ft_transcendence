import smtplib, random, logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)

def smtp_setting_validation(user, new_password):
    message: MIMEMultipart = MIMEMultipart()
    message['From'] = "fttranscendence.ft42@gmail.com"
    logger.debug(f"Sending validation code to user {user.username} {user.email}")
    message['To'] = user.email
    message['Subject'] = 'fttranscendence.ft42 - Reset password'

    body = f"""
    <h1>Hello { user.username }</h1>
    <h2>Just need to validate this step to confirm password change</h2>
    <p>Here's your validation code is: { new_password }</p>
    """

    message.attach(MIMEText(body, 'html'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("fttranscendence.ft42@gmail.com", "tfdmlyvubuxsnbeg")
    server.sendmail("fttranscendence.ft42@gmail.com", user.email, message.as_string())
    server.quit()

def smtp_aouth_validation(user, validation_code):
    message: MIMEMultipart = MIMEMultipart()
    message['From'] = "fttranscendence.ft42@gmail.com"
    logger.debug(f"Sending validation code to user {user.username} {user.email}")
    message['To'] = user.email
    message['Subject'] = 'fttranscendence.ft42 - Connexion validation'

    body = f"""
    <h1>Hello { user.username }</h1>
    <h2>Last step before you can start playing</h2>
    <p>Here's your validation code is: { validation_code }</p>
    """

    message.attach(MIMEText(body, 'html'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("fttranscendence.ft42@gmail.com", "tfdmlyvubuxsnbeg")
    server.sendmail("fttranscendence.ft42@gmail.com", user.email, message.as_string())
    server.quit()