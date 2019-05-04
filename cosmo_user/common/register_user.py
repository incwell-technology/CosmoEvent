from cosmo_user import models as cosmo_models
from datetime import datetime
from django.contrib.auth.models import User
import yaml
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
def register_django_user(request):
    try:
        user = User.objects.create(username=request.POST['username'],
                                   email=request.POST['email'], first_name=request.POST['first_name'],
                                   last_name=request.POST['last_name'])
        user.set_password(request.POST['password'])
        user.save()
        verification_code = 2580

        update_details = {
        'recipient_email': request.POST['email'],
        'email_subject': 'Cosmo Event | Registration verification code.',
        'email_body': f"""
                Hi {request.POST['first_name']} {request.POST['last_name']}, You have registered in Cosmo Event. Your verification code is:
            <input type='text' value='{verification_code}' disabled/>
                Please copy and paste the verification code to the link: http://localhost:8000/home/verify

                Date Registered: {datetime.now()}
                Note: This verification code expires soon. Please verify soon.
                Thank You,
                Cosmo Event.
                Arun Thapa Chowk, Jhamsikhel,
                Nepal.
                5555987, 6584658
                """
        }
        if send_verification_email(update_details):
            return True
        else:
            user.delete()
            return False

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


def send_verification_email(update_details):
    credentials = yaml.load(open('credentials.yaml'), Loader=yaml.FullLoader)
    sender = credentials['cosmo_admin_email']
    password = credentials['cosmo_admin_password']
    recipient = update_details['recipient_email']
    msg = MIMEText(update_details['email_body'])
    msg['Subject'] = update_details['email_subject']
    msg['From'] = sender
    msg['To'] = recipient

    try:
        server = smtplib.SMTP_SSL(credentials['smtp_server'], credentials['smtp_port'])
        server.login(sender, password)
        server.sendmail(sender, [recipient], msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(e)
        return False
        