from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import (
    EventListView, EventDetailView, EventCreateView, EventUpdateView, EventDeleteView,
    RSVPCreateView, MyEventsView,
    UserProfileView, UserProfileUpdateView,
    CustomPasswordChangeView, CustomPasswordChangeDoneView,
    CustomPasswordResetView, CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView, CustomPasswordResetCompleteView,
    signup_view, activate_account, post_login_redirect, home_redirect,
    admin_dashboard, organizer_dashboard, participant_dashboard,
    category_create, category_delete, category_update, category_list
)

urlpatterns = [
    # Home / Event list
    path('', home_redirect, name='home'),
    path('events/', EventListView.as_view(), name='event_list'),

    # Event CRUD
    path('event/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('event/create/', EventCreateView.as_view(), name='event_create'),
    path('event/<int:pk>/update/', EventUpdateView.as_view(), name='event_update'),
    path('event/<int:pk>/delete/', EventDeleteView.as_view(), name='event_delete'),

    # Categories CRUD (FBV)
    path('categories/', category_list, name='category_list'),
    path('categories/add/', category_create, name='category_add'),
    path('categories/<int:pk>/edit/', category_update, name='category_edit'),
    path('categories/<int:pk>/delete/', category_delete, name='category_delete'),

    # RSVP
    path('event/<int:pk>/rsvp/', RSVPCreateView.as_view(), name='event_rsvp'),
    path('my-events/', MyEventsView.as_view(), name='my_events'),

    # User Auth
    path('signup/', signup_view, name='signup'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate'),
    path('login/', LoginView.as_view(template_name="registration/login.html"), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('post-login-redirect/', post_login_redirect, name='post_login_redirect'),

    # Profile
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/edit/', UserProfileUpdateView.as_view(), name='edit_profile'),

    # Password Management
    path('password/change/', CustomPasswordChangeView.as_view(), name='password_change'),
    path('password/change/done/', CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password/reset/', CustomPasswordResetView.as_view(template_name ="registration/password_reset.html"), name='password_reset'),
    path('password/reset/done/', CustomPasswordResetDoneView.as_view(template_name ="registration/password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(template_name ="registration/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(template_name ="registration/password_reset_complete.html"), name='password_reset_complete'),

    # Dashboards
    path('dashboard/admin/', admin_dashboard, name='admin_dashboard'),
    path('dashboard/organizer/', organizer_dashboard, name='organizer_dashboard'),
    path('dashboard/participant/', participant_dashboard, name='participant_dashboard'),
]
