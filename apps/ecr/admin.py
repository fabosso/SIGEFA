from django.contrib import admin

from .models import (
   ECR, Corresponsal, Facilidad, 
   Equipamiento, EqCom, Vehiculo,
   GpoElectr, TipoEvento, SubTipoEvento, Evento,
   OrigenDestinoEvento, ClasificacionEvento, PrecedenciaEvento, CifradoEvento,
   EstadoAlistamiento, Sensor
)

admin.site.register(ECR)
admin.site.register(Corresponsal)
admin.site.register(Facilidad)
admin.site.register(EstadoAlistamiento)
admin.site.register(EqCom)
admin.site.register(Vehiculo)
admin.site.register(GpoElectr)
admin.site.register(TipoEvento)
admin.site.register(SubTipoEvento)
admin.site.register(OrigenDestinoEvento)
admin.site.register(ClasificacionEvento)
admin.site.register(PrecedenciaEvento)
admin.site.register(CifradoEvento)
admin.site.register(Evento)
admin.site.register(Sensor)

