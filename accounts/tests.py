from django.test import TestCase

from django.core.mail import EmailMessage
# Create your tests here.

def sendEmail():
    to_email = 'mingtyut@gmail.com'
    email = EmailMessage(
                "ACE TEST", "test", to=[to_email]
    )
    email.send()

sendEmail()