from django.urls import path
from . import views 
from .views import dashboard, accounts, services, projects, permissions, assign_permissions, service_form, projects_form, user_form, project_edit, service_edit, project_delete, service_delete, user_update, user_delete , create_user , project_post , project_all , project_pagess , project_alldetails

urlpatterns = [
    path('', views.project_pagess, name='project_pagess'),
    path('login/', views.login_view, name='login_view'),
    path('logout_view/', views.logout_view, name='logout_view'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('accounts/', views.accounts, name='accounts'),
    path('services/', views.services, name='services'),
    path('projects/', views.projects, name='projects'),
    path('permissions/', views.permissions, name='permissions'),
    path('assign_permissions/', views.assign_permissions, name='assign_permissions'),
    path('service_form/', views.service_form, name='service_form'),
    path('projects_form/', views.projects_form, name='projects_form'),
    path('user_form/', views.user_form, name='user_form'),
    path('projects/edit/<int:pk>/', views.project_edit, name='project_edit'),
    path('service/edit/<int:pk>/', views.service_edit, name='service_edit'),
    path('projects/delete/<int:pk>/', views.project_delete, name='project_delete'),
    path('service/delete/<int:pk>/', views.service_delete, name='service_delete'),
    path('user/update/', views.user_update, name='user_update'),
    path('user/delete/', views.user_delete, name='user_delete'),
    path('users/create/', views.create_user, name='create_user'),
    path('project_post/', views.project_post, name='project_post'),
    path('project_post/<int:pk>/', views.project_all, name='project_all'),
    path('project_page/', views.project_pagess, name='project_pagess'),
    path('project_alldetails/<int:pk>/', views.project_alldetails, name='project_alldetails')
]

