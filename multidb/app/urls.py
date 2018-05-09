from django.urls import path, include
from .views import *

urlpatterns = [
    path('person', PersionView.as_view())
]