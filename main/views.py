from django.shortcuts import render, render_to_response
from  django.views.generic import View

# Create your views here.
class MainPageView(View):
    template = 'main.html'
    def get(self, request):
        return render_to_response(self.template)