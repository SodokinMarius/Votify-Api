
from django.core.mail import send_mail

def send_email_to(subject:str,message:str,recipients:list,):
    send_mail(
            subject=subject,
            message=message,
            from_email= "yaomariussodokin@gmail.com",
            recipient_list=recipients,
            fail_silently=False,
                )