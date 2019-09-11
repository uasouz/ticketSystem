import hashlib

from django.conf.urls import url
from django.forms import model_to_dict
from tastypie.http import HttpUnauthorized
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
import jwt

from api.models import User, Ticket


# Login and Signup


def authenticate(username, uid):
    encoded_jwt = jwt.encode({'user': username, 'userid': uid}, "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
                             algorithm='HS256')
    return encoded_jwt


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        allowed_methods = ['get', 'post']
        resource_name = "user"

    def prepend_urls(self):
        return [
            url(r"login%s" %
                trailing_slash(),
                self.wrap_view('login'), name="api_login"),
            url(r"signup%s" %
                trailing_slash(),
                self.wrap_view('signup'), name="api_signup")
        ]

    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])

        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))

        username = data.get('username', '')
        password = data.get('password', '')

        user = User.objects.filter(username=username)

        if user.exists():
            encoder = hashlib.blake2b()
            encoder.update(password.encode('ascii'))
            hashedpassword = encoder.hexdigest()
            if hashedpassword == user.values()[0].get('password'):
                return self.create_response(request, {
                    'success': True,
                    'token': authenticate(username, 1)
                })
            else:
                return self.create_response(request, {
                    'success': False}, HttpUnauthorized)
        else:
            return self.create_response(request, {
                'success': False}, HttpUnauthorized)

    def signup(self, request, **kwargs):
        self.method_check(request, allowed=['post'])

        data = self.deserialize(request, request.body,
                                format=request.META.get('CONTENT_TYPE', 'application/json'))

        username = data.get('username', '')
        password = data.get('password', '')

        user = User.objects.filter(username=username)

        if user.exists():
            return self.create_response(request, {
                'success': False,
                'error': "username already exists"}, HttpUnauthorized)
        else:
            encoder = hashlib.blake2b()
            encoder.update(password.encode('ascii'))
            hashedpassword = encoder.hexdigest()
            User.objects.create(username=username, password=hashedpassword)
            return self.create_response(request, {
                'success': True
            })


# Tickets


class TicketResource(ModelResource):
    class Meta:
        queryset = Ticket.objects.all()
        allowed_methods = ['get', 'post', 'delete']
        resource_name = "ticket"

    def prepend_urls(self):
        return [
            url(r"ticket/create",
                self.wrap_view('create'), name="api_ticket_create"),
            url(r"ticket/move%s" %
                trailing_slash(),
                self.wrap_view('move'), name="api_ticket_move"),
            url(r"ticket/edit/(?P<ticketId>\d{0,5})$",
                self.wrap_view('edit'), name="api_ticket_edit"),
            url(r"ticket/delete/(?P<ticketId>\d{0,5})$",
                self.wrap_view('delete'), name="api_ticket_delete"),
            url(r"ticket/(?P<ticketId>\d{0,5})",
                self.wrap_view('ticket'), name="api_ticket_read"),
        ]

    def ticket(self, request, ticketId):
        self.method_check(request, allowed=['get'])
        try:
            ticket = Ticket.objects.get(id=ticketId)
            return self.create_response(request, {
                'success': True,
                "ticket": model_to_dict(ticket)
            })
        except Ticket.DoesNotExist:
            return self.create_response(request, {
                'success': False,
                'message': 'Ticket does not exist'
            })

    def create(self, request):
        self.method_check(request, allowed=['post'])

        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))

        name = data.get('name', '')
        description = data.get('description', '')
        board = data.get('board', 0)
        ticket = Ticket.objects.create(name=name, description=description, board=board)
        return self.create_response(request, {
            'success': True,
            "ticket": model_to_dict(ticket)
        })

    def edit(self, request, ticketId):
        self.method_check(request, allowed=['post'])

        data = self.deserialize(request, request.body, format=request.META.get('CONTENT_TYPE', 'application/json'))

        name = data.get('name', '')
        description = data.get('description', '')
        board = data.get('board', 0)

        ticket = Ticket.objects.get(id=ticketId)
        if name != '':
            ticket.name = name
        if description != '':
            ticket.description = description
        if board != '':
            ticket.board = board
        ticket.save()
        return self.create_response(request, {
            'success': True,
            "ticket": model_to_dict(ticket)
        })

    def delete(self, request, ticketId):
        self.method_check(request, allowed=['delete'])
        try:
            ticket = Ticket.objects.get(id=ticketId)
            ticket.delete()
            return self.create_response(request, {
                'success': True,
                "ticket": model_to_dict(ticket),
                'message': 'Ticket deleted'
            })
        except Ticket.DoesNotExist:
            return self.create_response(request, {
                'success': False,
                'message': 'Ticket does not exist'
            })