from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dashboard import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),
    path('get_menus/', views.get_menus, name='get_menus'),
    path('account/', include('account.urls')),
    path('medicine/', include('medicine.urls')),
    path('store/', include('store.urls')),
    path('doctor/', include('doctor.urls')),
    path('patient/', include('patient.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
