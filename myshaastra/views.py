from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.contrib.auth.models import User

from main_test.events.models import *
from main_test.users.models import *
from main_test.submissions.models import *
from main_test.misc.util import *
from main_test.settings import *
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

@needs_authentication
def team_home(request):
    add_member_form = AddMemberForm()
    change_leader_form = ChangeLeaderForm()
    if request.method == 'GET' and 'team_id' in request.GET:
        team_id = request.GET['team_id']
        try:
            team = Team.objects.get(pk = int(team_id))
            try:
                team.members.get(pk = request.user.id)
            except User.DoesNotExist:
                raise Http404
            team.is_leader = False
            if team.leader == request.user:
                team.is_leader = True
            return render_to_response('myshaastra/team_home.html', locals(), context_instance = global_context(request))
        except Team.DoesNotExist:
            raise Http404
    raise Http404

@needs_authentication
def create_team(request):
    user = request.user
    form = CreateTeamForm()
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
def add_member(request):
    add_member_form = AddMemberForm()
    change_leader_form = ChangeLeaderForm()
    if request.method == 'POST':
        user = request.user
        form = AddMemberForm(request.POST)
        if form.is_valid():
            team = Team.objects.get(pk = form.cleaned_data['team_id'])
            if user != team.leader:
                return HttpResponseRedirect('myshaastra/you_arent_leader.html', locals(), context_instance = global_context(request))
            member = User.objects.get(username = form.cleaned_data['member'])
            # autoregister member on addition to the team
            try:
                member.get_profile().registered.get(pk = team.event.id)
            except Event.DoesNotExist:
                member.get_profile().registered.add(team.event)
            team.members.add(member)
            return HttpResponseRedirect('%smyshaastra/' % SITE_URL)           # this probably needs to be changed to the submissions form page
    return render_to_response('myshaastra/team_home.html', locals(), context_instance = global_context(request))

@needs_authentication
def change_team_leader(request):
    change_leader_form = ChangeLeaderForm()
    add_member_form = AddMemberForm()
    if request.method == 'POST':
        user = request.user
        form = ChangeLeaderForm(request.POST)
        if form.is_valid():
            team = Team.objects.get(pk = form.cleaned_data['team_id'])
            if user != team.leader:
                return render_to_response('myshaastra/you_arent_leader.html', locals(), context_instance = global_context(request))
            new_leader = team.members.get(username = form.cleaned_data['new_leader'])
            team.leader = new_leader
            team.save()
            return HttpResponseRedirect('%smyshaastra/' % SITE_URL)           # this probably needs to be changed - i dunno to what :P
    return render_to_response('myshaastra/team_home.html', locals(), context_instance = global_context(request))

@needs_authentication
def drop_out(request):
    if request.method == 'POST':
        user = request.user
        team_id = request.POST['team_id']
        team = None
        try:
            # team should exist
            team = Team.objects.get(pk = int(team_id))
        except Team.DoesNotExist:
            raise Http404
        try:
            # user should be a team member
            team.members.get(username = user.username)
        except User.DoesNotExist:
            raise Http404
        if user == team.leader:
            return render_to_response('myshaastra/you_are_leader.html', locals(), context_instance = global_context(request))
        else:
            team.members.remove(user)
            return HttpResponseRedirect('%smyshaastra/' % SITE_URL)
    raise Http404

@needs_authentication
def remove_member(request):
    change_leader_form = ChangeLeaderForm()            # it is the same form essentially :P
    add_member_form = AddMemberForm()
    if request.method == 'POST':
        user = request.user
        form = ChangeLeaderForm(request.POST)
        if form.is_valid():
            team = Team.objects.get(pk = form.cleaned_data['team_id'])
            if user != team.leader:
                return HttpResponseRedirect('myshaastra/you_arent_leader.html', locals(), context_instance = global_context(request))
            new_leader = team.members.get(username = form.cleaned_data['new_leader'])           
            team.members.remove(new_leader)                                                     # yes i know, it looks bad. but what the hell. i'm lazy.
            return HttpResponseRedirect('%smyshaastra/' % SITE_URL)           # this probably needs to be changed - i dunno to what :P
    return render_to_response('myshaastra/team_home.html', locals(), context_instance = global_context(request))


