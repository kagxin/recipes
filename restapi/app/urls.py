from django.urls import path, include
from app import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path(r'snippet/', views.SnippetList.as_view()),
    path(r'snippet/<int:pk>/', views.SnippetDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

urlpatterns += [
    path(r'auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    path(r'login/', views.Login.as_view()),
    path(r'logout/', views.Logout.as_view())
]