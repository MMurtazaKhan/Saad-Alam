# urls.py
from django.urls import path
from app.views import UploadImageView, ListUploadedImagesView

urlpatterns = [
    path('upload/', UploadImageView.as_view(), name='upload-image'),
    path('list/', ListUploadedImagesView.as_view(), name='list_images'),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
