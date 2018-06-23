from django.test import TestCase
from django.db.utils import IntegrityError

from accounts.models import User


class UserTestCase(TestCase):

    def test_email_must_be_unique(self):
        data = {'email': 'user@test.com', 'password': 'test123'}
        User.objects.create_user(**data)

        with self.assertRaisesMessage(IntegrityError, 'UNIQUE constraint failed: accounts_user.email'):
            User.objects.create_user(**data)

    def test_create_a_staff_user(self):
        data = {'email': 'user@test.com', 'password': 'test123'}
        not_staff_user = User.objects.create_user(**data)
        self.assertEqual(False, not_staff_user.is_staff)

        not_staff_user.delete()

        data = {'email': 'user@test.com', 'password': 'test123'}
        staff_user = User.objects.create_staffuser(**data)

        self.assertEqual(True, staff_user.is_staff)

    def test_create_admin_user(self):
        data = {'email': 'user@test.com', 'password': 'test123'}
        not_admin_user = User.objects.create_user(**data)
        self.assertEqual(False, not_admin_user.is_admin)

        not_admin_user.delete()

        data = {'email': 'user@test.com', 'password': 'test123'}
        admin_user = User.objects.create_superuser(**data)

        self.assertEqual(True, admin_user.is_admin)

    def test_cant_create_a_user_without_an_email(self):
        data = {'email': '', 'password': 'test123'}

        with self.assertRaisesMessage(ValueError, 'Users must have an email address'):
            User.objects.create_user(**data)
