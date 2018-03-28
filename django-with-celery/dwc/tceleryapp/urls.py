from django.conf.urls import url
from tceleryapp.views import TestView

urlpatterns = [
    url('^test/', TestView.as_view())
]