from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),  # Главная страница
    path('docs/', include('documents.urls')),   # Документы
    path('blog/', include('blog.urls')),   # Блог
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'pages.views.page_not_found'
handler500 = 'pages.views.server_error'
