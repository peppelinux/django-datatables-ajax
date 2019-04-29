from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from .datatables import DjangoDatatablesServerProc


@login_required
def StatoUtenzaCorso_DTJson(request):
    model               = StatoUtenzaCorso # this could be also a queryset
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


# other example
class DTD(DjangoDatatablesServerProc):
    def get_queryset(self):
        data_year = self.request.GET.get('created__year') or \
                    self.request.POST.get('created__year') or \
                    datetime.date.today().year
        if self.search_key:
            self.aqs = self.model.filter(created__year=data_year)\
                .filter(\
                Q(code__icontains=self.search_key)      | \
                Q(subject__icontains=self.search_key)      | \
                Q(category__name__icontains=self.search_key)      | \
                Q(created__icontains=self.search_key))
        else:
            self.aqs = self.model.filter(created__year=data_year)

@login_required
def my_ticket_json(request):
    model = Ticket
    columns = _columns
    ticket_list = Ticket.objects.filter(created_by=request.user)
    dtd = DTD( request, ticket_list, columns )
    return JsonResponse(dtd.get_dict())
