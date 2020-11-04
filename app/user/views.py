from rest_framework import generics  # So this is a view that's pre-made for us that allows us to easily make a API that creates an object in a database using the serialize that we're going to provide.
from rest_framework.authtoken.views import ObtainAuthToken  # this comes with Django rest framework so if you're authenticated using a username and password as standard it's very easy to just switch this on you can just pass in the ObtainAuthToken view directly into our URLs. Because we are customizing it slightly we need to just basically import it into our views and then extend it with a class and then make a few modifications to the class variables.
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for the user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES  # renderer class and all this does is it sets the renderer so we can view this endpoint in the browser with the browsable api. So that means that you can basically login using Chrome or whatever and you can type in the username and password and you can click post and then it should return the token if you don't do this then you have to use a tool such as C URL or some other tool to basically make the HTTP POST request. we're just going to use the default ones and that's why we import them from our API settings so that way if we ever change the renderer class and we want to use a different class to render our basically our browseable API then we can do that in the settings and it will update in our view automatically so we don't have to go through the view and change it.
