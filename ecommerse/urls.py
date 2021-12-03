from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import  settings
from django.views.generic import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='shop/', permanent=True)),
    path('admin/', admin.site.urls),
    path('shop/', include('shop.urls')),
    path('accounts/', include("accounts.urls")),
    path('cart/', include("cart.urls")),
    path('api/', include("api.urls"))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)