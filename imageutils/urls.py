from django.urls import path

from imageutils import ajax

app_name = 'imageutils'
urlpatterns = [
    path('imageutils/save_image/', ajax.save_image, name='save_image'),
    path('imageutils/upload_avatar/', ajax.upload_avatar, name='upload_avatar'),
]
