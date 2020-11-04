from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                        PermissionsMixin
# These are all things that are required to extend the Django user model whilst making use of some of the features that come with the django user model out of the box.


# The manager class is a class that provides the helper functions for creating a user or creating a super user.
class UserManager(BaseUserManager):

    # this function when you call create user it creates a new user model, it sets the password and it saves the model and then it returns the user model that it has just created.
    def create_user(self, email, password=None, **extra_fields):
        # **extra_fields basically says take any of the extra functions that are passed in when you call the create user and pass them into extra fields so that we can then just add any additional fields that we create without user model.
        # It's not required but it just makes our function a little more flexible because every time we add new fields to our user it means we don't have to add them in here we can just add them ad hoc as we add them to our model.
        """Creates and saves a new user"""
        if not email:  # checks if an email was not inserted
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)  # normalize email is a helper function that comes with the base user manager, and makes the domain of the email lower case
        # user = self.model(email=email, **extra_fields) added features to the line above
        # the way that the management commands work is you can access the model that the manager is for by just typing self.model
        # so this is effectively the same as creating a new user model and assigning it to the user variable.
        user.set_password(password)
        # You can't set the password in this call because the password has to be encrypted it's very important that the password is not stored in clear text and
        # the way you do that is you use the set password helper function that comes with the Django base user or the abstractbaseuser.
        user.save(using=self._db)
        # using=self._db is just required for supporting multiple databases which we're not gonna worry about in this course but it's good practice to keep it in there anyway.
        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True  # is_superuser is included as part of the PermissionsMixin.
        user.save(using=self._db)
        return user


# this class basically gives us all the features that come out of the box with the Django user model but we can then build on top of them and customize it to support our email address.
class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()  # assign the user manager to the objects attribute/ creates a new user manager for our object.

    USERNAME_FIELD = 'email'  # by default the user name field is username and we're customizing that to email so we can use an email address.
