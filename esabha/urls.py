from django.contrib import admin
from django.urls import path
from django.urls import include
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from esabha import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('registration.backends.default.urls')),
    path('social/', include('social.urls')),
    path('', RedirectView.as_view(url="social/")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
