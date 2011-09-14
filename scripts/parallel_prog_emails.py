from users.models import *
f = open('final_results.txt')
usernames = []
for line in f:
    usernames.append(str(line))
f.close()
users = []
for username in useranmes:
    users.append(User.objects.get(username))
print users
