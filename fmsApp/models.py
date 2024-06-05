from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from cryptography.fernet import Fernet
from django.conf import settings
import base64, os
from django.dispatch import receiver
from PyPDF2 import PdfReader
from django.contrib.auth.models import AbstractUser


# Create your models here.

class File_type(models.Model):
    name = models.CharField(max_length=100, null=True)
    class Meta:
        verbose_name='File type'
        verbose_name_plural='File type'
    def __str__(self):
        return self.name
class Department(models.Model):
    name = models.CharField(max_length=100, null=True)

    class Meta:
        verbose_name='Department'
        verbose_name_plural='Department'

    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    userdepartment = models.ForeignKey(Department, on_delete=models.CASCADE,blank=True, null=True)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department=models.ForeignKey(Department, on_delete=models.CASCADE,blank=True, null=True)
    title = models.CharField(max_length=250)
    file_type=models.ForeignKey(File_type, on_delete=models.CASCADE,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    file_path = models.FileField(upload_to='uploads/',blank=True, null=True)
    pdf_content = models.TextField(blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username + '-' + self.title

    def get_share_url(self):
        fernet = Fernet(settings.ID_ENCRYPTION_KEY)
        value = fernet.encrypt(str(self.pk).encode())
        value = base64.urlsafe_b64encode(value).decode()
        return reverse("share-file-id", kwargs={"id": (value)})
    
    

@receiver(models.signals.post_delete, sender=Post)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.file_path:
        if os.path.isfile(instance.file_path.path):
            os.remove(instance.file_path.path)

@receiver(models.signals.pre_save, sender=Post)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).file_path
    except sender.DoesNotExist:
        return False

    new_file = instance.file_path
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
    