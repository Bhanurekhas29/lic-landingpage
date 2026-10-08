from django.conf import settings
from django.conf.urls.static import static
from django.http import FileResponse, Http404
from django.contrib import admin
from django.urls import path, include

def _root_file(filename, content_type):
    """Serve a file kept in the project root (next to manage.py) at the domain root."""
    def view(request):
        path = settings.BASE_DIR / filename
        if not path.is_file():
            raise Http404
        return FileResponse(open(path, 'rb'), content_type=content_type)
    return view


urlpatterns = [
    path('robots.txt', _root_file('robots.txt', 'text/plain; charset=utf-8')),
    path('sitemap.xml', _root_file('sitemap.xml', 'application/xml; charset=utf-8')),
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
