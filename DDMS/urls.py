
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
admin.site.site_header='Digital Document Management System'
admin.site.site_header = "Digital Document Management System"
admin.site.site_title = "Admin"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('fmsApp.urls')),
    path('pdf2text/',include('pdf2text.urls'))
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
