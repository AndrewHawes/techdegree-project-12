from django import forms
from django.forms import inlineformset_factory

from djangoformsetjs.utils import formset_media_js

from .models import Project, Position


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'timeline', 'applicant_requirements']
        widgets = {'timeline': forms.Textarea()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['description'].widget.attrs['class'] = 'form-control'
        self.fields['timeline'].widget.attrs['class'] = 'form-control h-75'
        self.fields['applicant_requirements'].widget.attrs['class'] = 'form-control h-75'

        self.fields['title'].widget.attrs['placeholder'] = 'Project Title'
        self.fields['description'].widget.attrs['placeholder'] = 'Project description...'


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['title', 'description', 'time_commitment', 'skills']
        widgets = {'skills': forms.SelectMultiple()}

    class Media:
        js = formset_media_js + ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs['placeholder'] = 'Position Title'
        self.fields['description'].widget.attrs['placeholder'] = 'Position description...'
        self.fields['time_commitment'].widget.attrs['placeholder'] = 'Time Commitment (optional)'

        self.fields['title'].widget.attrs['class'] = "form-control form-control-lg"
        self.fields['description'].widget.attrs['class'] = "form-control"
        self.fields['time_commitment'].widget.attrs['class'] = 'form-control'
        self.fields['skills'].widget.attrs['class'] = "custom-select"

        self.fields['skills'].label = 'Desired Skills:'
        self.fields['description'].widget.attrs['rows'] = '5'


PositionFormSet = inlineformset_factory(Project, Position, form=PositionForm, extra=1,
                                        can_delete=True)
