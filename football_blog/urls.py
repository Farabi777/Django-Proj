from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('users/', include('users.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # Добавление путей для логина/выхода
    path('', RedirectView.as_view(url='/blog/', permanent=True)),
    path('', RedirectView.as_view(url='/users/', permanent=True)),
]

# Настройка для медиа-файлов
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
