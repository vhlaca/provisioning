# used djange.test instead of unittest because django.test deletes testing data after
from django.test import TestCase
from ..models import DevVendor, DevModel, Device, DSS, Extension, Customer


class TestModels(TestCase):
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

    def setUp(self):
        # device vendor
        self.vendor = DevVendor.objects.create(name=self.vendor_name)
        # device model
        self.devmodel = DevModel.objects.create(
            name=self.device_model_name, dss=self.device_model_dss, device_format=self.device_model_format)
        # customer
        self.customer = Customer.objects.create(
            description=self.customer_description)
        # extension
        self.extension = Extension.objects.create(
            name=self.extension_name, extension=self.extension_extension, customer=self.customer)
        # device
        self.device = Device.objects.create(
            description=self.device_description, mac=self.device_mac, devmodel=self.devmodel, extension=self.extension)
        # dss
        self.dss1 = DSS.objects.create(
            device=self.device, dssType=self.dss1_type, key=self.dss1_key, value=self.dss1_value, label=self.dss1_label)
        self.dss2 = DSS.objects.create(
            device=self.device, dssType=self.dss2_type, key=self.dss2_key, value=self.dss2_value, label=self.dss2_label)

    def test_creation_device(self):
        self.assertEqual(self.device.description, self.device_description)

    def test_device_extension(self):
        self.assertEqual(self.device.extension.name, self.extension_name)

    def test_device_customer(self):
        self.assertEqual(self.device.getCustomer(),
                         self.customer_description)

    def test_device_dss(self):
        self.assertEqual(self.device.countDSS(), 2)

    def test_device_dev(self):
        self.assertEqual(self.device.devmodel.name, self.device_model_name)

    def tearDown(self):
        # device vendor
        self.vendor = None
        # device model
        self.devmodel = None
        # customer
        self.customer = None
        # extension
        self.extension = None
        # device
        self.device = None
        # dss
        self.dss1 = None
        self.dss2 = None
