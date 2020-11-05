from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate  # authenticate function which comes with Django and it's a Django helper command for working with the Django authentication system. So you simply pass in the username and password and you can authenticate a request
from django.utils.translation import ugettext_lazy as _


class UserSerializer(serializers.ModelSerializer):  # Django rest framework has a built-in serializer that we can do this with that we just need to specify the fields that we want from our module and it does the database conversion for us. And even helps with the creating and retrieving from the database.
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()  # model that you want to base your model sterilizer from. Call the get_user_model so it actually returns the user model class
        fields = ('email', 'password', 'name')  # fields that you want to include in serializer so these are the fields that are going to be converted to and from json when we make our HTTP POST and then we retrieve that in our view and then we want to save it to a model. So it basically are the fields that we want to make accessible in the API either to read or write.
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}  # extra keyword args allows us to configure a few extra settings in our model serilizer. We use this to ensure that the password is write only and that the minimum required length is 5 characters. Extra_kwargs allows you to set some extra restrictions or arguments for the fields that we reference in our fields variable here.

    def create(self, validated_data):  # The create function is the function that's called when we create a new object. I t basically specifies all the available functions that you can override in the different serializers that are available. We're going to override the create function here. We're going to call the create user function in our model because by default it only calls the create function and we want to use our create user model manager function that we created in our models to create the user so we know that the password that it stores will be encrypted. Otherwise the password that it sets will just be the clear text password that we pass in and then the authentication won't work because it's expecting an encrypted salt key.
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)  # we're going to use this star syntax here to unwind this validated data into the parameters of the create user function.
# Django rest framework: when we're ready to create the user it will call the create function and it will pass in the validated data the validated data will contain all of the data that was passed into our serializer which would be the JSON data that was made in the HTTP POST and it passes it as the argument here and then we can then use that to create our user.

    def update(self, instance, validated_data):  # The purpose of this is we want to make sure the password is set using the set password function instead of just setting it to whichever value is provided.
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


# Token endpoint.
# This is going to be an endpoint that you can make a HTTP POST request and you can generate a temporary auth token that you can then use to authenticate future requests with the API.
# With our API we're going to be using token authentication.
# So the way that you log in is you use this API to generate a token and then you provide that token as the authentication header for future requests which you want to authenticate.
# The benefit of this is you don't need to send the user's username and password with every single request that you make.
# You just need to send it once to create the token and then you can use that token for future requests and if you ever want to revoke the token you can do that in the database.
class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""  # overriding the default token serializer; we're just modifying it slightly to accept our email address instead of username.
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False  # because it's possible to have whitespace in your password (default Django rest framework serializer will trim off this white space)
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')  # attrs parameter here is basically just every field that makes up our serializer; so any field that makes up a sterilizer will get passed into the validate function here as this dictionary and then we can retrieve the fields via this attributes and we can then validate whether we want to pass this validation or we want to fail the validation.
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')  # Django rest framework knows how to handle this error and it handles it by passing the error as a 400 response and sending a response to the user which describes this message here basically, it just says unable to authenticate with provided credentials.

        attrs['user'] = user
        return attrs  # whenever you're overriding the validate function you must return the values at the end once the validation is successful.
