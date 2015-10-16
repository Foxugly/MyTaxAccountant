from django.shortcuts import render
from django.http import HttpResponse


def document_view(request, document_id):
    return HttpResponse("document_view")

