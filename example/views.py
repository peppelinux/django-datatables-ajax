from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from .datatables import DjangoDatatablesServerProc


@login_required
def StatoUtenzaCorso_DTJson(request):
    model               = StatoUtenzaCorso
    columns             = [  'pk', 'cliente', 'corso',  'altro', 
                             'contattato_mediante', 'data_creazione',  'stato' ]

    class DTD(DjangoDatatablesServerProc):
        def get_queryset(self):
            if self.search_key:
                self.aqs = self.model.objects.filter( 
                    Q(cliente__nome__icontains=self.search_key)       | \
                    Q(cliente__cognome__icontains=self.search_key)    | \
                    Q(cliente__nominativo__icontains=self.search_key) | \
                    Q(corso__nome__istartswith=self.search_key)       | \
                    Q(contattato_mediante__nome__istartswith=self.search_key) | \
                    Q(altro__nome__istartswith=self.search_key)    \
                    )
            else:
                self.aqs = self.model.objects.all()
    
    
    dtd = DTD( request, model, columns )
    return JsonResponse(dtd.get_dict())
