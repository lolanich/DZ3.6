from django.contrib import admin
from django.urls import path, include

urlpatterns = [
   path('admin/', admin.site.urls),
   path('pages/', include('django.contrib.flatpages.urls')),
   path('news/', include('NewsApp.urls')),
   path('', include('protect.urls')),
   path('sign/', include('sign.urls')),
   path('accounts/', include('allauth.urls')),
]
