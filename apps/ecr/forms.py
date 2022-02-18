from django import forms
from django.forms import formset_factory
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .models import (
   ECR, Corresponsal, EqCom,
   Vehiculo, GpoElectr, Evento,
   TipoEvento, SubTipoEvento, Sensor
)

User = get_user_model()



ACTION_OPTIONS = (
   ('1', 'Cargar cofiguracion inicial'),
   ('2', 'Operar facilidad'),
)


COMUNICACIONES_OPTIONS = (
   ('1', 'ECR'),
   ('2', 'Corresponsal')
)



class SelectionActionForms(forms.Form):
   ecr_action_options = forms.ChoiceField(choices=ACTION_OPTIONS)


class ComunicacionesForm(forms.Form):

   # TODO improve this performance. Its better if remove comunicatione_optiones?
   # and display that radio select options on client-side?

   comunicaciones_options = forms.ChoiceField(choices=COMUNICACIONES_OPTIONS, required=True)
   comunicaciones_ecr = forms.ModelChoiceField(
      queryset=ECR.objects.all(), 
      widget=forms.Select(attrs={'class': 'form-control'}),
      empty_label=None, 
      required=True)

   comunicaciones_corresp = forms.ModelChoiceField(
      queryset=Corresponsal.objects.all(), 
      widget=forms.Select(attrs={'class': 'form-control'}),
      empty_label=None,  
      required=True)


class VehiculoForm(forms.ModelForm):
   nombre_vehiculo = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Nombre:", required=True)
   cant_combustible_vehiculo = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}), label="Cant Combustible:", required=True)
   cap_combustible_vehiculo = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}), label="Cap Combustible:", required=True)

   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      for form in self.visible_fields():
         form.field.widget.attrs['class'] = 'form-control'

   def clean(self):
      super().clean()
      cant_combustible_vehiculo = self.cleaned_data['cant_combustible_vehiculo']
      cap_combustible_vehiculo = self.cleaned_data['cap_combustible_vehiculo']

      if cant_combustible_vehiculo > cap_combustible_vehiculo:
         self.add_error('cant_combustible_vehiculo',  forms.ValidationError("La cantidad de combustible, no puede ser mayor a la capacidad del vehiculo."))


   
   class Meta:
      model = Vehiculo
      fields = (
         'nombre_vehiculo',
         'cant_combustible_vehiculo',
         'cap_combustible_vehiculo',
         'marca_vehiculo',
         'modelo_vehiculo',
      )
      exclude = ('tipo_combustible',)

      


class GpoElectForm(forms.ModelForm):
   nombre_gpo_elect = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label="Nombre:", required=True)
   cant_combustible_gpo_elect = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}), label="Cant Combustible:", required=True)
   cap_combustible_gpo_elect = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}), label="Cap Combustible:", required=True)

   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      for form in self.visible_fields():
         form.field.widget.attrs['class'] = 'form-control'
   
   def clean(self):
      super().clean()
      cant_combustible_gpo_elect = self.cleaned_data['cant_combustible_gpo_elect']
      cap_combustible_gpo_elect = self.cleaned_data['cap_combustible_gpo_elect']

      if cant_combustible_gpo_elect > cap_combustible_gpo_elect:
         self.add_error('cant_combustible_gpo_elect', forms.ValidationError("La cantidad de combustible, no puede ser mayor a la capacidad del vehiculo."))
      


   class Meta:
      model = GpoElectr
      fields = (
         'nombre_gpo_elect',
         'cant_combustible_gpo_elect',
         'cap_combustible_gpo_elect',
         'marca_gpo_elect',
         'modelo_gpo_elect',
      )
      exclude = ('tipo_combustible',)
      

class LogisticaEqComForm(forms.ModelForm):


   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      for form in self.visible_fields():
         form.field.widget.attrs['class'] = 'form-control'
      self.empty_permitted = False

   class Meta:
      model = EqCom
      fields = ['nombre']
      labels = {
         "nombre": "Equipo Com"
      }



LogisticaEqComFormset = formset_factory(LogisticaEqComForm, extra=1)


class CombusVehiculo(forms.ModelForm):

   cant_combustible_vehiculo = forms.IntegerField(
      widget=forms.NumberInput(
         attrs={
            'type': 'range', 
            'class': 'custom-range custom-range-teal slider-range'}),
      label='Combustible Vehiculo',
      required=False)


   def __init__(self, *args, **kwargs):
      instance = kwargs.get('instance', None)
      super(CombusVehiculo, self).__init__(*args, **kwargs)

      if instance:
         capacitiy = instance.cap_combustible_vehiculo
         quantity = instance.cant_combustible_vehiculo
         self.fields['cant_combustible_vehiculo'].widget.attrs.update({
            'value': quantity,
            'max': capacitiy,
            'min': '0',
            'id': 'vehiculoCantCombus{}'.format(instance.id)})


   class Meta:
      model = Vehiculo
      fields = (
         'cant_combustible_vehiculo',
      )
      exclude = (
         'nombre_vehiculo',
         'marca_vehiculo',
         'modelo_vehiculo',
         'tipo_combustible',
         'cap_combustible_gpo_elect',
      )



class CombusGpoElect(forms.ModelForm):

   cant_combustible_gpo_elect = forms.IntegerField(
      widget=forms.NumberInput(
         attrs={
            'type': 'range', 
            'class': 'custom-range custom-range-teal slider-range'}),
      label='Combustible Gpo Electr',
      required=False)


   def __init__(self, *args, **kwargs):
      instance = kwargs.get('instance', None)
      super(CombusGpoElect, self).__init__(*args, **kwargs)

      if instance:
         capacitiy = instance.cap_combustible_gpo_elect
         quantity = instance.cant_combustible_gpo_elect
         self.fields['cant_combustible_gpo_elect'].widget.attrs.update({
            'value': quantity,
            'max': capacitiy,
            'min': '0',
            'id': 'gpoElectCantCombus{}'.format(instance.id)})


   class Meta:
      model = GpoElectr
      fields = (
         'cant_combustible_gpo_elect',
      )
      exclude = (
         'nombre_gpo_elect',
         'marca_gpo_elect',
         'modelo_gpo_elect',
         'tipo_combustible_gpo_elect',
         'cap_combustible_gpo_elect',
      )


class EventoForm(forms.ModelForm):
   tipo = forms.ModelChoiceField(
      queryset=TipoEvento.objects.all().prefetch_related('subtipos'), 
      widget=forms.Select(attrs={'class': 'form-control select2'}),
      label='Tipo:',)
   
   subtipo = forms.ModelChoiceField(
      queryset=SubTipoEvento.objects.all().select_related('tipo'), 
      widget=forms.Select(attrs={'class': 'form-control select2'}),
      label='Subtipo:',)

   description = forms.CharField(
      widget=forms.Textarea(attrs={'class': 'form-control', 'rows': "4"}),
      label='Descripción:',)


   class Meta:
      model = Evento
      fields = (
         'description',
         'tipo',
         'subtipo',
      )


class SensorForm(forms.ModelForm):

   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      for form in self.visible_fields():
         form.field.widget.attrs['class'] = 'form-control'

   class Meta:
      model = Sensor
      fields = (
         'nombre',
         'indicador',
      )
      exclude = (
         'facilidad',
      )