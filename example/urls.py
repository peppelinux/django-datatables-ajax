from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required

from .views import *

urlpatterns = [
    url(r'^datatable.json$', login_required(StatoUtenzaCorso_DTJson), name='datatable_json'),
]
