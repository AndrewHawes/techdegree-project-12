from django.test import TestCase
from django.contrib.auth import get_user_model


class UserManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email='user@test.com', password='pass')
        self.assertEqual(user.email, 'user@test.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email='')
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', password='pass')

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser('superuser@test.com', 'pass')
        self.assertEqual(admin_user.email, 'superuser@test.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='superuser@test.com', password='pass', is_superuser=False)

