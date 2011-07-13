from django.contrib import admin
from main_test.users.models import *

for x in main_test.users.models:
    admin.site.register(x)
