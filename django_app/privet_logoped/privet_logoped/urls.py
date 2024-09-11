from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path

from api.urls import urlpatterns as api_urlpatterns

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(api_urlpatterns)),
]


admin.site.site_url = None
admin.site.index_title = "Администрирование"
admin.site.site_title = "Привет-логопед"
admin.site.site_header = "Меню администратора"
