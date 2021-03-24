from .models import DevVendor, DevModel, Device, DSS, Extension, Customer
from .forms import PresentXMLData
from django.views.generic.edit import FormView
from rest_framework import viewsets
from rest_framework import permissions
from django.utils.safestring import mark_safe
from .serializers import DevVendorSerializer, DevModelSerializer, DeviceSerializer, CustomerSerializer, ExtensionSerializer, DSSSerializer
from django.http import request, HttpRequest, HttpResponse
from .endpoints import GetXMLConfig
import logging


class PresentXMLDataView(FormView):
    """
    PresentXMLDataView is form view to represent XML data in text mode (ready to copy & paste)
    It collect device id from URL (format "../form/{id}).
    """
    form_class = PresentXMLData
    template_name = 'admin/base_site.html'

    def get(self, request, *args, **kwargs):
        data = GetXMLConfig(kwargs['id'])
        return HttpResponse(data, content_type='text')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Present XML configuration data'
        context['content'] = mark_safe("<text>GetXMLConfig</text>")
        context['has_permission'] = True

        return context


class DevVendorViewSet(viewsets.ModelViewSet):
    """View set for Device vendor REST API"""
    queryset = DevVendor.objects.all()
    serializer_class = DevVendorSerializer


class DevModelViewSet(viewsets.ModelViewSet):
    """View set for Device model REST API"""
    queryset = DevModel.objects.all()
    serializer_class = DevModelSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    """View set for Customer REST API"""
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class ExtensionViewSet(viewsets.ModelViewSet):
    """View set for Extension REST API"""
    queryset = Extension.objects.all()
    serializer_class = ExtensionSerializer


class DSSViewSet(viewsets.ModelViewSet):
    """View set for DSS REST API"""
    queryset = DSS.objects.all()
    serializer_class = DSSSerializer


class DeviceViewSet(viewsets.ModelViewSet):
    """View set for Device REST API"""
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
