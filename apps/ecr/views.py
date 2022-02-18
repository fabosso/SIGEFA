import json
from django.db import transaction, connection
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView, DetailView
from django.http import JsonResponse
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .models import (
   Facilidad, Vehiculo, 
   GpoElectr, EqCom,
   Equipamiento,
   ECR, Corresponsal,
   SubTipoEvento,
   Evento,
   EstadoAlistamiento
)

from .forms import (
   SelectionActionForms, 
   ComunicacionesForm,
   LogisticaEqComFormset,
   VehiculoForm,
   GpoElectForm,
   CombusVehiculo,
   CombusGpoElect,
   EventoForm,
   SensorForm
)




class ActionOptionsView(LoginRequiredMixin, View):
   template_name = 'ecr_actions_option.html'
   login_url = 'accounts/login/'

   def get(self, *args, **kwargs):
      form = SelectionActionForms()

      ctx = {
         'form': form,
      }
      return render(self.request, self.template_name, ctx)
   
   def post(self, *args, **kwargs):
      form = SelectionActionForms(self.request.POST)

      user = self.request.user

      if form.is_valid():
         option = form.cleaned_data['ecr_action_options']

         if option == '1':
            return redirect("ecr:ecr_initial_conf")
         else:
            if user.facilidad:
               return redirect("ecr:ecr_index", pk=user.facilidad.pk)
            messages.error(self.request, "Aún no posee ningun proceso de Gestion de Facilidad configurado.")
            return redirect("ecr:ecr_action_option")


      else:
         return render(self.request, self.template_name, {'form': form})


class InitialConfView(LoginRequiredMixin, View):
   template_name = 'ecr_initial_conf.html'
   login_url = 'accounts/login/'

   def dispatch(self, *args, **kwargs):
      facilidad = self.request.user.facilidad

      if facilidad:
         return redirect(facilidad.get_absolute_url())
      return super(InitialConfView, self).dispatch(self.request)

   def get(self, *args, **kwargs):
      form = ComunicacionesForm()
      formset = LogisticaEqComFormset()
      vehiculo_form = VehiculoForm()
      gpo_electform = GpoElectForm()

      ctx = {
         'form': form,
         'formset': formset,
         'vehiculo_form': vehiculo_form,
         'gpo_electform': gpo_electform,
      }
      return render(self.request, self.template_name, ctx)

   def post(self, *args, **kwargs):
      data = {}
      user = self.request.user
      r = self.request.POST

      
      comunication_form = ComunicacionesForm(r)
      logistic_formset = LogisticaEqComFormset(r)
      vehiculo_form = VehiculoForm(r)
      gpo_elect_form = GpoElectForm(r)

      try:
         # Set "Facilidad" name.
         if comunication_form.is_valid() and logistic_formset.is_valid() and vehiculo_form.is_valid() and gpo_elect_form.is_valid():

            # Cleaned Data forms
            cd_comunication = comunication_form.cleaned_data
            cd_logistic = logistic_formset.cleaned_data
            cd_vehiculo = vehiculo_form.cleaned_data
            cd_gpo_elect = gpo_elect_form.cleaned_data


            # If an error happend. Don't save in the database.
            with transaction.atomic():
               comunicaciones_option = cd_comunication.get('comunicaciones_options', None)


               if comunicaciones_option:
                  if comunicaciones_option == '1':
                     fac_name = cd_comunication.get('comunicaciones_ecr')
                  else:
                     fac_name = cd_comunication.get('comunicaciones_corresp')

               facilidad = Facilidad.objects.create(
                  nombre=fac_name.nombre
               )
               
               # Create initial Status
               EstadoAlistamiento.objects.create(
                     nombre=fac_name.nombre,
                     status='L',
                     facilidad=facilidad,
                  )

               # Get all "Logistica" forms.
               # As a "Logistica" is a form set,
               # its need iterate throgout the queryset,
               # to get all the possible incoming forms.
               eqcoms = [EqCom.objects.create(nombre=i['nombre']) for i in cd_logistic]

               for e in eqcoms:
                  Equipamiento.objects.create(content_object=e, facilidad=facilidad)

               # Vehiculo # TODO UNDRY
               v = Vehiculo.objects.create(
                  nombre_vehiculo=cd_vehiculo.get('nombre_vehiculo'), 
                  cant_combustible_vehiculo=cd_vehiculo.get('cant_combustible_vehiculo'),
                  cap_combustible_vehiculo=cd_vehiculo.get('cap_combustible_vehiculo'),
                  marca_vehiculo=cd_vehiculo.get('marca_vehiculo'),
                  modelo_vehiculo=cd_vehiculo.get('modelo_vehiculo')
               )
               Equipamiento.objects.create(content_object=v, facilidad=facilidad)

               # Gpo Elect # TODO UNDRY
               ge = GpoElectr.objects.create(
                  nombre_gpo_elect=cd_gpo_elect.get('nombre_gpo_elect'), 
                  cant_combustible_gpo_elect=cd_gpo_elect.get('cant_combustible_gpo_elect'),
                  cap_combustible_gpo_elect=cd_gpo_elect.get('cap_combustible_gpo_elect'),
                  marca_gpo_elect=cd_gpo_elect.get('marca_gpo_elect'),
                  modelo_gpo_elect=cd_gpo_elect.get('modelo_gpo_elect')
               )
               Equipamiento.objects.create(content_object=ge, facilidad=facilidad)

               user.facilidad = facilidad
               user.save()

               messages.success(self.request, "Se ha configurado la Facilidad satisfactoriamente.")
               data = {
                  'status': 200,
                  'success_url': reverse_lazy('ecr:ecr_index', kwargs={'pk': facilidad.pk}),
                  'message': "",
               }
               return JsonResponse(data)
         data = {
            'status': 400,
            'message': "Ha ocurrido un error en el procesado del formulario.",
            'errors': [
               comunication_form.errors.as_json(),
               self.get_formset_errors(logistic_formset.errors),
               vehiculo_form.errors.as_json(),
               gpo_elect_form.errors.as_json(),
            ]
         }
         return JsonResponse(data, safe=False)
      except Exception as e:
         print(e)
         data = {
            'status': 500,
            'message': "Ha ocurrido un problema inesperado en la configuracion.",
            'errors': str(e),
         }
         return JsonResponse(data)

   def get_formset_errors(self, formset_errors):
      errors = dict()

      for error in formset_errors:
         if error:
            for k, v in error.items():
               index = formset_errors.index(error)
               key = 'form-{index}-{field}'.format(index=index, field=k)
               errors[key] = v
      return json.dumps(errors)


