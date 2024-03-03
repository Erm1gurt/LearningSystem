from . import views
from django.urls import path


urlpatterns = [
    path('', views.homepage, name='home'),
    path('home', views.homepage, name='home'),
    path('course', views.course, name='course'),
    path('course/<slug:course_slug>', views.course, name='course'),
    path('course/<slug:course_slug>/<int:lesson_id>', views.course, name='course'),
    path('course/<slug:course_slug>/create_lesson', views.create_lesson, name='create_lesson'),
    path('course/<slug:course_slug>/join', views.join_course, name='join'),
    path('add_course', views.add_course, name='add_course'),
    path('login', views.LoginUser.as_view(), name='login'),
    path('register', views.RegisterUser.as_view(), name='register'),
    path('logout', views.logout_user, name='logout'),
    path('customers', views.customers, name='customers'),
    path('customers/<int:user_id>', views.customers, name='customers'),
    ]