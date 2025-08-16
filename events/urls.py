from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Auth
    path('signup/', views.signup_view, name='signup'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('post-login-redirect/', views.post_login_redirect, name='post_login_redirect'),

    # Dashboards
    path('', views.home_redirect, name='home'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/organizer/', views.organizer_dashboard, name='organizer_dashboard'),
    path('dashboard/participant/', views.participant_dashboard, name='participant_dashboard'),

    # Events & Categories CRUD (RBAC enforced inside views)
    path('events/', views.event_list, name='event_list'),
    path('events/add/', views.event_create, name='event_add'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('events/<int:pk>/edit/', views.event_update, name='event_edit'),
    path('events/<int:pk>/delete/', views.event_delete, name='event_delete'),

    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.category_create, name='category_add'),
    path('categories/<int:pk>/edit/', views.category_update, name='category_edit'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),

    # RSVP
    path('events/<int:pk>/rsvp/', views.rsvp_event, name='rsvp_event'),
    path('my-rsvps/', views.my_rsvps, name='my_rsvps'),
]
