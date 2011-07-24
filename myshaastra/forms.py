from django import forms

from main_test.users.models import Team
from main_test.events.models import Event

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
        if 'name' is in data and 'event' is in data:
            try:
                Team.objects.filter(event__id = data['event'].id).get(name__iexact = data['name'])
                raise ValidationError('A team with the same name already exists for this event!')
            except Team.DoesNotExist:
                pass
        return data
    
    class Meta:
        model = Team
        fields = ('name', 'event')

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
        if 'name' is in data and 'event' is in data:
            try:
                Team.objects.filter(event__id = data['event'].id).get(name__iexact = data['name'])
            except Team.DoesNotExist:
                raise ValidationError('A team with this name does not exist for this event!')
        return data
    
    class Meta:
        model = Team
        fields = ('name', 'event')

