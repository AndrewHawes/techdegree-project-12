from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError, transaction
from django.dispatch import receiver
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from .forms import PositionFormSet, ProjectForm
from .models import Application, Project, Position

from .signals import application_status_changed


class CreateProjectView(LoginRequiredMixin, CreateView):
    login_url = '/signin/'
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_new.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = PositionFormSet(self.request.POST)
        else:
            data['formset'] = PositionFormSet()
        return data

    def form_valid(self, form):
        title = form.cleaned_data.get('title')
        if Project.objects.filter(title=title, owner=self.request.user).exists():
            messages.error(self.request, 'You have already created a project with that name.')
            return self.render_to_response(self.get_context_data(form=form))

        form.instance.owner = self.request.user
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            with transaction.atomic():
                self.object = form.save()
                formset.instance = self.object
                formset.save()
        else:
            return self.render_to_response(context)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('project', args=(self.object.id,))


class UpdateProjectView(LoginRequiredMixin, UpdateView):
    login_url = '/signin/'
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_edit.html'

    def get_object(self, queryset=None):
        obj = super().get_object()

        if not obj.owner == self.request.user:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        #
        qs = Position.objects.prefetch_related('skills')
        #
        if self.request.POST:
            # data['formset'] = PositionFormSet(self.request.POST, instance=self.object)
            data['formset'] = PositionFormSet(self.request.POST, instance=self.object, queryset=qs)
        else:
            # data['formset'] = PositionFormSet(instance=self.object)
            data['formset'] = PositionFormSet(instance=self.object, queryset=qs)
        return data

    def form_valid(self, form):
        project = self.get_object()
        new_title = form.cleaned_data.get('title')

        if project.title != new_title:
            print('original:', project.title, 'new:', form.cleaned_data.get('title'))
            if Project.objects.filter(title=new_title, owner=self.request.user).exists():
                messages.error(
                    self.request,
                    'You have already created another project with that name.'
                )
                return self.render_to_response(self.get_context_data(form=form))

        form.instance.owner = self.request.user
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            with transaction.atomic():
                try:
                    self.object = form.save()
                except IntegrityError:
                    messages.error(
                        self.request,
                        'You have already created another project with that name.')
                formset.instance = self.object
                formset.save()
        else:
            return self.render_to_response(context)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('project', args=(self.object.id,))


def project_detail(request, pk):
    queryset = (
        Project.objects
        .select_related('owner__profile')
        .prefetch_related('positions__skills', 'positions__applicants')
    )
    project = get_object_or_404(queryset, pk=pk)

    return render(request, 'projects/project.html', {'project': project})


@login_required(login_url=reverse_lazy('signin'))
def applications(request):
    open_applications = (
        Application.objects
        .filter(position__project__owner=request.user)
        .filter(position__filled=False, position__project__is_active=True)
        .select_related('position__project')
        .select_related('applicant__profile')
        .prefetch_related('applicant__owned_projects')
        .order_by('applicant__profile__display_name', 'position__title')
    )
    position_titles = (
        open_applications
        .values_list('position__title', flat=True)
        .order_by('position__title')
        .distinct()
    )
    context = {
        'applications': open_applications,
        'position_titles': position_titles
    }

    return render(request, 'projects/applications.html', context)


@receiver(application_status_changed, sender=Application, dispatch_uid="application_status_email")
def send_application_status_email(sender, instance, current_site, email_template, **kwargs):
    subject = 'Your Recent Application for {}'.format(instance.position.title)
    email_context = {
        'position': instance.position.title,
        'project': instance.position.project.title,
        'domain': current_site.domain,
    }
    message = render_to_string(email_template, email_context)
    instance.applicant.email_user(subject, message)


class DeleteProjectView(DeleteView):
    model = Project
    success_url = reverse_lazy('profile')
    template_name = 'projects/project_confirm_delete.html'

    def get_object(self, queryset=None):
        obj = super().get_object()

        if not obj.owner == self.request.user:
            raise Http404
        return obj
