#! /usr/bin/env python

from django.core.mail import EmailMultiAlternatives
from email.MIMEImage import MIMEImage
from django.core.mail import EmailMessage
from django.template import Template,Context
from main_test.users.models import Team
from django.contrib.auth.models import User, Group
import ho.pisa as pisa
import os

SPAM_ROOT = "/home/sudharshan/Shaastra/main_test/templates/saars/"
SAAR_TEMPLATE = "/home/sudharshan/Shaastra/main_test/templates/saars/"
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
            #msg.send()
            print "Mail sent to " + to
            f.write('/')
        except:
            print "Mail not sent to " + to        
    
def superspam(team_name="BLAH",eventname=""):
    subject = "Shaastra 2011 Accommodation"
    text = """
    Greetings from the Hospitality team of Shaastra.

This email is regarding your team's stay at IIT-Madras during Shaastra-2011.

Please find attached a SAAR (Shaastra Advanced Accommodation Registration) document (pdf) along with this email.

Fill in your arrival and departure details in this google form (It is enough if one member of a team fills up the form):
https://docs.google.com/spreadsheet/viewform?formkey=dERlZkMzZU9OZzlZYXlYaGxsWjhUVFE6MQ
(If you cannot click the link, please copy and paste it into the address bar)

Please take a print out of the attached file and fill in the relevant details when coming to Shaastra-2011.

You are expected to abide by the rules and regulations as stated in the SAAR document.

Please read the instructions given in the document carefully.


------------------------------
Thanks and Regards,
The Hospitality Team,
Shaastra-2011.

-------------------------------------------
(For any queries contact hospitality@shaastra.org)

Shaastra-2011 website : http://www.shaastra.org/2011/main/home/
"""
    success = False
    try:
        print eventname
        team_object=Team.objects.get(name = team_name,event__name=eventname)
        print "Got team"
        users_list=team_object.members.all()
        print "got user list"
        print users_list
        saar_id="SHA11T"+str(team_object.id)
        team_leader = team_object.leader.username
        team_size = users_list.count()
        for user in users_list:
            user_profile = user.get_profile()
            college,phone_number,gender = user_profile.college.name,user_profile.mobile_number,user_profile.gender
            mail = EmailMessage(subject,text,"shaastra@iitm.ac.in",[user.email],['psbbboyz@gmail.com'],headers={"Reply-To":"hospitality@shaastra.org"})
            rawhtml = open(SAAR_TEMPLATE+"prefinal.html","r")
            t = Template(rawhtml.read())
            c = Context(locals())
            f = open(SPAM_ROOT+saar_id + "_"+ str(user.id)+"saar.html" , "w")
            f.write(t.render(c).encode('utf-8'))
            os.system("xhtml2pdf " + SAAR_TEMPLATE + saar_id+ "_"+str(user.id)+ "saar.html")
            saarpdf_data = open(SPAM_ROOT+saar_id +"_"+ str(user.id)+ "saar.pdf","rb")
            mail.attach_file(SPAM_ROOT+saar_id +"_"+ str(user.id)+"saar.pdf")
            print " gonna send"
	    try:
                mail.send()
                success = True
            except:
                success = False
    except:
        print "fail"            
    return success
              
