# encoding: utf-8
from django.conf.urls import patterns, url
from fileupload.views import FileUploadCreateView, FileUploadDeleteView, FileUploadListView


urlpatterns = patterns('',
    url(r'^basic/$', FileUploadCreateView.as_view(), name='upload-basic'),
    url(r'^new/$', FileUploadCreateView.as_view(), name='upload-new'),
    url(r'^delete/(?P<pk>\d+)$', FileUploadDeleteView.as_view(), name='upload-delete'),
    url(r'^view/$', FileUploadListView.as_view(), name='upload-view'),
)
