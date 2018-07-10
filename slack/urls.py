from django.conf.urls import url
from django.contrib import admin
from standupbot import views
from standupbot.views import Events

urlpatterns = [
    url('^$', views.health_check),
    url('^send_standup/', views.send_first_question_to_all_users),
    url('^send_reminder/', views.send_standup_reminder),
    url(r'^admin/', admin.site.urls),
    url(r'^standupbot/', Events.as_view())
]