class EcrDashboardView(LoginRequiredMixin, DetailView):
   template_name = 'ecr_index.html'
   model = Facilidad
   context_object_name = 'facilidad'
   login_url = 'accounts/login/'
   facilidad = None
   vehiculo_obj = None
   gpoelectr_obj = None
   equipamientos = None
   status = None


   @method_decorator(csrf_exempt)
   def dispatch(self, *args, **kwargs):
      if self.request.user.is_anonymous:
         return redirect("login")
      
      if not self.request.user.facilidad:
         messages.error(self.request, "No poseé o no se encuentra en algún proceso de Facilidad.")
         return redirect("ecr:ecr_action_option")

      self.facilidad = self.request.user.facilidad
      self.status = self.facilidad.estados_alistamiento.first()
      self.equipamientos = self.facilidad.equipamientos

      # Get contenttype of each equipments.
      veh_content = ContentType.objects.get(app_label='ecr', model='vehiculo')
      gpoelectr_content = ContentType.objects.get(app_label='ecr', model='gpoelectr')

      # Get de equipments object.
      try:
         vehiculo = self.equipamientos.get(content_type=veh_content)
         self.vehiculo_obj = veh_content.get_object_for_this_type(id=vehiculo.object_id)
      except Exception as e:
         self.vehiculo_obj = None

      try:
         gpoelectr = self.equipamientos.get(content_type=gpoelectr_content)
         self.gpoelectr_obj = gpoelectr_content.get_object_for_this_type(id=gpoelectr.object_id)
      except Exception as e:
         self.gpoelectr_obj = None


      # TODO Permission for users creation.

      if not self.facilidad:
         messages.info(self.request, "Aún no posee ningun proceso de Gestion de Facilidad configurado.")
         return redirect('ecr_action_options')
      return super(EcrDashboardView, self).dispatch(self.request)

   def get_context_data(self, *args, **kwargs):
      context = super(EcrDashboardView, self).get_context_data(**kwargs)
      eventos_form = EventoForm()
      eventos_form.fields['subtipo'].queryset = SubTipoEvento.objects.none()
      context['eventos_form'] = eventos_form
      context['facilidad_id'] = self.facilidad.id
      context['facilidad_name'] = self.facilidad.nombre
      context['facilidad_status'] = self.status.status


      eqcom_content = ContentType.objects.get(app_label='ecr', model='eqcom')
      
      eqcom_list = self.equipamientos.filter(content_type=eqcom_content)
      
      context['vehiculo'] = self.vehiculo_obj
      context['eqcom_list'] = EqCom.objects.filter(id__in=eqcom_list.values_list('object_id'))
      context['gpoelectr'] = self.gpoelectr_obj

      if self.vehiculo_obj and self.gpoelectr_obj:
         context['comb_vehiculo_form'] = CombusVehiculo(instance=self.vehiculo_obj)
         context['comb_gpoelect_form'] = CombusGpoElect(instance=self.gpoelectr_obj)
      elif self.vehiculo_obj:
         context['comb_vehiculo_form'] = CombusVehiculo(instance=self.vehiculo_obj)
      elif self.gpoelectr_obj:
         context['comb_gpoelect_form'] = CombusGpoElect(instance=self.gpoelectr_obj)

      context['section'] = "Logistica"

      return context

   
   def post(self, *args, **kwargs):
      data = {}
      r = self.request.POST

      vehiculo = r.get('cant_combustible_vehiculo', None)
      gpoelect = r.get('cant_combustible_gpo_elect', None)

      try:
         with transaction.atomic():
            if vehiculo:
               form_vehiculo = CombusVehiculo(r, instance=self.vehiculo_obj)

               if form_vehiculo.is_valid():
                  form_vehiculo.save()
                  return JsonResponse({'status': 200, 'form_name': 'vehiculo_form'})
               else:
                  data = {
                     'status': 400,
                     'errors': str(form_vehiculo.errors)
                  }
            
            if gpoelect:
               form_gpoelectr = CombusGpoElect(r, instance=self.gpoelectr_obj)
               
               if form_gpoelectr.is_valid():
                  form_gpoelectr.save()
                  return JsonResponse({'status': 200, 'form_name': 'gpoelect_form'})
               else:
                  data = {
                     'status': 400,
                     'errors': str(form_vehiculo.errors)
                  }
            return JsonResponse(data)
      except Exception as e:
         data = {
            'status': 500,
            'error': str(e),
            'message': 'Ha ocurrido un error en el procesado del formulario.'
         }
         return JsonResponse(data)


