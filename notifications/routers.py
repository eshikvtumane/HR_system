from swampdragon import route_handler
from swampdragon.route_handler import ModelPubRouter,BaseRouter, ModelRouter
from .models import Notification
from .serializers import NotificationSerializer


class NotificationRouter(ModelPubRouter):
    valid_verbs = ['subscribe']
    route_name = 'notifications'
    model = Notification
    serializer_class = NotificationSerializer



class TestRouter(ModelRouter):
    route_name = 'test_notifications'
    model = Notification
    serializer_class = NotificationSerializer

    def get_object(self, **kwargs):
        return self.model.objects.get(pk=kwargs['id'])

    def get_query_set(self, **kwargs):
        return self.model.objects.all().order_by('-pk')[:3]

route_handler.register(NotificationRouter)
route_handler.register(TestRouter)