def indspam(email_id = "BLAH"):                
    subject = "Shaastra 2011 Accommodation"
    text = """
    Greetings from the Hospitality team of Shaastra.

This email is regarding your stay at IIT-Madras during Shaastra-2011.

Please find attached a SAAR (Shaastra Advanced Accommodation Registration) document (pdf) along with this email.

Fill in your arrival and departure details in this google form:
https://docs.google.com/spreadsheet/viewform?formkey=dERlZkMzZU9OZzlZYXlYaGxsWjhUVFE6MQ
(If you cannot click the link, please copy and paste it into the address bar)

Please take a print out of the attached file and fill in the relevant details when coming to Shaastra-2011.

You are expected to abide by the rules and regulations as stated in the SAAR document.

 Please read the instructions given in the document carefully.


------------------------------
Thanks and Regards,
The Hospitality Team,
Shaastra-2011.

-------------------------------------------
(For any queries contact hospitality@shaastra.org)

Shaastra-2011 website : http://www.shaastra.org/2011/main/home/
"""
    success = False
    try:
        print email_id
        user_object=User.objects.get(email=email_id)
        print user_object 
        user_object_profile = user_object.get_profile()
        print "hi2"
        try:
            gender,first_name,last_name,college,phone_number= user_object_profile.gender,user_object.first_name,user_object.last_name,user_object_profile.college.name,user_object_profile.mobile_number
        except:
            print "failed"
        print "hi6"        
        saar_id = "SHA11U"+str(user_object.id)
        print "hi5"
        mail = EmailMessage(subject,text,"shaastra@iitm.ac.in",[user_object.email])
        print "hi3"
        try:
	  print SAAR_TEMPLATE+"indprefinal.html"
	  rawhtml = open(SAAR_TEMPLATE+"indprefinal.html","r")
        except:
	  raise
	print "check"
	t = Template(rawhtml.read())
        c = Context(locals())
        f = open(SPAM_ROOT+saar_id + "saar.html" , "w")
        f.write(t.render(c).encode('utf-8'))
        os.system("xhtml2pdf " +SPAM_ROOT+ saar_id +"saar.html")
        saarpdf_data = open(SPAM_ROOT+saar_id +"saar.pdf","rb")
        mail.attach_file(SPAM_ROOT+saar_id+"saar.pdf")
        print "hifin"
        try:
            mail.send()
            success = True
            print "WIN"
        except:
            success = False
    except:
	print email_id      
    return success             
        
def hospispamind():
    teamfile=open(SAAR_TEMPLATE+"list_1.csv","r")
    teamfileresults = open(SAAR_TEMPLATE+"cfrwsuccess.csv","w")
    for line in teamfile:
        data = line.rstrip()
        print data
        datalist = data.split(",")
        print datalist
        teamname = datalist[0]
        eventname = datalist[1]
        teamfileresults.write(data)
        teamfileresults.write(" --> ")
        teamfileresults.write(str(superspam(teamname,eventname)))
        teamfileresults.write('\n')
    teamfile.close()
    teamfileresults.close()
    indfile = open("/home/swaroop/teamlist.csv","r")
    indfileresults = open("/home/swaroop/indlistsuccess.csv","w")
    indfile = open(SAAR_TEMPLATE+"indlist.csv","r")
    indfileresults = open(SAAR_TEMPLATE+"indlistsuccess.csv","w")
    for line in indfile:
        data = line.rstrip()
        indfileresults.write(data)
        indfileresults.write(" --> ")
        indfileresults.write(str(indspam(data)))
        indfileresults.write('\n')
        
def getdata():
    f = open("/home/swaroop/success/list_1.csv","r")
    g = open("/home/swaroop/success/list_data.csv","w")
    for line in f:
        dataline = line.rstrip().split(",")
        print dataline
        teamname = dataline[1]
        eventname = dataline[0]
        try:
            teamobject = Team.objects.get(name = teamname, event__name = eventname)
            print "0"
            userlist = teamobject.members.all()
            print "1"
            g.write(eventname +"    " + teamname + "\n")
            for user in userlist:
                userprof = user.get_profile()
                g.write(str(user.id) + "," + user.email + "," + str(userprof.mobile_number) + "," + user.first_name + "," + user.last_name )
                g.write("\n")
        except:
            print "fail"
    f.close()
    g.close()
    
def getidata():
    f = open("/home/swaroop/success/indlistsuccess.csv","r")
    g = open("/home/swaroop/success/ind_list_data.csv","w")
    for line in f:
        emailid = line.rstrip()
        try:
            user = User.objects.get(email = emailid)
            userprof = user.get_profile()
            g.write(str(user.id) + "," + user.email + "," + str(userprof.mobile_number) + "," + user.first_name + "," + user.last_name )
            g.write("\n")
        except:
            print "fail"
    f.close()
    g.close()
