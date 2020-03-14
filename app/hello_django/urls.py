from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from upload.views import image_upload, \
    FoodViewSet, \
    notify_user_about_missing_expiry_date, \
    ExpiryDate, \
    SetExpiryDate


router = DefaultRouter()
router.register(r'food', FoodViewSet, basename='food')


urlpatterns = [
    path("", image_upload, name="upload"),
    path("api/", include(router.urls), name="api"),
    path("api/notify/", notify_user_about_missing_expiry_date, name="notify_user"),
    path("api/expiry/", ExpiryDate.as_view(), name="expiry_date_queue"),
    path("api/set-expiry/", SetExpiryDate.as_view(), name="set_expiry_date"),
    path("admin/", admin.site.urls),
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
