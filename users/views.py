#-*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.views.generic import View
from django.contrib.auth.forms import AuthenticationForm
from django.template import RequestContext
from django.http import HttpResponseRedirect

from django.contrib import auth
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordResetForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
class LoginView(View):
    template = 'users/login.html'
    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        return self.render(request)



    def post(self, request):
        user = auth.authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect('/')

        return self.render(request)

    def render(self, request):
        args = {}
        args['auth_form'] = AuthenticationForm(None, request.POST or None)
        rc = RequestContext(request, args)
        return render_to_response(self.template, rc)

class LogoutView(View):
    @method_decorator(login_required)
    def get(self, request):
        auth.logout(request)
        return HttpResponseRedirect('/')

# изменение пароля
class PasswordChangeView(View):
    template = 'users/change_password.html'

    @method_decorator(login_required)
    def get(self, request):
        args = {}
        args['change_password_form'] = AdminPasswordChangeForm(request.user)
        rc = RequestContext(request, args)
        return render_to_response(self.template, rc)

    @method_decorator(login_required)
    def post(self, request):
        print 'ttt'
        args = {}
        form = AdminPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            auth.update_session_auth_hash(request, form.user)

        args['change_password_form']=form
        rc = RequestContext(request, args)
        return render_to_response(self.template, rc)

# восстановление пароля
class PasswordResetView(View):
    template = 'users/password_reset.html'
    def get(self, request):
        args = {}
        args['reset_password_form'] = PasswordResetForm(request.user)
        rc = RequestContext(request, args)
        return render_to_response(self.template, rc)
