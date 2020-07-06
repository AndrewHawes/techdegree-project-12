from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase

from projects.models import Project, Position, Application

user1 = {'full_name': 'Zorbert Kraft', 'email': 'zorbert@example.com'}
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


class ProjectModelsTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user1 = User.objects.create(**user1)
        self.user2 = User.objects.create(**user2)
        self.project = Project.objects.create(**project1)

    def test_project_creation(self):
        project = Project.objects.create(**project2)

        self.assertEqual(project.owner.email, 'zorbert@example.com')
        self.assertEqual(self.user1, project.owner)
        self.assertEqual('A Test Project', project.title)
        self.assertIn("I'm a project description.", project.description)
        self.assertEqual(str(project), project.title)

    def test_project_duplicate_constraint(self):
        # User cannot create two projects with same title
        with self.assertRaises(IntegrityError):
            Project.objects.create(**project1)
            Project.objects.create(**project1)

    def test_project_markdown_inactive(self):
        self.assertFalse(self.user1.profile.using_markdown)
        self.assertEqual(self.project.description, self.project.get_description())
        self.assertNotIn('h1', self.project.get_description())

    def test_project_markdown_active(self):
        self.assertFalse(self.user1.profile.using_markdown)

        self.user1.profile.using_markdown = True
        self.user1.profile.save()

        self.assertTrue(self.user1.profile.using_markdown)
        self.assertIn('h1', self.project.get_description())


class PositionModelTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user1 = User.objects.create(**user1)
        self.user2 = User.objects.create(**user2)
        self.project = Project.objects.create(**project1)
        self.position = Position.objects.create(**position1)

    def test_position_creation(self):
        position = Position.objects.create(**position2)
        self.assertIn('Fish Trainer', position.title)
        self.assertEqual(position.project, self.project)

        self.assertFalse(position.filled)
        position.filled_by = self.user2
        position.save()
        self.assertTrue(position.filled)

        self.assertEqual(str(position), position.title)

    def test_position_markdown_inactive(self):
        self.assertFalse(self.user1.profile.using_markdown)
        self.assertEqual(self.position.description, self.position.get_description())
        self.assertNotIn('h1', self.position.get_description())

    def test_position_markdown_active(self):
        self.user1.profile.using_markdown = True
        self.user1.profile.save()
        self.user1.save()

        self.assertTrue(self.user1.profile.using_markdown)
        self.assertIn('h1', self.position.get_description())

class ApplicationModelTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user1 = User.objects.create(**user1)
        self.user2 = User.objects.create(**user2)
        self.project = Project.objects.create(**project1)
        self.position = Position.objects.create(**position1)

    def test_application_creation(self):
        application = Application.objects.create(**application1)
        self.assertEqual(application.applicant, self.user2)
        self.assertEqual(application.position, self.position)
        self.assertEqual(application.project, self.position.project)
        self.assertIn(application.position.title, str(application))

    def test_approve(self):
        application = Application.objects.create(**application1)
        self.assertIsNone(application.accepted)
        application.approve()
        self.assertTrue(application.accepted)

    def test_reject(self):
        application = Application.objects.create(**application1)
        self.assertIsNone(application.accepted)
        application.reject()
        self.assertFalse(application.accepted)