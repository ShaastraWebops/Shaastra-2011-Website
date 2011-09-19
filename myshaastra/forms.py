from django import forms
from django.contrib.auth.models import User

from main_test.users.models import Team
from main_test.events.models import Event
from main_test.myshaastra.models import ShaastraAmbassador

class CreateTeamForm(forms.ModelForm):
    
    def clean_event(self):
        if 'event' in self.cleaned_data:
            event = self.cleaned_data['event']
            try:
                Event.objects.get(pk = event.id)
            except Event.DoesNotExist:
                raise forms.ValidationError('Not a valid event')
        return self.cleaned_data['event']
    
    def clean(self):
        data = self.cleaned_data
        if 'name' in data and 'event' in data:
            try:
                Team.objects.filter(event__id = data['event'].id).get(name__iexact = data['name'])
                raise forms.ValidationError('A team with the same name already exists for this event!')
            except Team.DoesNotExist:
                pass
        return data
    
    class Meta:
        model = Team
        fields = ('name', 'event')
        widgets = {
            'event' : forms.HiddenInput(),
        }

class JoinTeamForm(forms.ModelForm):
    
    def clean_event(self):
        if 'event' in self.cleaned_data:
            event = self.cleaned_data['event']
            try:
                Event.objects.get(pk = event.id)
            except Event.DoesNotExist:
                raise forms.ValidationError('Not a valid event')
        return self.cleaned_data['event']
    
    def clean(self):
        data = self.cleaned_data
        if 'name' in data and 'event' in data:
            try:
                Team.objects.filter(event__id = data['event'].id).get(name__iexact = data['name'])
            except Team.DoesNotExist:
                raise forms.ValidationError('A team with this name does not exist for this event!')
        return data
    
    class Meta:
        model = Team
        fields = ('name', 'event')

class AddMemberForm(forms.Form):
    member = forms.CharField(max_length = 50, help_text = "Please enter your friend's username")
    team_id = forms.IntegerField()
    
    def clean_team_id(self):
        team_id = self.cleaned_data['team_id']
        try:
            team = Team.objects.get(pk = team_id)
        except Team.DoesNotExist:
            raise forms.ValidationError('Team does not exist!')
        return team_id
    
    def clean_member(self):
        member = self.cleaned_data['member']
        try:
            user = User.objects.get(username = member)
            if not user.is_active:
                raise forms.ValidationError('This user is not active! Please ask him/her to activate his account first.')
        except User.DoesNotExist:
            raise forms.ValidationError('No such user!')
        return member
    
    def clean(self):
        data = self.cleaned_data
        if 'team_id' and 'member' in data:
            team = Team.objects.get(pk = data['team_id'])
            # check if this user is already a part of another team (any team) for the same event
            if Team.objects.filter(event = team.event).filter(members__username = data['member']).count() > 0:
                msg = 'This user is already a part of a team for this event!'
                self._errors['member'] = self.error_class([ msg, ])
                del data['member']
        return data

class ChangeLeaderForm(forms.Form):
    new_leader = forms.CharField(max_length = 50, help_text = "Please enter the new leader's username")
    team_id = forms.IntegerField()
    
    def clean_team_id(self):
        team_id = self.cleaned_data['team_id']
        try:
            team = Team.objects.get(pk = int(team_id))
        except Team.DoesNotExist:
            raise forms.ValidationError('Team does not exist!')
        return team_id
    
    def clean(self):
        data = self.cleaned_data
        if 'team_id' and 'new_leader' in data:
            team = Team.objects.get(pk = data['team_id'])
            try:
                user = team.members.get(username = data['new_leader'])
            except User.DoesNotExist:
                raise forms.ValidationError('This user is not a part of this team')
        return data

class ShaastraAmbassadorForm(forms.ModelForm):
    
    def clean_user(self):
        if 'user' in self.cleaned_data:
            user = self.cleaned_data['user']
            try:
                User.objects.get(pk = user.id)
            except User.DoesNotExist:
                raise forms.ValidationError('User does not exist!')
        return self.cleaned_data['user']
    
    class Meta:
        model = ShaastraAmbassador
        widgets = {
            'user' : forms.HiddenInput(),
        }

class AccommodationForm(forms.Form):
    username = forms.CharField(max_length = 80, widget = forms.HiddenInput)
    
    def clean_username(self):
        data = self.cleaned_data
        if 'username' in data:
            try:
                User.objects.get(username = data['username'])
            except User.DoesNotExist:
                raise forms.ValidationError('This user does not exist!')
        return data['username']
    
