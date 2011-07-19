from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response

from main_test.events.models import *
from main_test.users.models import *
from main_test.misc.util import *
from main_test.settings import *

@needs_authentication
def home(request):
    user = request.user
    userprof = user.get_profile()
    events_list = userprof.registered.all()
    #Should show all other events of the same tag. Until tags are implemented, will show all other events of the same category
    category = None
    for event in events_list:
        try:
            category = Menu.objects.get(event = event).parent_menu
            event.similar = category.menu_set.exclude(event = event)
        except Menu.DoesNotExist:
            raise http404
    ''' 
        for event in events_list:
            try:
                tags = event.tag_set.all()
                for tag in tags:
                    #construct a Q object orred with event names
    '''
    display_email_sms_update = False
    try:
        r = userprof.receive_updates
        display_email_sms_updates = True
    except:
        pass
    teams = None
    try:
        teams = Team.objects.filter(members__id__exact = user.id)
    except:
        pass
    #Display all submissions that this person is linked to
    #Add/join team functionality
    #Account settings page
    return render_to_response('myshaastra/home.html', locals(), context_instance = global_context(request))

