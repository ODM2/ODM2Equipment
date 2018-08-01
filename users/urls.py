from django.urls import path
from .views import CreateUserView

app_name = 'users'
urlpatterns = [
    path('signup', CreateUserView.as_view(), name='signup')
]
