from main_test.misc.util import camelize
from main_test.events.models import Event
from main_test.settings import SITE_URL
from django.contrib.auth.models import User
from main_test.users.models import UserProfile, College
from django.core.mail import send_mail
from django.template import Context, Template
import random, string

sender = "noreply@shaastra.org"
mail = open("/home/shaastra/mail.txt")
msg = Template(mail.read())
mail.close()
f = open("/home/shaastra/test.csv")
N = 6
def insert(line):
    [dname, email_string] = line.split(',', 1)
    email_string = email_string.replace("\n", '')
    mailing_list = email_string.split(',')
    name = dname.replace('&', '').replace('!', '').replace('\'', '').replace('-', '').replace('  ', ' ')
    username = camelize(name).lower()
    password = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(N))
    url = SITE_URL + "events/" + camelize(name) + "/"
    e = Event(name = name, display_name = dname, url = url)
    e.save()
    u = User.objects.create_user(username = username, email = mailing_list[0], password = password)
    u.save()
    UserProfile(user = u, is_coord = True, coord_event = e).save()              #All coords are implicitly female :P
    content = msg.render(Context({"username":username,"password":password}))
    subject = name + ": Your shaastra.org access details"
    send_mail(subject, content, sender, mailing_list)

for line in f:
    insert(line)

print "success"

