from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

urlpatterns = [
    path('', include('chat.urls')),
    path('accounts/login/', LoginView.as_view()),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls)
]
