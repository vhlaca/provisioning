from django.test import TestCase, Client
from django.urls import reverse
from ..models import Device
from ..views import ExtensionViewSet
from rest_framework.test import APIRequestFactory, APIClient


class TestStatusViews(TestCase):
    client = Client()
    # vendor
    vendor_name = "The vendor"
    # device model
    device_model_name = "Phone set xyz"
    device_model_dss = True
    device_model_format = "Hardware IP telephone"
    # customer
    customer_description = "Beloved Customer XYZ"
    # extension
    extension_name = "This is the extension"
    extension_extension = 1234
    # device
    device_description = "This is the phone that rings and then people speak"
    device_mac = "AA-CC-DD-DD-E1-00"
    # DSS
    dss1_type = 'BLF - Busy Lamp Field'
    dss2_type = 'SPD - Speed dial key'
    dss1_key = 1
    dss2_key = 2
    dss1_value = "442"
    dss2_value = "098XXYYZZ"
    dss1_label = "My boss"
    dss2_label = "Wife"

    def test_device_list(self):
        response = self.client.get('/api/device/')
        self.assertEqual(response.status_code, 200)

    def test_dds_list(self):
        response = self.client.get('/api/dss/')
        self.assertEqual(response.status_code, 200)

    def test_vendor_list(self):
        response = self.client.get('/api/devvendor/')
        self.assertEqual(response.status_code, 200)

    def test_model_list(self):
        response = self.client.get('/api/devmodel/')
        self.assertEqual(response.status_code, 200)

    def test_customer_list(self):
        response = self.client.get('/api/customer/')
        self.assertEqual(response.status_code, 200)

    def test_ext_list(self):
        response = self.client.get('/api/extension/')
        self.assertEqual(response.status_code, 200)

    def test_xml_list(self):
        response = self.client.get(
            reverse('xmldata', kwargs={'id': 1}))
        self.assertEqual(response.status_code, 200)
