from django.urls import path
from .views import IndexView

urlpatterns = [
    path(r'', IndexView.as_view(), name='home_page'),
]
