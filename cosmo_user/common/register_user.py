from cosmo_user import models as cosmo_models
from datetime import datetime
from django.contrib.auth.models import User
import yaml
import smtplib
from email.mime.text import MIMEText

def register_django_user(request):
    try:
        user = User.objects.create(username=request.POST['username'],
                                   email=request.POST['email'], first_name=request.POST['first_name'],
                                   last_name=request.POST['last_name'])
        user.set_password(request.POST['password'])
        user.save()
        # send_verification_email(request)
        return True

    except Exception as e:
        print(e)
        return False

def register_cosmo_user(user, phone):
        try:
            cosmo_models.CosmoUser.objects.create(user=user, primaryPhone=phone, votingCount=25,verified=False,token=2580,expiry=datetime.now())
            return True
        except Exception as e:
            print(e)
            return False


def send_verification_email(request):
    credentials = yaml.load(open('credentials.yaml'))
    sender = credentials['cosmo_admin_email']
    password = credentials['cosmo_admin_password']
    recipient = request.POST['email']
    verification_code = 2580
    # Create message
    email_body = f"""
            Hello {request.POST['first_name']} {request.POST['last_name']},

            You have registered in Cosmo Event. Your verification code is:
            <input type='text' value='{verification_code}' disabled/>

            Please copy and paste the verification code to the link: http://localhost:8000/home/verify

            Note: This verification code expires soon. Please verify soon.
            Thank You,
            Cosmo Event.
            Arun Thapa Chowk, Jhamsikhel,
            Nepal.
            5555987, 6584658
            
    """
    msg = MIMEText(email_body)
    msg['Subject'] = "Cosmo Event: Email Verification"
    msg['From'] = sender
    msg['To'] = recipient

    try:
        # Create server object with SSL option
        server = smtplib.SMTP_SSL(credentials['smtp_server'], credentials['smtp_port'])
        # Perform operations via server
        server.login(sender, password)
        server.sendmail(sender, [recipient], msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(e)
        return False