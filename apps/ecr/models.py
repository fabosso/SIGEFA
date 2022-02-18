from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse




OPERADOR_ROL = (
   ('OP', 'Operador'),
   ('CO', 'Conductor'),
)

STATUS = (
   ('S', 'En servicio'),
   ('L', 'Limitado'),
   ('F', 'F/S'),
)




class TipoEvento(models.Model):
   nombre_tipe = models.CharField(max_length=50)

   def __str__(self):
      return self.nombre_tipe


class SubTipoEvento(models.Model):
   nombre_sub_tipo = models.CharField(max_length=50)

   tipo = models.ForeignKey(TipoEvento, on_delete=models.CASCADE, related_name='subtipos')

   def __str__(self):
      return self.nombre_sub_tipo


class BaseModelComunicaciones(models.Model):
   nombre = models.CharField(max_length=50)


   class Meta:
      abstract = True


class ECR(BaseModelComunicaciones):

   def __str__(self):
      return self.nombre


class Corresponsal(BaseModelComunicaciones):

   def __str__(self):
      return self.nombre


class Facilidad(models.Model):
   nombre = models.CharField(max_length=50)


   class Meta:
      ordering = ('id',)


   def __str__(self):
      return self.nombre

   def get_absolute_url(self):
      return reverse('ecr:ecr_index', kwargs={'pk': self.pk})


class EstadoAlistamiento(models.Model):
   nombre = models.CharField(max_length=150)
   fecha = models.DateField(auto_now=True)
   status = models.CharField(max_length=1, choices=STATUS)

   facilidad = models.ForeignKey(Facilidad, on_delete=models.CASCADE, related_name='estados_alistamiento')

   def __str__(self):
      return "Estado: {}".format(self.get_status_display())


class Evento(models.Model):
   description = models.TextField()
   tipo = models.ForeignKey(TipoEvento, on_delete=models.CASCADE, related_name='eventos_por_tipos')
   subtipo = models.ForeignKey(SubTipoEvento, on_delete=models.CASCADE, related_name='eventos_por_subtipos')
   timestamp = models.DateTimeField(auto_now_add=True)

   facilidad = models.ForeignKey(Facilidad, on_delete=models.CASCADE, related_name='eventos')

   
   class Meta:
      ordering = ['-timestamp',]



   def __str__(self):
      return "Evento: {}. Facilidad: {}".format(self.pk, self.facilidad.nombre)


class Sensor(models.Model):
   nombre = models.CharField(max_length=50)
   indicador = models.FloatField()

   facilidad = models.ForeignKey(Facilidad, null=True, blank=True, on_delete=models.CASCADE, related_name='sensores')

   def __str__(self):
      return "Sensor: {}. Facilidad: {}".format(self.nombre, self.facilidad.nombre)


class Equipamiento(models.Model):
   content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in':('Eq_com', 'Vehiculo', 'Gpo_electr')})
   object_id = models.PositiveIntegerField()
   content_object = GenericForeignKey('content_type', 'object_id')

   facilidad = models.ForeignKey(Facilidad, null=True, blank=True, on_delete=models.CASCADE, related_name='equipamientos')


class EqCom(models.Model):
   nombre = models.CharField(max_length=80)

   equipo = GenericRelation(Equipamiento)


   def __str__(self):
      return "Equipamiento: {}".format(self.nombre)


class Vehiculo(models.Model):
   nombre_vehiculo = models.CharField(max_length=80)
   marca_vehiculo = models.CharField(max_length=80, null=True, blank=True)
   modelo_vehiculo = models.CharField(max_length=80, null=True, blank=True)
   tipo_combustible = models.CharField(max_length=80, blank=True, null=True)
   cap_combustible_vehiculo = models.PositiveIntegerField(blank=True, null=True)
   cant_combustible_vehiculo = models.PositiveIntegerField(blank=True, null=True)

   equipo = GenericRelation(Equipamiento)


   def __str__(self):
      return "Equipamiento: {}".format(self.nombre_vehiculo)


class GpoElectr(models.Model):
   nombre_gpo_elect = models.CharField(max_length=80)
   marca_gpo_elect = models.CharField(max_length=80, null=True, blank=True)
   modelo_gpo_elect = models.CharField(max_length=80, null=True, blank=True)
   tipo_combustible_gpo_elect = models.CharField(max_length=80, blank=True, null=True)
   cap_combustible_gpo_elect = models.PositiveIntegerField(blank=True, null=True)
   cant_combustible_gpo_elect = models.PositiveIntegerField(blank=True, null=True)

   equipo = GenericRelation(Equipamiento)


   def __str__(self):
      return "Equipamiento: {}".format(self.nombre_gpo_elect)