class EventosView(View):
   template_name = 'ecr_eventos.html'


   def get(self, request, pk, *args, **kwargs):
      facilidad = get_object_or_404(Facilidad, pk=pk)
      context = dict()

      context['facilidad_id'] = facilidad.id
      eventos_form = EventoForm()
      eventos_form.fields['subtipo'].queryset = SubTipoEvento.objects.none()
      context['eventos_form'] = eventos_form
      context['section'] = "Libro de Guardia"

      return render(self.request, self.template_name, context)


   def post(self, *args, **kwargs):
      form = EventoForm(self.request.POST)
      try:
         with transaction.atomic():
            if form.is_valid():
               instance = form.save(commit=False)
               facilidad_obj = Facilidad.objects.get(id=self.request.POST.get('id_facilidad_obj', None))
               instance.facilidad = facilidad_obj
               instance.save()
               return JsonResponse({'status': 200, 'message': 'Evento generado. Visualice el Libro de Guardia.'})
            return JsonResponse({'status': 400, 'errors': str(form.errors)})
      except Exception as e:
         return JsonResponse({'status': 500, 'errors': str(e)})


class SensorSectionView(View):
   template_name = 'sensor_section.html'
   form_class = SensorForm
   facilidad_obj = None


   def dispatch(self, *args, **kwargs):
      facilidad_pk = self.kwargs.get('pk', None)

      if facilidad_pk:
         self.facilidad_obj = get_object_or_404(Facilidad, pk=facilidad_pk)

      return super(SensorSectionView, self).dispatch(self.request)

   
   def get(self, *args, **kwargs):
      pk = self.kwargs.get('pk', None)
      facilidad = get_object_or_404(Facilidad, pk=pk)

      context = dict()
      context['facilidad_id'] = facilidad.id
      context['section'] = "Sensores"

      if bool(facilidad.sensores.first()):
         context['sensor_created'] = True
         sensor = self.facilidad_obj.sensores.first()
         context['sensor_id'] = sensor.id
      else:
         context['sensor_created'] = False
         context['form'] = self.form_class()
         messages.info(self.request, "Aún se ha agregado ningun sensor a la facilidad.")
      return render(self.request, self.template_name, context)

   def post(self, *args, **kwargs):
      try:
         form = self.form_class(self.request.POST)

         if form.is_valid():
            data = dict()
            instance = form.save(commit=False)
            instance.facilidad = self.facilidad_obj
            instance.save()

            ctx = {
               'sensor': instance
            }

            data['status'] = 200
            data['html_card'] = render_to_string('sensor_card.html', ctx)
            return JsonResponse(data)
         return JsonResponse({
            'status': 400,
            'errors': form.errors.as_json()
         })

      except Exception as e:
         return JsonResponse({
            'status': 500,
            'error': str(e),
            'message': 'Un error ha ocurrido.'
         })

      


def search_event_subtipo(request):
   r_id = request.GET.get('id', None)

   data = [{'id': '', 'text': '---------'}]
   for i in SubTipoEvento.objects.filter(tipo=r_id):
      data.append({'id': i.id, 'text': i.nombre_sub_tipo})

   return JsonResponse(data, safe=False)


def change_status_facilidad(request):

   if request.method == 'POST':
      id = request.POST.get('id', None)
      status = request.POST.get('status', None)

      if id and status:
         facilidad = get_object_or_404(Facilidad, id=id)
         facilidad_status = facilidad.estados_alistamiento.first()
         facilidad_status.status = status
         facilidad_status.save()

         return JsonResponse({'message': 'El estado fue actualizado.'}, status=200)
      return JsonResponse({'error': 'Ha ocurrido un error en la solicitud.'}, status=404)
   return JsonResponse({'error': 'Ha ocurrido un problema en la actualizacion del estado.'}, status=500)
