# Django Datatables server processing
Lightweight Django class for a full Datatables server processing implementation.

https://datatables.net/examples/data_sources/server_side.html

After hanging around for a good integration of Datatables server processing in Django, I tested the things I found on internet but they all have the same problem, they cannot manage the ForeignKey relations as well. After all, I made it by myself.

This code was tested on Datatables 1.10.+ and Django 1.10.+.

To get it works just put datatables in your html template, like this:

```html
    <!-- jQuery -->
    <script src="/statics/js/vendors/jquery/dist/jquery.min.js"></script>
    <!-- Datatables -->
    <script src="/statics/js/vendors/datatables.net/js/jquery.dataTables.js"></script>
    
    <!-- Datatables -->
    <script>
      $(document).ready(function() {

        $('.datatable-responsive-serverside').DataTable({
        
            "aLengthMenu": [
            [25, 50, 100, 500, ], // -1],
            [25, 50, 100, 500, ] //"All"]
            ],
            "paging": true,
            "responsive": true,
            "processing": true,
            "serverSide": true,
            "ajax": "{% url 'appnamespace:viewname_json' %}",
            // POST METHOD EXAMPLE HERE
            //~ "ajax": {
                  //~ url: "{% url 'appnamespace:viewname_json' %",
                  //~ method: 'post',
                  //~ data: function(args) {
                    //~ return {
                      //~ "args": JSON.stringify(args)
                    //~ };
                  //~ }
                //~ },
        });
        
    });
    </script>
```

Requirements
------------

Download your preferred DataTables release from [here](https://datatables.net/download/).

Setup and examples
------------------
Install package in your Python environment.
````
pip install git+https://github.com/peppelinux/django-datatables-ajax.git
````

Create a view
````
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.http.response import HttpResponseRedirect
from django.http import JsonResponse

from .datatables import DjangoDatatablesServerProc

@login_required
def datatable_data(request):
    radcheck = get_radcheck_active(request)
    radius_accounts = _get_radius_accounts(request, radcheck)
    
    model               = RadiusPostAuth
    columns             = ['pk', 'username', 'reply', 'calling_station_id', 'date']

    base_query = model.objects.filter(username__in=[i.username for i in radius_accounts]).exclude(calling_station_id='').order_by('-date')
    
    class DTD(DjangoDatatablesServerProc):
        def get_queryset(self):
            if self.search_key:
                self.aqs = base_query.filter(
                                        Q(username__icontains=self.search_key) | \
                                        Q(reply__icontains=self.search_key)    | \
                                        Q(calling_station_id__icontains=self.search_key))
            else:
                self.aqs = base_query.filter(username=radcheck.username)
    
    
    dtd = DTD( request, model, columns )
    return JsonResponse(dtd.get_dict())
````

Create an url resource
````
from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required

from .views import *

urlpatterns = [
    url(r'^datatable.json$', login_required(StatoUtenzaCorso_DTJson), name='datatable_json'),
]
````
