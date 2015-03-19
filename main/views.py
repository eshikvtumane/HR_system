from django.shortcuts import render, render_to_response
from  django.views.generic import View

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
class MainPageView(View):
    template = 'main/main.html'

    @method_decorator(login_required)
    def get(self, request):
        return render_to_response(self.template)

