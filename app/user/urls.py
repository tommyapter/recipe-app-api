from django.urls import path  # This is a helper function that comes with Django that allows us to define different paths in our app.

from . import views


app_name = 'user'  # the app name is set to help identify which app we're creating the URL from when we use our reverse function

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]
# name is so that we can identify it when using the reverse lookup function the name is going to be create
# put a comma there at the end because it's good to practice
