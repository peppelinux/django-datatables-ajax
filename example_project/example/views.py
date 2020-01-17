from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from django.db.models import Q
from datatables_ajax.datatables import DjangoDatatablesServerProc

from . models import Ticket


_columns = ['code','subject', 'created', 'edited',
            'description', 'get_priority_verbose']

class DTD(DjangoDatatablesServerProc):
    def get_queryset(self):
        if self.search_key:
            self.aqs = self.queryset.filter(
                Q(code__icontains=self.search_key)    | \
                Q(subject__icontains=self.search_key) | \
                Q(created__icontains=self.search_key) | \
                Q(edited__icontains=self.search_key))
        else:
            self.aqs = self.queryset

def get_all_ticket_json(request):
    model = Ticket
    columns = _columns
    ticket_list = model.objects.all()
    dtd = DTD(request=request, queryset=ticket_list, columns=columns)
    return JsonResponse(dtd.get_dict())

@login_required
def my_ticket_json(request):
    model = Ticket
    columns = _columns
    ticket_list = Ticket.objects.filter(created_by=request.user)
    dtd = DTD(request=request, queryset=ticket_list, columns=columns)
    return JsonResponse(dtd.get_dict())
