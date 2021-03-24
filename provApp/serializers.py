"""
This functionality of serializers is available:

CRUD tested with postman
C
ADD A RECORD: 
method POST;
http://localhost:8000/api/devvendor/
form-data
- name = "Value"

R
GET ALL RECORDS: method GET; http://localhost:8000/api/devvendor/
GET SPECIFIC RECORD: method GET; http://localhost:8000/api/devvendor/10/

U
UPDATE A RECORD: 
method PUT;
http://localhost:8000/api/devvendor/13/
form-data
- name = "Value"

UPDATE A RECORD WITHOUT PROVIDING ALL THE REQUIRED FIELDS:
method PATCH;
http://localhost:8000/api/extension/11/
form-data
- name = "new value"

D
DELETE A RECORD:
method DELETE;
http://localhost:8000/api/devvendor/13/

"""

from .models import DevVendor, DevModel, Device, DSS, Extension, Customer
from rest_framework import serializers


class DevVendorSerializer(serializers.ModelSerializer):
    """
    Device vendor serializer. Includes following fields:
    - 'id'
    - 'name'
    """
    class Meta:
        model = DevVendor
        fields = ('id', 'name', )


class DevModelSerializer(serializers.ModelSerializer):
    """
    Device model serializer. Includes following fields:
    - 'id'
    - 'name'
    - 'dss'
    - 'device_format'
    """
    class Meta:
        model = DevModel
        fields = ('id', 'name', 'dss', 'device_format')


class CustomerSerializer(serializers.ModelSerializer):
    """
    Customer serializer. Includes following fields:
    - 'id'
    - 'description'
    """
    class Meta:
        model = Customer
        fields = ('id', 'description', )


class ExtensionSerializer(serializers.ModelSerializer):
    """
    Extension serializer. Includes following fields:
    - 'id'
    - 'name'
    - 'extension'
    - 'customer'
    """
    class Meta:
        model = Extension
        fields = ('id', 'name', 'extension', 'customer')


class DSSSerializer(serializers.ModelSerializer):
    """
    DSS serializer. Includes following fields:
    - 'id'
    - 'device'
    - 'dssType'
    - 'key'
    - 'value'
    - 'label'
    """
    class Meta:
        model = DSS
        fields = ('id', 'device', 'dssType', 'key', 'value', 'label')


class DeviceSerializer(serializers.ModelSerializer):
    """
    Device serializer. Includes following fields:
    - 'id'
    - 'description'
    - 'devmodel'
    - 'mac'
    - 'extension'
    - 'getDSS'
    - 'countDSS'
    - 'getExtension'
    - 'getCustomer'
    """
    class Meta:
        model = Device
        fields = ('id', 'description', 'devmodel', 'mac',
                  'extension', 'getDSSJSON', 'countDSS', 'getExtensionJSON', 'getCustomerJSON')
