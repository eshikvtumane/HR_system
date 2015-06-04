from django.shortcuts import render
from django.views.generic import ListView
from .models import Notification

# Create your views here.

class Notifications(ListView):
    model = Notification
    template_name ='notifications/notifications_view.html'

    def get_queryset(self):
        return self.model.objects.order_by('-pk')[:5]
