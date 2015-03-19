from django.shortcuts import render_to_response
from django.views.generic import View
from django.contrib.auth.forms import AuthenticationForm
from django.template import RequestContext
from django.http import HttpResponseRedirect

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
class LoginView(View):
    template = 'users/login.html'
    def get(self, request):
        return self.render(request)

    def post(self, request):
        user = auth.authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user is not None and user.is_active:
            print 'AUTH'
            auth.login(request, user)
            print 'AUTH'
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