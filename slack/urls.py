from django.conf.urls import url
from django.contrib import admin
from standupbot.views import Events

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^standupbot/', Events.as_view())
]
