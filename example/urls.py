from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required

from . views import *

app_name="example"

urlpatterns = [
    url(r'^all_ticket.json$', get_all_ticket_json, name='get_all_ticket_json'),
]
