from users.models import *
f = open('/home/shaastra/final_results.txt')
usernames = f.readlines()
f.close()
users = []
for username in usernames:
    username = username.replace('\n', '')
    users.append(User.objects.get(username = username))
print users
