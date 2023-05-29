
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


admin.site.site_header = 'CRVWWDA'
admin.site.index_title = 'CENTRAL RIFT VALLEY WATER WORKS DEVELOPMENT AGENCY'



urlpatterns = [
    path("", include('main.urls')),
    path("", include('applicants.urls')),
    path('tinymce/', include('tinymce.urls')),
    path('admin/', admin.site.urls),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
