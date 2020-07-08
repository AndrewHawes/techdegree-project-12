from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from projects.models import Project, Position, Application

user1 = {
    'full_name': 'Zorbert Kraft',
    'email': 'zorbert@example.com',
    'password': 'test'
}
user2 = {'full_name': 'Laya Khan', 'email': 'laya@example.com'}

project1 = {
    'owner_id': 1,
    'title': 'Main Test Project',
    'url': 'http://www.example.com',
    'description': '# A Heading\nA test description',
    'timeline': '2 weeks',
    'applicant_requirements': 'No requirements'
}
project2 = {
    'title': 'A Test Project',
    'description': "Hi! I'm a project description.",
    'owner_id': 1
}
position1 = {
    'title': 'Batman Expert',
    'description': '# Batman Expert\nKnows things about Batman.',
    'project_id': 1
}
position2 = {
    'title': 'Fish Trainer',
    'description': 'Trains fish to do amazing things.',
    'project_id': 1
}
application1 = {
    'applicant_id': 2,
    'position_id': 1
}
application2 = {
    'applicant_id': 1,
    'position_id': 2
}


class ProjectViewsTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user1 = User.objects.create(**user1)
        self.user2 = User.objects.create(**user2)
        self.client = Client()
        self.client.force_login(self.user1)
        self.project1 = Project.objects.create(**project1)
        self.project2 = Project.objects.create(**project2)
        self.position1 = Position.objects.create(**position1)
        self.position2 = Position.objects.create(**position2)
        self.application1 = Application.objects.create(**application1)
        self.application2 = Application.objects.create(**application2)

    def test_create_project_view(self):
        url = reverse('project_new')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/project_new.html')

    def test_update_project_view(self):
        url = reverse('project_edit', args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'projects/project_edit.html')

    def test_project_detail_view(self):
        resp = self.client.get(reverse('project', args=[1]))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.project1, resp.context['project'])

    def test_applications_view(self):
        resp = self.client.get(reverse('applications'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.application1, resp.context['applications'])

    def test_delete_project(self):
        project = Project.objects.create(title='Deletion Test', owner=self.user1)
        url = reverse('project_delete', args=[project.id])
        resp = self.client.get(url, follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Are you sure you want to delete")
