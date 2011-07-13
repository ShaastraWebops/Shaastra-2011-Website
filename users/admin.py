from django.contrib import admin
from main_test.users import models

for x in models:
    admin.site.register(x)
