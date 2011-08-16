#! /usr/bin/env python

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def spam(line):
    subject = 'Registration and Questions(TDP) on the Shaastra 2011 site'
    from_email =  'noreply@iitm.ac.in'
    [dname, email_string] = line.split(',', 1)
    email_string = email_string.replace("\n", '')
    to  = email_string.split(',')
    to.append("chetanbademi@gmail.com")    
    content = open("/home/chetan/main_test/scripts/mail")
    html_content = ""
    for line in content:
        html_content = html_content + "<br/>" + line 
    text_content = strip_tags(html_content) # this strips the html, so people will have the text as well.
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)# sending plain text in case they cant view html
    msg.attach_alternative(html_content, "text/html")# the additional html content added to the content for ppl who can view html content
    msg.send()
    print "Sent mail to " , dname, to 


f = open("/home/chetan/main_test/scripts/test.csv")
for line in f:
    spam(line)
    print line

f.close()
    
