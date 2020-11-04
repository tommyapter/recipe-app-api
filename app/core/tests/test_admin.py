from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse  # allow us to generate URLs for our Django admin page.


class AdminSiteTests(TestCase):

    def setUp(self):  # setup function is a function that is ran before every test that we run so sometimes there are setup tasks that need to be done before every test in our test case class.
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@londonappdev.com',
            password='password123'
        )
        self.client.force_login(self.admin_user)  # force_login allows you to log a user in with the Django authentication and this really helps make our tests a lot easier to write because it means we don't have to manually log the user in.
        self.user = get_user_model().objects.create_user(
            email='test@londonappdev.com',
            password='password123',
            name='Test User Full Name',
        )

    def test_users_listed(self):
        """Test that users are listed on the user page"""     # test that the users are listed in our Django admin. The reason we need to add a test for this is because we need to slightly customize the Django admin to work with our custom user model so as explained previously the default user model expects a username and as such the default Django admin for the user model also expects a username which we don't have user name we just have the email address so we need to make a few small changes to our admin.py file just to make sure it supports our custom user model.
        # reverse will generate the URL for our list user page. We use this reverse function instead of just typing the URL manually is because if we ever want to change the URL in a future it means we don't have to go through and change it everywhere in our test because it should update automatically based on reverse.
        url = reverse('admin:core_user_changelist')  # pass to reverse, the app that you're going for : the URL that you want; These URLs are actually defined in the Django admin documentation
        res = self.client.get(url)

        self.assertContains(res, self.user.name)  # assertContains check that our response here contains a certain item. It checks that the HTTP response was HTTP 200 and that it looks into the actual content of this res because if you were to manually output this res it's just an object so it's intelligent enough to look into the actual output that is rendered and to check for the contents there
        self.assertContains(res, self.user.email)

    def test_user_page_change(self):
        """Test that the user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])  # reverse function will create a URL like /admin/core/user/id of the user. And this is how the args argument works in the reverse function. So basically anything we pass in here will get assigned to the arguments of the URL here at the end so that's how we customize the ID.

        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
