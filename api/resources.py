import binascii
import hashlib

from django.conf.urls import url
from tastypie.http import HttpUnauthorized
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash
import jwt

from api.models import User

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

    def override_urls(self):
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
