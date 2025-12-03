from django.urls import path
from .views import AutenticacaoCustomizada

urlpatterns = [
    path('token/', AutenticacaoCustomizada.as_view(), name='token_obtain_pair')
]