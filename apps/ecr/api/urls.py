from django.urls import path


from .views import (
   ApiEventosList,
   FacilidadAPIListView,
   FacilidadAPIStatusView,
   FacilidadAPIDetailView,
   VehiculoAPICantCombus,
   GpoElectrAPICantCombus,
   SensorAPIView,
)



urlpatterns = [
   path('facilidad/list', FacilidadAPIListView.as_view(), name='api_facilidad_list'),
   path('facilidad/<int:pk>/status', FacilidadAPIStatusView.as_view(), name='api_facilidad_status'),
   path('facilidad/<int:pk>/detail', FacilidadAPIDetailView.as_view(), name='api_facilidad_detail'),
   path('facilidad/<int:pk>/eventos/list', ApiEventosList.as_view(), name='eventos_list'),
   path('facilidad/<int:pk>/vehiculo/cant-combustible/', VehiculoAPICantCombus.as_view(), name='api_vehiculo_combustible'),
   path('facilidad/<int:pk>/gpo-electr/cant-combustible/', GpoElectrAPICantCombus.as_view(), name='api_gpoelectr_combustible'),
   path('facilidad/<int:pk>/sensor/<sensor_id>/edit/', SensorAPIView.as_view(), name='api_facilidad_sensor'),

]