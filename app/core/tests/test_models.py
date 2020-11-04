from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email if successful"""
        email = 'a@a.a'
        password = 'test123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'a@A.A'
        user = get_user_model().objects.create_user(email, 'test123')
        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser('a@a.com', 'test123')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


# class AdminSiteTests(TestCase):
#
#     def setUp(self):
#         self.client = Client()
#         self.admin_user = get_user_model().objects.create_superuser(
#             email='admin@londonappdev.com',
#             password='password123'
#         )
#         self.client.force_login(self.admin_user)
#         self.user = get_user_model().objects.create_user(
#             email='test@londonappdev.com',
#             password='password123',
#             name='Test User Full Name',
#         )
#
#     def test_users_listed(self):
#         """Test that users are listed on the user page"""
#         url = reverse('admin:core_user_changelist')
#         res = self.client.get(url)
#
#         self.assertContains(res, self.user.name)
#         self.assertContains(res, self.user.email)
#
#     def test_user_page_change(self):
#         """Test that the user edit page works"""
#         url = reverse('admin:core_user_change', args=[self.user.id])
#         res = self.client.get(url)
#
#         self.assertEqual(res.status_code, 200)
#
#     def test_create_user_page(self):
#         """Test that the create user page works"""
#         url = reverse('admin:core_user_add')
#         res = self.client.get(url)
#
#         self.assertEqual(res.status_code, 200)
