from django.db import models
from django.utils import timezone
import xml.etree.ElementTree as et
from xml.dom import minidom
import json


class DevVendor(models.Model):
    """
    Vendors model class

    Fields:
    name - char length 255, required (not null and not blank)

    __str__: 30 chars of name field for easier display on forms

    Verbose name: Device vendor
    """
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.name[0:30]

    class Meta:
        verbose_name = "Device vendor"


class DevModel(models.Model):
    """
    Device model class

    Fields:
    name - char length 255, required (not null and not blank), verbose_name = "Device model"
    dss - boolean - can the device have DSS keys
    device_format - text length 255, choices enumeration:
    SOFTPHONE = 'Software telephone' (default value)
    HARDPHONE = 'Hardware IP telephone'

    __str__: 30 chars of name field for easier display on forms

    Verbose name: Device model
    """
    class deviceFormat(models.TextChoices):
        """Choices class for Device format in Device model"""
        SOFTPHONE = 'Software telephone'
        HARDPHONE = 'Hardware IP telephone'

    name = models.CharField(max_length=255, null=False,
                            blank=False, verbose_name="Device model")
    dss = models.BooleanField(default=False)
    device_format = models.TextField(
        max_length=255, choices=deviceFormat.choices, default=deviceFormat.SOFTPHONE)

    def __str__(self):
        return self.name[0:30]

    class Meta:
        verbose_name = "Device model"


class Device(models.Model):
    """
    Device class

    Fields:
    description - char length 255, required (not null and not blank)
    mac - char length 17, unique, required (not null and not blank), verbose_name = "MAC"
    devmodel - foreignkey - device models, on delete - cascade, verbose_name = "Device model" 
    cfg_last_update - Datetime - time when the XML configuration was downloaded last time verbose_name = 'Last config update'
    extension - One to one field to Extension. An extension can have only one customer therefore, a device can have  only one customer due to this one to one relationship

    __str__: 30 chars of description field for easier display on forms

    Verbose name: Device
    """
    description = models.CharField(max_length=255, null=False, blank=False)
    mac = models.CharField(max_length=17, unique=True,
                           null=False, blank=False, verbose_name="MAC")
    devmodel = models.ForeignKey(
        'DevModel', on_delete=models.CASCADE, verbose_name='Device Model')
    cfg_last_update = models.DateTimeField(
        null=True, blank=True, verbose_name='Last config update')

    extension = models.OneToOneField(
        'Extension', on_delete=models.CASCADE)

    def getDSS(self):
        """The method returns list of configured DSS of the device"""
        dss = DSS.objects.filter(device_id=self.id)
        return dss

    def getDSSJSON(self):
        """The method returns list of configured DSS of the device in JSON format"""
        tempDSS = []
        if self.countDSS() > 0:
            dss = self.getDSS()
            for d in dss:
                tempDSS.append({"id": d.id,
                                "dssType": d.dssType,
                                "key": d.key,
                                "value": d.value,
                                "label": d.label,
                                "device_id": d.device_id})
        return json.dumps(tempDSS)

    def countDSS(self):
        """
        The method returns number of configured DSS. 

        Short description - Number of CSS connect to the device
        """
        return self.getDSS().count()
    countDSS.short_description = "Number of CSS connect to the device"

    def getExtension(self):
        """The method returns the extension related to the device"""
        return Extension.objects.filter(id=self.extension.id)[0]

    def getExtensionJSON(self):
        """The method returns the extension related to the device in JSON format"""
        result = []
        ext = self.getExtension()
        result.append({"id": ext.id, "extension": ext.extension,
                       "name": ext.name})
        return result
    getExtensionJSON.short_description = "Extension"

    def getCustomer(self):
        """The method returns the customer related to the device"""
        # exten =
        return self.getExtension().customer.description

    def getCustomerJSON(self):
        """The method returns the customer related to the device in JSON format"""
        result = []
        exten = self.getExtension()
        result.append(
            {"id": exten.customer.id, "description": exten.customer.description})
        return result
    getCustomerJSON.short_description = "Customer"

    def XMLConfig(self):
        """
        The method returns XML configuration which contains elements:
        - customer
        - extension
        - description
        - MAC address
        - DSS if there are any related to the device
        """
        exten = self.getExtension().name

        cust = self.getCustomer()

        root = et.Element("settings")

        phoneSettings = et.Element("phone-settings")
        root.append(phoneSettings)

        customer = et.SubElement(phoneSettings, "Customer")
        customer.text = cust

        extension = et.SubElement(phoneSettings, "Extension")
        extension.text = exten

        description = et.SubElement(phoneSettings, "description")
        description.text = self.description

        mac = et.SubElement(phoneSettings, "mac")
        mac.text = self.mac

        if(self.countDSS() > 0):

            allDSS = self.getDSS()
            dsss = et.Element("dss")
            phoneSettings.append(dsss)
            for dss in allDSS:
                et.SubElement(dsss, "value.{key} = " + dss.value)
                et.SubElement(dsss, "label.{key} = " + dss.label)
                et.SubElement(dsss, "type.{key} = " + dss.dssType[0:3])

        tree = et.ElementTree(root)

        return et.tostring(tree.getroot(), encoding='utf8')

    XMLConfig.short_description = "XML configuration"

    def friendlyTimeDiff(self):
        """The method returns friendl form of the time difference between now and recorded cfg_last_update time"""
        if self.cfg_last_update is not None:
            now = timezone.now()
            diff = now - self.cfg_last_update
            second_diff = diff.seconds
            day_diff = diff.days

            if day_diff < 0:
                return ''

            if day_diff == 0:
                if second_diff < 10:
                    return "just now"
                if second_diff < 60:
                    return str(int(second_diff)) + " seconds ago"
                if second_diff < 120:
                    return "a minute ago"
                if second_diff < 3600:
                    return str(int(second_diff / 60)) + " minutes ago"
                if second_diff < 7200:
                    return "an hour ago"
                if second_diff < 86400:
                    return str(int(second_diff / 3600)) + " hours ago"
            if day_diff == 1:
                return "Yesterday"
            if day_diff < 7:
                return str(int(day_diff)) + " days ago"
            if day_diff < 31:
                return str(int(day_diff / 7)) + " weeks ago"
            if day_diff < 365:
                return str(int(day_diff / 30)) + " months ago"
            return str(int(day_diff / 365)) + " years ago"
        return "Never"
    friendlyTimeDiff.short_description = "Time since last update"

    def __str__(self):
        return self.description[0:30]


