from crispy_forms.helper import FormHelper
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import modelformset_factory, BaseModelFormSet
from djangoformsetjs.utils import formset_media_js

from .fields import CustomModelChoiceField
from .models import CustomUser, Profile, Skill


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'full_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs['placeholder'] = 'Full Name'
        self.fields['full_name'].widget.attrs['autofocus'] = ''
        self.fields['email'].widget.attrs['placeholder'] = 'Email Address'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-lg'
            visible.help_text = None

        self.helper = FormHelper()
        self.helper.label_class = 'sr-only'


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['display_name', 'about']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['display_name'].widget.attrs['class'] = 'form-control form-control-lg'
        self.fields['about'].widget.attrs['class'] = 'form-control'
        self.fields['display_name'].widget.attrs['placeholder'] = 'Name'
        self.fields['about'].widget.attrs['placeholder'] = 'Tell us about yourself...'


class LazyModelChoiceField(CustomModelChoiceField):
    """Bypasses validation to allow custom input."""
    def clean(self, value):
        return value


class SkillForm(forms.ModelForm):
    name = LazyModelChoiceField(
        queryset=Skill.objects.prefetch_related('profiles'),
        to_field_name='name',
        empty_label=None,
        required=False
    )

    class Meta:
        model = Skill
        exclude = ()

    class Media:
        js = formset_media_js + ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['required'] = False
        self.fields['name'].widget.attrs['class'] = 'form-control js-select'
        self.fields['name'].widget.attrs['placeholder'] = 'New skill...'
        self.fields['name'].widget.attrs['autocomplete'] = 'off'

    def clean(self):
        # Bypass validation. Duplicate skills are handled in save method.
        return self.cleaned_data

    def save(self, *args, **kwargs):
        name = self.cleaned_data.get('name')
        if not name:
            return None
        try:
            skill = Skill.objects.get(name=name)
        except Skill.DoesNotExist:
            skill = None

        if skill:
            return skill

        # Abort save if for is marked for deletion to prevent Skill deletion
        if self.cleaned_data.get('DELETE'):
            return None

        return super().save(*args, **kwargs)


class BaseSkillFormSet(BaseModelFormSet):
    def __init__(self, *args, profile, **kwargs):
        self.profile = profile
        super().__init__(*args, **kwargs)
        self.queryset = self.profile.skills.all()

    def clean(self):
        pass


ProfileSkillFormSet = modelformset_factory(
    Skill,
    form=SkillForm,
    formset=BaseSkillFormSet,
    extra=0,
    can_delete=True
)
