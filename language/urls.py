from django.urls import path
from django.urls.resolvers import URLPattern
from .views import LanguageViewSet, LanguageVersionViewSet, language_export, bulk_upload


urlpatterns = [
  
    #Language
    path('admin/languages/<str:code>/export/', language_export, name='language-export'),
    path('admin/languages/bulk-upload/', bulk_upload, name='bulk-upload'),
    
    # Mobile app endpoints (compatible with LanguageManager)
    path('languages/', LanguageViewSet.as_view({'get': 'available'}), name='available-languages'),
    path('translations/<str:code>/', LanguageViewSet.as_view({'get': 'translations'}), name='language-translations'),
    
    

  
]
