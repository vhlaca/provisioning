from django.contrib import admin
from django.http import HttpResponse
from django.utils import timezone
from django.utils.html import format_html, html_safe, escape
from django.utils.safestring import mark_safe

from .models import DSS, Customer, Device, DevModel, DevVendor, Extension
from .endpoints import GetXMLConfig


def turnOffFields(form, fields):
    """This function receives a form and list of fields which are foreign key shown on same form, and then disables edit or add values over forign key"""
    for field in fields:
        field = form.base_fields[field]
        field.widget.can_add_related = False
        field.widget.can_change_related = False
        field.widget.can_delete_related = False
    return form


def actionGetXMLConf(modeladmin, request, queryset):
    """
    This function is used as admin action on lisf of devices. Parameters are automatic: modeladmin, request, queryset.
    The data is shown in same window and therefore to continue with administration it is necessary to click back button.
    """
    xmlData = b'XML conviguration for selected devices\n\n'
    for q in queryset:
        temp = GetXMLConfig(q.id)
        xmlData = b''.join([xmlData, temp, b'\n\n'])
    xmlData = b''.join(
        [xmlData, b'\n\nClick back on your browser to return to Admin forms'])
    return HttpResponse(xmlData.decode('utf8'), content_type='text')


actionGetXMLConf.short_description = "Get XML configuration"


class DeviceAdmin(admin.ModelAdmin):
    """
    Administration of devices

    Following is set:
    readonly_fields = ['friendlyTimeDiff', 'countDSS', "XMLConfig"]
    fields = ['description', 'mac', 'devmodel', 'extension', 'friendlyTimeDiff', 'countDSS']
    list_display = ['description', 'friendlyTimeDiff', 'custom_xml_url']
    list_filter = ['devmodel', 'extension__customer']
    search_fields = ['mac', 'description', 'extension__customer__description', 'devmodel__name', ]
    autocomplete_fields = ["devmodel",                            "extension"]
    actions = [actionGetXMLConf]

    customer_xml_url is dummy buttone and when it is clicked XML configuration windows of a device is shown in new tab.

    """

    def get_form(self, request, obj=None, **kwargs):
        """
        Overriden method which allows usage of funcion turnOffFields
        """
        form = super().get_form(request, obj, **kwargs)

        fields = ["devmodel", "extension"]
        return turnOffFields(form, fields)

    readonly_fields = ['friendlyTimeDiff', 'countDSS', "XMLConfig"]
    fields = ['description', 'mac', 'devmodel',
              'extension', 'friendlyTimeDiff', 'countDSS']
    list_display = ['description', 'friendlyTimeDiff',
                    'custom_xml_url']
    list_filter = ['devmodel',
                   'extension__customer']
    search_fields = ['mac', 'description',
                     'extension__customer__description', 'devmodel__name', ]
    autocomplete_fields = ["devmodel",
                           "extension"]
    actions = [actionGetXMLConf]

    def custom_xml_url(self, obj):
        """
        custom_xml_url is used for creation of dummy link to open window with XML configuration of a device. It includes the device id
        """
        return mark_safe('<a href="" onclick=(window.open("../form/{}"))>Configuration</ a>'.format(obj.id))
    custom_xml_url.short_description = 'XML configuration'
    custom_xml_url.allow_tags = True


class DSSAdmin(admin.ModelAdmin):
    """
    Administration of DSS
    Following is set:
    list_display = ['label']
    """

    def get_form(self, request, obj=None, **kwargs):
        """
        Overriden method which allows usage of funcion turnOffFields
        """
        form = super().get_form(request, obj, **kwargs)
        fields = ["device", ]
        return turnOffFields(form, fields)

    list_display = ['label']


class DevModelAdmin(admin.ModelAdmin):
    """
    Administration of device models
    Following is set:
    search_fields = ["name", 'id']
    """
    search_fields = ["name", 'id']


class ExtensionAdmin(admin.ModelAdmin):
    """
    Administration of extensions
    Following is set:
    search_fields = ["name", "id"]
    """

    def get_form(self, request, obj=None, **kwargs):
        """
        Overriden method which allows usage of funcion turnOffFields
        """
        form = super().get_form(request, obj, **kwargs)

        fields = ["customer", ]
        return turnOffFields(form, fields)
    search_fields = ["name", "id"]


# Register your models here.
admin.site.register(DevVendor)
admin.site.register(DevModel, DevModelAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(DSS, DSSAdmin)
admin.site.register(Extension, ExtensionAdmin)
admin.site.register(Customer)
