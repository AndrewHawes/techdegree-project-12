from django import forms
from django.contrib import admin
from django.contrib.admin.views.main import ChangeList

from accounts.models import Skill
from .models import Application, Project, Position


class ApplicationInline(admin.TabularInline):
    model = Application
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    fields = ['owner', 'title', 'description', 'timeline',
              'applicant_requirements', 'is_active']
    list_display = ['title', 'owner', 'is_active', 'description']
    list_editable = ['description']


class SkillInline(admin.TabularInline):
    model = Position.skills.through


class PositionChangeListForm(forms.ModelForm):
    skills = forms.ModelMultipleChoiceField(queryset=Skill.objects.all(), required=False)


class PositionChangeList(ChangeList):
    def __init__(self, request, model, list_display, list_display_links,
                 list_filter, date_hierarchy, search_fields, list_select_related,
                 list_per_page, list_max_show_all, list_editable, model_admin,
                 sortable_by):

        super().__init__(request, model, list_display, list_display_links,
                         list_filter, date_hierarchy, search_fields,
                         list_select_related, list_per_page, list_max_show_all,
                         list_editable, model_admin, sortable_by)

        self.list_display = ['action_checkbox', 'title', 'skills']
        self.list_display_links = ['title']
        self.list_editable = ['skills']


class PositionAdmin(admin.ModelAdmin):
    def get_changelist(self, request, **kwargs):
        return PositionChangeList

    def get_changelist_form(self, request, **kwargs):
        return PositionChangeListForm


admin.site.register(Project, ProjectAdmin)
admin.site.register(Application)
admin.site.register(Position, PositionAdmin)
