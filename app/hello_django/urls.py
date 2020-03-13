from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from upload.views import image_upload, FoodViewSet

router = DefaultRouter()
router.register(r'food', FoodViewSet, basename='food')


urlpatterns = [
    path("", image_upload, name="upload"),
    path("api/", include(router.urls), name="api"),
    path("admin/", admin.site.urls),
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
