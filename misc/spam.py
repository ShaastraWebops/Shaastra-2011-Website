#! /usr/bin/env python

from django.core.mail import EmailMultiAlternatives
from email.MIMEImage import MIMEImage
from django.core.mail import EmailMessage

def email_embed_image(email, img_content_id, img_data):
    """
    email is a django.core.mail.EmailMessage object
    """
    img = MIMEImage(img_data)
    img.add_header('Content-ID', '<%s>' % img_content_id)
    img.add_header('Content-Disposition', 'inline')
    email.attach(img)
    
def spam():
    subject, from_email, to = 'Shaastra 2013 invitation', 'hospitality@shaastra.org', 'swaroop551992@gmail.com'
    #text_content = 'Please find attached the Shaastra 2011 invitation'
    html_content = '<img src = "http://www.shaastra.org/2011/media/main/img/all_logos.png>"'
    #msg = EmailMultiAlternatives(subject, text_content, from_email, [to])# sending plain text in case they cant view html
    #msg.attach_alternative(html_content, "text/html")# the additional html content added to the content for ppl who can view html content
    #send_html_mail(subject,html_content,from_email,[to])
    img_data = open('/var/www/invite.jpg', 'rb').read()
    img_content_id = 'noname'
    body = '<img src="cid:%s" />' % img_content_id
    msg = EmailMessage('tite4', body, 'hospitality@shaastra.org', ['swaroop551992@gmail.com'], headers = {'Content-ID': img_content_id,'Content-Disposition' : 'inline'})
    msg.mixed_subtype = 'relative'

    #msg.mixed_subtype = 'multipart/related'
    img = MIMEImage(img_data)
    img.add_header('Content-ID', '<%s>' % img_content_id)
    img.add_header('Content-Disposition', 'inline')

    msg.attach(img)
    msg.send()
    
def spam2():
    subject, from_email= 'Shaastra 2011 invitation', 'hospitality@shaastra.org'
    f = open('./data.csv','rw')
    text_content = '[image: invite.jpg]'
    html_content = '<img title="invite.jpg" alt="invite.jpg" src="http://www.shaastra.org/2011/media/main/img/invite.jpg">'
    for line in f:
        to = line.rstrip()
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])# sending plain text in case they cant view html
        msg.attach_alternative(html_content, "text/html")# the additional html content added to the content for ppl who can view html content
        try:
            msg.send()
            print "Mail sent to " + to
            f.write('/')
        except:
            print "Mail not sent to " + to        
    

