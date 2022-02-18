from django.urls import path
from django.contrib.auth import views


from .views import SignupPageView, RegistrarPersonal, UserLogin


app_name = 'users'

urlpatterns = [
   path('signup/', SignupPageView.as_view(), name='signup'),
   path('facilidad/<int:pk>/personal/', RegistrarPersonal.as_view(), name='personal_section'),
   path('', UserLogin.as_view(), name='login'),
]

