from django.contrib import admin
from .models import Post,File_type,Department,UserProfile

# Register your models here.
admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(File_type)
admin.site.register(Department)

