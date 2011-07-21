#! /usr/bin/env python

from django.core.mail import EmailMultiAlternatives

def spam():
    subject, from_email, to = 'hello', 'hospitality@shaastra.org', 'sid24ss@gmail.com'
    text_content = 'This is a image message.'
    html_content = '<img src = "http://www.shaastra.org/2011/media/main/img/all_logos.png>"'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])# sending plain text in case they cant view html
    msg.attach_alternative(html_content, "text/html")# the additional html content added to the content for ppl who can view html content
    msg.send()
