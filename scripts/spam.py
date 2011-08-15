#! /usr/bin/env python

from django.core.mail import EmailMultiAlternatives

def spam():
    subject, from_email, to =  'gen', 'noreply@iitm.ac.in', 'chetanbademi@gmail.com'
    text_content = 'This is an image message. http://www.shaastra.org/2011/media/main/img/all_logos.png'
    html_content = '<a href="www.google.com">Google!</a>This is an <img src = "http://www.shaastra.org/2011/media/main/img/all_logos.png>" message.'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])# sending plain text in case they cant view html
    msg.attach_alternative(html_content, "text/html")# the additional html content added to the content for ppl who can view html content
    msg.send()

spam()
