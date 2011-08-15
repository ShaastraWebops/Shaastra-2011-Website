from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template import Context, Template
import random, string

sender = "noreply@shaastra.org"
mail = open("/home/shaastra/mail.txt")
msg = Template(mail.read())
mail.close()
f = open("/home/shaastra/test.csv")
def insert(line):
    mailing_list = line 
    mailing_list.append("chetanbademi@gmail.com")
    subject ="Instructions for registration and questions on shaastra.org"
    send_mail(subject, content, sender, mailing_list)

for line in f:
    insert(line)

print "success"

