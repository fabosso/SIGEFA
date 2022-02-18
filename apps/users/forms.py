from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):


   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      for form in self.visible_fields():
         form.field.widget.attrs['class'] = 'form-control'
      self.fields['grado'].required = True
      self.fields['rol'].required = True
      self.fields['first_name'].required = True
      self.fields['last_name'].required = True

   class Meta:
      model = User
      fields = (
         'username', 
         'first_name', 
         'last_name',
         'grado',
         # 'turno',
         'rol',
      )
