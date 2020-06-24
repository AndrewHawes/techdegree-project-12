from django.db import models


class Photo(models.Model):
    file = models.ImageField(upload_to='temp-images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
