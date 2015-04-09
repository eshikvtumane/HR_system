#-*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.generic import View
from django.template import RequestContext

from datetime import datetime
import json

import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from django.contrib.sites.models import get_current_site


# Create your views here.
class EmailConstructorView(View):
    template = 'email_constructor/builder.html'
    def get(self, request):
        args = {}
        args['domain'] = get_current_site(request).domain
        rc = RequestContext(request, args)
        return render_to_response(self.template, rc)


# сохранение изображений на сервер
class SavingImages():
    def savingImage(self, file, dir='tmp', path=settings.MEDIA_URL):
        return self.__save(file, path, dir)

    def savingImages(self, files, dir='tmp', path=settings.MEDIA_URL):
        arr_path = []
        for image in files:
            image_url = self.__save(image, path, dir)
            arr_path.append(image_url)
        return arr_path

    def __save(self, file, path, dir):
        original_name, file_extension = os.path.splitext(file.name)

        filename = original_name + '-' + datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + file_extension

        save_path = default_storage.save(os.path.join(dir, filename), ContentFile(file.read()))
        image_url = os.path.join(path, save_path)
        return image_url


class SavingImageAjax(View, SavingImages):
    def post(self, request):
        if request.is_ajax():
            url = self.savingImage(request.FILES['img'], 'email_images')
            full_url = ''.join(['http://', get_current_site(request).domain, url])
            result = json.dumps(['200', full_url])
            return HttpResponse(result, content_type='application/json')