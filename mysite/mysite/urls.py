from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static,settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('motoshop.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('chaining/', include('smart_selects.urls')),
    path('select2/', include('django_select2.urls')),
] + (static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
