from django.contrib import admin
from .models import Image, UserTransaction, UserData, Updated_image
# Register your models here.

admin.site.register(Image)
admin.site.register(Updated_image)
admin.site.register(UserTransaction)
admin.site.register(UserData)