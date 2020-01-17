import datetime
import json

from abc import abstractmethod

from django.conf import settings
from django.utils import timezone

from . settings import *


class DjangoDatatablesServerProc(object):
    def __init__(self, request, queryset, columns):
        """
        model    = StatoUtenzaCorso
        columns  = ['pk', 'cliente', 'corso',  'altro',
                    'contattato_mediante', 'data_creazione', 'stato']
        """
        self.columns = columns
        # self.model  = model.objects if hasattr(model, 'objects') else model
        self.queryset  = queryset
        self.request = request
        self.method = 'POST' if request.POST.get('args') else 'GET'
        if self.method == 'POST':
            r = json.loads(request.POST.get('args'))
        else:
            r = dict(request.GET)

        self.dt_ajax_request = r
        # queryset attributes
        self.aqs = None
        self.fqs = None
        # response object will be similar to this, but with datas!
        # Since DataTables never sends draw as 0, it should never be
        # returned as 0 (assuming that was the issue). As the documentation
        # says, it should be returned as the same value that was sent
        # (cast as an integer)

        if self.method == 'GET':
            self.d = {'draw': int(self.dt_ajax_request['draw'][0]),
                      'recordsTotal': 0,
                      'recordsFiltered': 0,
                      'data': []}
            self.lenght = self.dt_ajax_request['length']
            self.start  = self.dt_ajax_request['start']
            self.search_key = self.dt_ajax_request['search[value]']
            self.order_col = self.dt_ajax_request['order[0][column]']
            self.order_dir = self.dt_ajax_request['order[0][dir]']
        else:
            # request.POST
            self.d = {'draw': int(self.dt_ajax_request['draw']),
                      'recordsTotal': 0,
                      'recordsFiltered': 0,
                      'data': []}
            self.lenght = self.dt_ajax_request['length']
            self.start  = self.dt_ajax_request['start']
            self.search_key = self.dt_ajax_request['search']['value']
            self.order_col = self.dt_ajax_request['order'][0]['column']
            self.order_dir = self.dt_ajax_request['order'][0]['dir']

        # casting
        for field in ['lenght', 'start', 'search_key',
                      'order_col', 'order_dir']:
            attr = getattr(self, field)
            if isinstance(attr, list):
                setattr(self, field, attr[0])
            else:
                setattr(self, field, attr)

            if isinstance(attr, int): continue
            if getattr(self, field).isdigit():
                v = getattr(self, field)
                setattr(self, field, int(v))

    @abstractmethod
    def get_queryset(self):
        """
           Overload me in your DjangoDatatablesServerProc' inherited class!
           The query must be customized to get it work

           Example data:
               if self.search_key:
                    self.aqs = self.model.objects.filter(
                        Q(cliente__nome__icontains=self.search_key)       | \
                        Q(cliente__cognome__icontains=self.search_key)    | \
                        Q(cliente__nominativo__icontains=self.search_key) | \
                        Q(corso__nome__istartswith=self.search_key)       | \
                        Q(contattato_mediante__nome__istartswith=self.search_key) | \
                        Q(altro__nome__istartswith=self.search_key))
                else:
                    self.aqs = self.model.objects.all()
        """
        pass

    def get_ordering(self):
        """
           overload me if you need different ordering approach
        """
        if not self.aqs:
            self.get_queryset()

        # if lenght is -1 means ALL the records, sliceless
        if self.lenght == -1:
            self.lenght = self.aqs.count()

        # fare ordinamento qui
        # 'order[0][column]': ['2'],
        # bisogna mappare la colonna con il numero di sequenza eppoi
        # fare order_by
        if self.order_col:
            self.col_name = self.columns[self.order_col]
            if self.order_dir == 'asc':
                self.aqs = self.aqs.order_by(self.col_name)
            else:
                self.aqs = self.aqs.order_by('-'+self.col_name)

    def get_paging(self):
        # paging requirement
        self.get_ordering()
        self.fqs = self.aqs[self.start:self.start+self.lenght]

    def _make_aware(self, dt):
        if hasattr(dt, 'tzinfo'):
            if dt.tzinfo != timezone.get_default_timezone():
                return dt.astimezone(timezone.get_default_timezone())
            else:
                return dt
        return timezone.make_aware(dt, timezone=timezone.get_current_timezone())

    def _dt_strftime_as_naive(self, dt):
        """ todo """
        pass

    def fill_data(self):
        """
        overload me if you need some clean up
        """
        if not self.fqs:
            self.get_paging()

        for r in self.fqs:
            cleaned_data = []
            for e in self.columns:
                # this avoid null json value
                v = getattr(r, e)
                if v:
                    if isinstance(v, datetime.datetime):
                        default_datetime_format = DEFAULT_DATETIME_FORMAT
                        if hasattr(settings, 'DEFAULT_DATETIME_FORMAT'):
                            default_datetime_format = settings.DEFAULT_DATETIME_FORMAT
                        vrepr = self._make_aware(v).strftime(default_datetime_format)
                    elif isinstance(v, datetime.date):
                        default_date_format = DEFAULT_DATE_FORMAT
                        if hasattr(settings, 'DEFAULT_DATE_FORMAT'):
                            default_date_format = settings.DEFAULT_DATE_FORMAT
                        vrepr = v.strftime(default_date_format)
                    elif callable(v):
                        vrepr = str(v())
                    else:
                        vrepr = v.__str__()
                else:
                    vrepr = ''
                cleaned_data.append(vrepr)

            self.d['data'].append( cleaned_data )
        self.d['recordsTotal'] = self.queryset.count()
        self.d['recordsFiltered'] = self.aqs.count()

    def get_dict(self):
        if not self.d['data']:
            self.fill_data()
        return self.d
