from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group

from apps.ecr.models import Facilidad


OPERADOR_GRADO = (
   ('1', 'Cabo'),
   ('2', 'Cabo 1ro'),
   ('3', 'Sargento'),
)



class Turno(models.Model):
   rol = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='turnos')
   desde = models.DateTimeField(null=True, blank=True)
   hasta = models.DateTimeField(null=True, blank=True)


class Operador(AbstractUser):
   grado = models.CharField(max_length=1, blank=True, null=True, choices=OPERADOR_GRADO)
   facilidad = models.ForeignKey(Facilidad, blank=True, null=True, on_delete=models.CASCADE, related_name='operadores_en_facilidad')
   turno = models.ForeignKey(Turno, blank=True, null=True, on_delete=models.CASCADE, related_name='operadores_en_turno')
   rol =  models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True, related_name='personal')


   def __str__(self):
      return self.username



