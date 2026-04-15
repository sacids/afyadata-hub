from django.contrib import admin
from django.urls import path, include

from django.contrib import admin

admin.site.site_header = "AfyaData Plus Central Registry"
admin.site.site_title = "AfyaData Hub Admin"
admin.site.index_title = "System Management"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("registry.urls")),
    path("api/v1/", include("language.urls")),
]
