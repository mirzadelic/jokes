from django.conf.urls import url, include
from django.contrib import admin
from app.urls import api_urls

# define all api urls in list
apis = [
    url(r'^app/', include(api_urls, namespace="app")),
]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/v1/', include(apis, namespace="api"))  # url for apis
]
