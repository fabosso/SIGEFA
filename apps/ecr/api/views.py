from django.db import connection
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse, Http404
from rest_framework import generics, permissions
from rest_framework import renderers
from rest_framework import status
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt

from .pagination import CustomPagination, StandardResultsSetPagination
from .serializers import (
   EventoSerializer,
   FacilidadSerializer,
   EstadoAlistamientoSerializer,
   CombustibleVehiculoSerializer,
   CombustibleGpoElectrSerializer,
   SensorSerializer,
)

from ..models import Evento, Facilidad, EstadoAlistamiento, Sensor



class ApiEventosList(ListAPIView):
   serializer_class = EventoSerializer
   pagination_class = CustomPagination

   def dispatch(self, *args, **kwargs):
      response = super().dispatch(*args, **kwargs)
      print('Queries Counted: {}'.format(len(connection.queries)))
      return response

   
   def get_queryset(self):
      facilidad_pk = self.kwargs['pk']
      queryset = Evento.objects.filter(facilidad__pk=facilidad_pk).select_related('tipo', 'subtipo', 'facilidad').prefetch_related('tipo', 'subtipo', 'facilidad')

      return queryset


class FacilidadAPIListView(ListAPIView):
   serializer_class = FacilidadSerializer
   queryset = Facilidad.objects.all()
   pagination_class = StandardResultsSetPagination
   renderer_classes = [renderers.JSONRenderer]


class FacilidadAPIDetailView(APIView):
   permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

   def get(self, request, pk):
      facilidad = get_object_or_404(Facilidad, pk=pk)
      data = FacilidadSerializer(facilidad).data
      return Response(data)


class FacilidadAPIStatusView(APIView):

   def get(self, request, pk):
      facilidad = get_object_or_404(Facilidad, pk=pk)
      estado_instance = facilidad.estados_alistamiento.first()
      data = EstadoAlistamientoSerializer(estado_instance).data
      return Response(data)
   
   def post(self, request, pk):
      facilidad = get_object_or_404(Facilidad, pk=pk)
      estado_instance = facilidad.estados_alistamiento.first()
      serializer = EstadoAlistamientoSerializer(estado_instance, data=request.data)
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VehiculoAPICantCombus(APIView):

   def get(self, request, pk):
      facilidad = get_object_or_404(Facilidad, pk=pk)
      equipamientos = facilidad.equipamientos

      veh_content = ContentType.objects.get(app_label='ecr', model='vehiculo')
      vehiculo = equipamientos.get(content_type=veh_content)
      vehiculo_obj = veh_content.get_object_for_this_type(id=vehiculo.object_id)

      data = CombustibleVehiculoSerializer(instance=vehiculo_obj).data
      return Response(data)


class GpoElectrAPICantCombus(APIView):

   def get(self, request, pk):
      facilidad = get_object_or_404(Facilidad, pk=pk)
      equipamientos = facilidad.equipamientos

      gpoelectr_content = ContentType.objects.get(app_label='ecr', model='gpoelectr')
      gpoelectr = equipamientos.get(content_type=gpoelectr_content)
      gpoelectr_obj = gpoelectr_content.get_object_for_this_type(id=gpoelectr.object_id)

      data = CombustibleGpoElectrSerializer(instance=gpoelectr_obj).data
      return Response(data)


class SensorAPIView(APIView):

   def get_object(self, sensor_id):
      try:
         return Sensor.objects.get(id=sensor_id)
      except Sensor.DoesNotExist:
         raise Http404

   def get(self, request, pk, sensor_id, format=None):
      sensor = self.get_object(sensor_id)
      serializer = SensorSerializer(sensor)
      return Response(serializer.data)

   def post(self, request, pk, sensor_id, format=None):
      sensor = self.get_object(sensor_id)
      serializer = SensorSerializer(sensor, data=request.data)
      if serializer.is_valid():
         serializer.save()
         return Response(serializer.data)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
