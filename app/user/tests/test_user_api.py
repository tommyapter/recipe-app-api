from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient  # this just is a test client that we can use to make requests to our API and then check what the response is.
from rest_framework import status  # us from rest framework. So it's from rest_framework import status and all this is is a module that contains some status codes that we can see in basically human readable form so instead of just typing 200 it's HTTP 200 ok it just makes the tests a little bit easier to read and understand.
# Every single test that runs it refreshes the database so these users that were created in one test are not going to be accessible in another test

CREATE_USER_URL = reverse('user:create')
# at the beginning of any API test that I create. I add either a helper function or a constant variable for our URL that we're going to be testing.
# Doing it all caps is a naming convention for anything you expect to be a constant
# reverse should create the user create URL and assign it to this create user URL variable.
TOKEN_URL = reverse('user:token')  # So this is going to be the URL that we're going to use to make the HTTP POST request to generate our token.


def create_user(**params):
    """Helper function to create new user"""
    return get_user_model().objects.create_user(**params)
# helper function that we can use to create some example users for our tests.
# So anything that you do multiple times in different tests I like to create a helper function so instead of creating the user for each test individually
# **params is a dynamic list of arguments. So we can basically add as many arguments as we want here and we can then pass them directly into the create user model. That will mean we have a lot of flexibility about the fields that we can assign to the users that we create for our samples.


class PublicUserApiTests(TestCase):  # Personal preference to separate my API tests into public and private tests, as it keeps the tests nice and clean because then in your setup you can have one that authenticates and one that doesn't authenticate. A public API is one that is unauthenticated so anyone from the internet can make a request. An example of this would be the create user because when you typically create a user on a system usually you're creating a user because you haven't got authentication set up already.
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()  # this makes it easier to call our client in our test, so every single test we run we don't need to manually create this API client we just have one client for our test suite that we can reuse for all of the tests.

    def test_create_valid_user_success(self):
        """Test creating using with a valid payload is successful"""  # the payload is the object that you pass to the API when you make the request so we're just going to test that if you pass in all the correct fields then the user is created successfully
        payload = {
            'email': 'test@londonappdev.com',
            'password': 'testpass',
            'name': 'name',
        }
        res = self.client.post(CREATE_USER_URL, payload)  # make our requests. This will do a HTTP POST request to our client to our URL for creating users

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)  # We expect a HTTP 201 created response from the API.
        user = get_user_model().objects.get(**res.data)  # Test that the object is actually created. **res.data will take the dictionary response. If this gets the user successfully then we know that the user is actually being created properly.
        self.assertTrue(
            user.check_password(payload['password'])  # test our password is correct
        )
        self.assertNotIn('password', res.data)  # check that the password is not returned as part of this object

    def test_user_exists(self):
        """Test creating a user that already exists fails"""
        payload = {'email': 'test@londonappdev.com', 'password': 'testpass', 'name': 'Test', }
        create_user(**payload)  # **payload will pass email=test@londonappdev.com password=testpass. The ** just make it a little less wordy, a bit cleaner.
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)  # We expect to see here is a HTTP 400 bad request because the user already exists

    def test_password_too_short(self):
        """Test that password must be more than 5 characters"""
        payload = {'email': 'test@londonappdev.com', 'password': 'pw'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {'email': 'test@londonappdev.com', 'password': 'testpass'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)  # make our request and store it in a variable called res

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given"""
        create_user(email='test@londonappdev.com', password='testpass')
        payload = {'email': 'test@londonappdev.com', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user doens't exist"""
        payload = {'email': 'test@londonappdev.com', 'password': 'testpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required"""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
