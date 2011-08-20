from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.contrib.auth.models import User

from main_test.events.models import *
from main_test.users.models import *
from main_test.submissions.models import *
from main_test.misc.util import *
from main_test.settings import *
from main_test.myshaastra.models import *
from main_test.myshaastra.forms import *

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
            raise Http404
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
    member_teams = None
    leader_teams = None
    team_submissions = []
    try:
        teams = Team.objects.filter(members__id__exact = user.id)
        member_teams = teams.exclude(leader = user)
        leader_teams = teams.filter(leader = user)
        # try:
            # for team in teams:                
                # ts = TeamSubmissions.objects.filter(team = team)
                # team_submissions.extend(ts)
        # except:
            # pass
    except:
        pass
    indi_submissions = None
    try:
        indi_submissions = IndividualSubmissions.objects.filter(participant = user)
    except:
        pass
    display_add_join_team = False
    if teams is not None:
        display_add_join_team = True
    #Add/join team functionality
    #Account settings page
    create_team_form = CreateTeamForm()
    return render_to_response('myshaastra/home.html', locals(), context_instance = global_context(request))

def get_authentic_team(request = None, team_id = None):
    if team_id is None or request is None:
        return None
    try:
        team = Team.objects.get(pk = int(team_id))
        try:
            team.members.get(pk = request.user.id)
            return team
        # Non-members fail the test
        except User.DoesNotExist:
            return None
    except Team.DoesNotExist:
        return None
    return None

@needs_authentication
def team_home(request, team_id = None):
    team = get_authentic_team(request, team_id)
    if team is not None:
        add_member_form = AddMemberForm()
        change_leader_form = ChangeLeaderForm()
        return render_to_response('myshaastra/team_home.html', locals(), context_instance = global_context(request))
    raise Http404

@needs_authentication
def create_team(request, event_id = None):
    if event_id is None:
        raise Http404
    user = request.user
    event = None
    try:
        event = Event.objects.get(pk = int(event_id))
    except:
        raise Http404
    form = CreateTeamForm(initial = { 'event' : event.id, } )
    view = "Create"
    if request.method == 'POST':
        form = CreateTeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit = False)
            team.leader = user
            try:
                team.leader.get_profile().registered.get(pk = team.event.id)
            except Event.DoesNotExist:
                team.leader.get_profile().registered.add(team.event)
            team.save()
            team.members.add(user)
            return HttpResponseRedirect('%smyshaastra/' % SITE_URL)
    return render_to_response('myshaastra/create_team.html', locals(), context_instance = global_context(request))

'''
def join_team(request):
    user = request.user
    form = JoinTeamForm()
    view = "Join"
    if request.method == 'POST':
        form = JoinTeamForm(request.POST)
        if form.is_valid():
            team = Team.objects.get(name = form.cleaned_data['name'], event = form.cleaned_data['event'])
            team.join_requests.add(user)
            return HttpResponseRedirect('%smyshaastra/' % SITE_URL)
    return render_to_response('myshaastra/team_form.html', locals(), context_instance = global_context['request'])
'''

@needs_authentication
def add_member(request, team_id = None):
    team = get_authentic_team(request, team_id)    
    if team is not None:
        add_member_form = AddMemberForm()
        change_leader_form = ChangeLeaderForm()
        if request.method == 'POST':
            user = request.user
            add_member_form = AddMemberForm(request.POST)
            if add_member_form.is_valid():
                if user != team.leader:
                    return HttpResponseRedirect('myshaastra/you_arent_leader.html', locals(), context_instance = global_context(request))
                member = User.objects.get(username = add_member_form.cleaned_data['member'])
                # autoregister member on addition to the team
                try:
                    member.get_profile().registered.get(pk = team.event.id)
                except Event.DoesNotExist:
                    member.get_profile().registered.add(team.event)
                team.members.add(member)
                return HttpResponseRedirect('%smyshaastra/' % SITE_URL)           # this probably needs to be changed to the submissions form page
        return render_to_response('myshaastra/team_home.html', locals(), context_instance = global_context(request))
    raise Http404

@needs_authentication
def change_team_leader(request, team_id = None):
    team = get_authentic_team(request, team_id)
    if team is not None:
        change_leader_form = ChangeLeaderForm()
        add_member_form = AddMemberForm()
        if request.method == 'POST':
            user = request.user
            change_leader_form = ChangeLeaderForm(request.POST)
            if change_leader_form.is_valid():
                if user != team.leader:
                    return render_to_response('myshaastra/you_arent_leader.html', locals(), context_instance = global_context(request))
                new_leader = team.members.get(username = change_leader_form.cleaned_data['new_leader'])
                team.leader = new_leader
                team.save()
                return HttpResponseRedirect('%smyshaastra/' % SITE_URL)           # this probably needs to be changed - i dunno to what :P
        return render_to_response('myshaastra/team_home.html', locals(), context_instance = global_context(request))
    raise Http404

@needs_authentication
def drop_out(request, team_id = None):
    team = get_authentic_team(request, team_id)
    if team is not None:
        user = request.user
        if user == team.leader:
            return render_to_response('myshaastra/you_are_leader.html', locals(), context_instance = global_context(request))
        else:
            team.members.remove(user)
            return HttpResponseRedirect('%smyshaastra/' % SITE_URL)
    raise Http404

@needs_authentication
def remove_member(request, team_id = None):
    team = get_authentic_team(request, team_id)
    if team is not None:
        change_leader_form = ChangeLeaderForm()            # it is the same form essentially :P
        add_member_form = AddMemberForm()
        if request.method == 'POST':
            user = request.user
            change_leader_form = ChangeLeaderForm(request.POST)
            if change_leader_form.is_valid():
                team = Team.objects.get(pk = change_leader_form.cleaned_data['team_id'])
                if user != team.leader:
                    return HttpResponseRedirect('myshaastra/you_arent_leader.html', locals(), context_instance = global_context(request))
                new_leader = team.members.get(username = change_leader_form.cleaned_data['new_leader'])           
                team.members.remove(new_leader)                                                # yes i know, it looks bad. but what the hell. i'm lazy.
                return HttpResponseRedirect('%smyshaastra/' % SITE_URL)           # this probably needs to be changed - i dunno to what :P
        return render_to_response('myshaastra/team_home.html', locals(), context_instance = global_context(request))
    raise Http404

@needs_authentication
def ambassador_form(request):
    user = request.user
    sa = ShaastraAmbassador(user = user)
    form = ShaastraAmbassadorForm(instance = sa)
    if request.method == 'POST':
        if form.is_multipart():
            form = ShaastraAmbassadorForm(request.POST, request.FILES)
        else:
            form = ShaastraAmbassadorForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('%smyshaastra/' % SITE_URL)
    return render_to_response('myshaastra/shaastra_ambassador.html', locals(), context_instance = global_context(request))

@needs_authentication
def ambassador_list(request):
    user = request.user
    if user.username != 'cores':
        raise Http404
    ambassador_list = ShaastraAmbassador.objects.all()
    return render_to_response('myshaastra/ambassador_list.html', locals(), context_instance = global_context(request))

@needs_authentication
def ambassador_details(request, ambassador_id = None):
    user = request.user
    if user.username != 'cores':
        raise Http404
    if ambassador_id is None:
        raise Http404
    try:
        sa = ShaastraAmbassador.objects.get(pk = int(ambassador_id))
        sa.profile = sa.user.get_profile()
        return render_to_response('myshaastra/ambassador_details.html', locals(), context_instance = global_context(request))
    except ShaastraAmbassador.DoesNotExist:
        raise Http404
    raise Http404
