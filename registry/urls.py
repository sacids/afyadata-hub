from django.urls import path
from .views import ProjectDiscoveryView, RegisterProjectView

urlpatterns = [
    path('projects/discover/', ProjectDiscoveryView.as_view(), name='project-discovery'),
    path('projects/register/', RegisterProjectView.as_view(), name='project-registration'),
]