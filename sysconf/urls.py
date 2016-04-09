from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = patterns('',
    url(r'^admin/', include('dashboard.urls')),
)

urlpatterns += patterns('',
    url(r'^api/', include('dashboard.urls')),
)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
