#! /usr/bin/env python

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def spam(line):
    subject = 'Registration and Questions on the Shaastra 2011 site'
    from_email =  'noreply@iitm.ac.in'
    [dname, email_string] = line.split(',', 1)
    email_string = email_string.replace("\n", '')
    to  = email_string.split(',')
    to.append("chetanbademi@gmail.com")    
    print to
    html_content = """Dear coords,
    A couple of new features are up on the shaastra site. You will be able to open the registration and add a questionnaire to your event.
    1. Registration
        - To enable registration, go to your dashboard and click on "Edit Event Details.
        - Check the "registrable" option. 
        - Save the event details. 
        - Check <a href = "">this</a> for more detais. 
        - Once you've done this, a register button will appear when users login. 
        - You can also view the users who have registered by clicking on the "Show registered users" button.
    
    2. 
        " """

    text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.
    print html_content
    print text_content
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)# sending plain text in case they cant view html
    msg.attach_alternative(html_content, "text/html")# the additional html content added to the content for ppl who can view html content
    msg.send()
    print "Sent mail to %s", dname


f = open("/home/chetan/main_test/scripts/test.csv")
for line in f:
    spam(line)
    print line

f.close()
    
