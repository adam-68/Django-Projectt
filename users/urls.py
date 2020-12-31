from django.conf.urls import url
from users import views
from django.urls import path
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name='register'),
    path("home/", views.HomePageView.as_view(), name="home"),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path('profile/<str:username>/', views.ProfileView.as_view(), name="user_profile"),
]