class DSS(models.Model):
    """
    DSS class

    Fields:
    device - foreignkey to device related to this DSS, on delete - cascade. Limited only to those devices that are based on device model with DSS = True
    dssType - text length 45, choices enumeration:
    BLF = 'BLF - Busy Lamp Field' (default value)
    SPD = 'SPD - Speed dial key'
    key - Integer - ordinal number of the DSS per device, required (not null and not blank)
    value - char length 255 - what is dialed, required (not null and not blank)
    label - char length 255 - what is presented on the DSS

    __str__: label

    Unique per device & key
    Verbose name: DSS
    """
    class dssType(models.TextChoices):
        BLF = 'BLF - Busy Lamp Field'
        SPD = 'SPD - Speed dial key'

    device = models.ForeignKey(
        'Device', on_delete=models.CASCADE, limit_choices_to={"devmodel__dss": 1}, verbose_name="Device to connect DSS")
    dssType = models.TextField(
        max_length=45, choices=dssType.choices, default=dssType.BLF, verbose_name="DSS type")
    key = models.IntegerField(blank=False, null=False,
                              default=1, verbose_name="DSS key")
    value = models.CharField(max_length=255, blank=False,
                             null=False, verbose_name="DSS value")
    label = models.CharField(max_length=255, blank=True,
                             null=True, verbose_name="DSS label")

    class Meta:
        unique_together = ("device", "key")
        verbose_name = "DSS"

    def __str__(self):
        return self.label


class Extension(models.Model):
    """
    Extension class

    Fields:
    name - char length 64, required (not null and not blank), verbose_name="Extension name"
    extension - integer - actual phone number
    customer - foreignkey, on delete - cascade, an extension can be related to only one customer. Verbose name "Customer"

    Extensions must be unique within a customer

    __str__: 30 chars of name field for easier display on forms
    """
    name = models.CharField(max_length=64, blank=False,
                            null=False, verbose_name="Extension name")
    extension = models.IntegerField(
        null=False, blank=False, verbose_name="Extension")
    customer = models.ForeignKey(
        "Customer", on_delete=models.CASCADE, verbose_name='Customer')

    class Meta:
        unique_together = ("customer", "extension")

    def __str__(self):
        return self.name[0:30]

# Customers


class Customer(models.Model):
    """
    Customer class

    Fields:
    description - char length 100, required (not null and not blank), verbose_name="Customer"

    __str__: 30 chars of description field for easier display on forms
    """
    description = models.CharField(
        max_length=100, null=False, blank=False, verbose_name="Customer")

    def __str__(self):
        return self.description[0:30]
