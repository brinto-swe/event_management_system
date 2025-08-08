from django.contrib import admin
from django.urls import path, include
from events.views import dashboard
# from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('admin/', admin.site.urls),
    path("events/",  include("events.urls"))
]
# + debug_toolbar_urls()