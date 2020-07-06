import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from projects.models import Project


class ProjectViewsTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(email='zorbert@example.com')
        self.project = Project.objects.create(
            owner=self.user,
            title='Main Test Project',
            url='http://www.example.com',
            description='# A Heading\nA test description',
            timeline='2 weeks',
            applicant_requirements='No requirements'
        )

    def test_create_project(self):
        project = Project.objects.create(
            owner=self.user,
            title='Test Project',
        )
        self.assertEqual(project.date_created, datetime.date.today())

    def test_project_detail(self):
        resp = self.client.get(reverse('project', args=[1]))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['project'], self.project)

    # CreateProjectView(LoginRequiredMixin, CreateView)
    # UpdateProjectView(LoginRequiredMixin, UpdateView)
    #
    # @login_required(login_url=reverse_lazy('signin'))
    # def applications(request):
    #
    # def project_detail(request, pk):
    # @receiver(application_status_changed, sender=Application, dispatch_uid="application_status_email")
    # def send_application_status_email(sender, instance, current_site, email_template, **kwargs):
    #
    # class DeleteProjectView(DeleteView):
    pass


class ProjectFormTests(TestCase):
    pass