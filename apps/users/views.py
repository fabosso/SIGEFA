from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, View
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm

from apps.ecr.models import Facilidad



class SignupPageView(SuccessMessageMixin, CreateView):
   form_class = CustomUserCreationForm
   success_url = reverse_lazy('login')
   template_name = 'registration/signup.html'
   success_message = "Usuario %(username)s creado satisfactoriamente. Deberá esperar confirmacion por el administrador para poder ingresar."


class RegistrarPersonal(View):
   template_name = 'personal_section.html'
   facilidad = None

   def dispatch(self, request, pk, *args, **kwargs):
      self.facilidad = get_object_or_404(Facilidad, pk=pk)

      return super(RegistrarPersonal, self).dispatch(self.request, pk)

   def get(self, request, pk, *args, **kwargs):
      
      ctx = {
         'section': 'Personal',
         'facilidad_id': self.facilidad.id,
         'form': CustomUserCreationForm(),
         'personal_list': self.facilidad.operadores_en_facilidad.all()
      }

      return render(self.request, self.template_name, ctx)

   def post(self, *args, **kwargs):
      data = dict()
      try:
         form = CustomUserCreationForm(self.request.POST)

         if form.is_valid():
            instance = form.save(commit=False)
            instance.facilidad = self.facilidad
            instance.save()

            personal_list = self.facilidad.operadores_en_facilidad.all()
            context = {'personal_list': personal_list}
            data['html_personal_list'] = render_to_string('personal_list.html', context)
            data['status'] = 200
            data['message'] = 'Usuario {}, fue creado de forma exitosa'.format(instance.username)
            
            return JsonResponse(data)
         return JsonResponse({'status': 400, 'errors': form.errors.as_json()})



      except Exception as e:
         return JsonResponse({'status': 500, 'error': str(e), 'message': 'Un error ha ocurrido.'})


class UserLogin(LoginView):
   template_name = 'registration/login.html'

   def dispatch(self, *args, **kwargs):
      if self.request.user.is_authenticated:
         return redirect('ecr:ecr_action_option')

      return super(UserLogin, self).dispatch(self.request)
