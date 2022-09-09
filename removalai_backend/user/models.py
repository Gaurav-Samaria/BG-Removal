from django.db import models
from django.contrib.auth.models import User

class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.FileField(upload_to="media/")
    

class UserTransaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=20)
    created_date = models.DateTimeField(auto_now=True)
    uploads_till_now = models.IntegerField(default=0)


class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    images_used = models.IntegerField(default=0)
    images_left = models.IntegerField(default=100)


class Updated_image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_image = models.CharField(max_length=400)