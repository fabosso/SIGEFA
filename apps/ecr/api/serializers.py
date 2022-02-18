from rest_framework import serializers

from ..models import (
    Evento,
    Facilidad,
    EstadoAlistamiento,
    EqCom,
    Vehiculo,
    GpoElectr,
    Sensor,

)


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = (
            'id',
            'nombre',
            'indicador',
        )


class EventoSerializer(serializers.ModelSerializer):
    tipo = serializers.StringRelatedField(read_only=True)
    subtipo = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Evento
        fields = (
            'id',
            'tipo',
            'subtipo',
            'description',
            'timestamp',
        )

    def to_representation(self, instance):
        representation = super(EventoSerializer, self).to_representation(instance)
        representation['timestamp'] = instance.timestamp.strftime('%d/%m/%Y, %H:%M:%S %p')
        return representation


class CombustibleVehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = ('cant_combustible_vehiculo',)


class CombustibleGpoElectrSerializer(serializers.ModelSerializer):
    class Meta:
        model = GpoElectr
        fields = ('cant_combustible_gpo_elect',)


class EstadoAlistamientoSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = EstadoAlistamiento
        fields = (
            'nombre',
            'fecha',
            'status',
        )

    def to_representation(self, instance):
        representation = super(EstadoAlistamientoSerializer, self).to_representation(instance)
        representation['fecha'] = instance.fecha.strftime('%d/%m/%Y, %H:%M:%S %p')
        return representation


class EqComSerializer(serializers.ModelSerializer):
    class Meta:
        model = EqCom
        fields = (
            'nombre',
        )


class FacilidadSerializer(serializers.ModelSerializer):
    estados_alistamiento = EstadoAlistamientoSerializer(many=True, read_only=True)
    eventos = EventoSerializer(many=True, read_only=True)
    sensores = SensorSerializer(many=True, read_only=True)

    class Meta:
        model = Facilidad
        fields = (
            'id',
            'nombre',
            'estados_alistamiento',
            'eventos',
            'sensores',
        )


