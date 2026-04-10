from django.urls import path

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('plans/', views.plan_list, name='plans'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('plans/<int:plan_id>/select/', views.select_plan, name='select_plan'),
]
