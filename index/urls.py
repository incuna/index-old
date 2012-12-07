from django.conf import settings
from django.conf.urls import *
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views import HomeView, IndexCardDetail, LoginError, AuthComplete


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', HomeView.as_view()),
    url(r'^(?P<slug>[\w-]+)/$', IndexCardDetail.as_view(), name='detail'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^complete/(?P<backend>[^/]+)/$', AuthComplete.as_view()),
    url(r'^login-error/$', LoginError.as_view()),
    url(r'', include('social_auth.urls')),
)

urlpatterns += staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

