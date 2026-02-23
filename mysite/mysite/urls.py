from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static,settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('motoshop.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('tinymce/', include('tinymce.urls')),
] + (static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
