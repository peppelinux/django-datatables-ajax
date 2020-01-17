import json
import logging

from django.apps import apps
from django.conf import settings
from django.test import Client, TestCase

from . models import Ticket


logger = logging.getLogger('my_logger')

class BaseTest(TestCase):

    def setUp(self):
        self.ticket_1 = Ticket.objects.create(code="code1",
                                              subject="subject 1",
                                              created="2020-01-01 12:12:00",
                                              edited="2020-01-01",
                                              description="descr 1",
                                              priority="1")

    def test_tickets(self):
        logger.info(self.ticket_1)
        assert self.ticket_1

    def test_datatables_getalltickets_post(self):
        c = Client()
        p = {"draw":1,
             "order":[{"column":0,"dir":"asc"}],
             "start":0,
             "length":10,
             "search":{"value":"","regex":False}
            }
        args = json.dumps(p)
        response = c.post('/all_ticket.json', {"args": args})
        response_string = response.content.decode("utf-8")
        response_json = json.loads(response_string)
        data = response_json['data']
        logger.info(data)
        assert data

    def test_datatables_getalltickets_get(self):
        c = Client()
        p = {"draw":1,
             "order[0][column]":1,
             "order[0][dir]":"asc",
             "start":0,
             "length":10,
             "search[value]":"subject 1",
             "regex":False
            }
        args = json.dumps(p)
        response = c.get('/all_ticket.json', p)
        response_string = response.content.decode("utf-8")
        response_json = json.loads(response_string)
        data = response_json['data']
        logger.info(data)
        assert data

    def test_datatables_search_valid(self):
        c = Client()
        p = {"draw":1,
             "order":[{"column":1,"dir":"asc"}],
             "start":0,
             "length":-1, # all the records
             "search":{"value":"subject 1","regex":False}
            }
        args = json.dumps(p)
        response = c.post('/all_ticket.json', {"args": args})
        response_string = response.content.decode("utf-8")
        response_json = json.loads(response_string)
        data = response_json['data']
        logger.info(data)
        assert data

    def test_datatables_search_invalid(self):
        c = Client()
        p = {"draw":1,
             "order":[{"column":0,"dir":"asc"}],
             "start":0,
             "length":10,
             "search":{"value":"subject 10","regex":False}
            }
        args = json.dumps(p)
        response = c.post('/all_ticket.json', {"args": args})
        response_string = response.content.decode("utf-8")
        response_json = json.loads(response_string)
        data = response_json['data']
        logger.info(response_json['data'])
        self.assertFalse(data)
