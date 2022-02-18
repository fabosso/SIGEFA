from django.urls import path

from .views import (
   EcrDashboardView, ActionOptionsView,
   InitialConfView, EventosView, search_event_subtipo,
   change_status_facilidad, SensorSectionView
)



app_name = 'ecr'

urlpatterns = [
   path('choice-ecr-actions/', ActionOptionsView.as_view(), name='ecr_action_option'),
   path('initial-conf/', InitialConfView.as_view(), name='ecr_initial_conf'),
   path('<int:pk>/', EcrDashboardView.as_view(), name='ecr_index'),
   path('<int:pk>/eventos', EventosView.as_view(), name='ecr_eventos'),
   path('search_subtipo', search_event_subtipo, name='search_subtipo'),
   path('change/facilidad_status/', change_status_facilidad, name='change_status_facilidad'),
   path('<int:pk>/sensor/', SensorSectionView.as_view(), name='ecr_sensor'),
]