from misc.util import camelize
from main_test.events.models import Event
from main_test.settings import SITE_URL
from django.contrib.auth.models import User
from main_test.users.models import UserProfile, College
from django.core.mail import send_mail
from django.template import Context, Template
import random, string
import sys
sys.path.remove("/home/shaastra/django-projects")
sys.path.append("/home/shaastra/django-projects/test/")
print sys.path
sender = "noreply@shaastra.org"
mail = open("/home/shaastra/mail.txt")
msg = Template(mail.read())
mail.close()
f = open("/home/shaastra/test.csv")
N = 6
c = College.objects.get(name='testcollege')
def insert(line):
    [dname, email] = line.split(',', 1)
    name = dname.replace('&', '').replace('!', '').replace('\'', '').replace('-', '').replace('  ', ' ')
    username = camelize(name).lower()
    password = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(N))
    url = SITE_URL + "events/" + username + "/"
    e = Event(name = name, display_name = dname, url = url)
    e.save()
    email = email.replace("\n", '')
    u = User.objects.create_user(username = username, email = email, password = password)
    u.save()
    UserProfile(user = u, is_coord = True, coord_event = e, college = c).save()              #All coords are implicitly female :P
    content = msg.render(Context({"username":username,"password":password}))
    subject = name + ": Your shaastra.org access data"
    send_mail(subject, content, sender, [email,])

for line in f:
    insert(line)

print "success"

