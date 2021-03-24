from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, status
from .models import Device
from django.utils import timezone
import logging
import sys

# creating logger object
logger = logging.getLogger(__name__)


def GetXMLConfig(device_id):
    """
    Function that, based on device id, collect XML configuration for a device. In same time the function updates cfg_last_update time for the requested device.
    """
    data = []
    dict = {}
    try:
        device = Device.objects.filter(id=device_id)
        if device.count() > 0:
            device = device[0]
            device.cfg_last_update = timezone.now()
            device.save(update_fields=['cfg_last_update'])
            data = device.XMLConfig()
        else:
            dict["message"] = "No available device"
            data.append(dict)
            logger.warning("No available device (id = " + str(device_id)+")")
    except Exception as e:
        e = str(e)
        dict["error"] = "Error retrieving device data"
        dict["description"] = e
        data.append(dict)
        logger.error(e)
    return data


class GetXMLConfiguration(APIView):
    """
    The view for REST end point that allows collection of XML configuration data.
    """

    def get(self, request):
        """
        Overriden method that allows function call. It is calling GetXMLConfig()
        """
        device_id = request.data.get('device', '')
        if device_id.isnumeric():
            return Response(GetXMLConfig(int(device_id)))
        else:
            error = "Wrong ID format"
            response = {'message': error}
            logger.error(error)
            return Response(response)

    def update(self, request, *args, **kwargs):
        """
        Overriden method that disallows update of data.
        """
        response = {'message': 'You cant update rating this way'}
        logger.error(
            "Tried to update values using XML endopoint GetXMLConfiguration")
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        """
        Overriden method that disallows creation of data.
        """
        response = {'message': 'You cant create rating this way'}
        logger.error(
            "Tried to create values using XML endopoint GetXMLConfiguration")
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
