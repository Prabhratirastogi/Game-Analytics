from django.urls import path
from .views import UploadCSV, QueryData
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('upload-csv/', UploadCSV.as_view(), name='upload-csv'),
    path('query_data/', QueryData.as_view(), name='query_data'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
