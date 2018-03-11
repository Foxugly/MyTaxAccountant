# encoding: utf-8
#
# Copyright 2015, Foxugly. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.

import json

from django.http import HttpResponse
from django.views.generic import CreateView, DeleteView, ListView
from fileupload.models import FileUpload
from fileupload.response import JSONResponse, response_mimetype
from fileupload.serialize import serialize


class FileUploadCreateView(CreateView):
    model = FileUpload
    fields = "__all__"

    def form_valid(self, form):
        self.object = form.save()
        files = [serialize(self.object)]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response

    def form_invalid(self, form):
        data = json.dumps(form.errors)
        return HttpResponse(content=data, status=400, content_type='application/json')


class FileUploadDeleteView(DeleteView):
    model = FileUpload

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        response = JSONResponse(True, mimetype=response_mimetype(request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


class FileUploadListView(ListView):
    model = FileUpload

    def render_to_response(self, context, **response_kwargs):
        files = [serialize(p) for p in self.get_queryset()]
        data = {'files': files}
        response = JSONResponse(data, mimetype=response_mimetype(self.request))
        response['Content-Disposition'] = 'inline; filename=files.json'
        return response


def remove_upload(request, fileupload_id):
    if request.is_ajax():
        f = FileUpload.objects.get(id=fileupload_id)
        f.delete()
        results = {'return': 'OK'}
        return HttpResponse(json.dumps(results))
