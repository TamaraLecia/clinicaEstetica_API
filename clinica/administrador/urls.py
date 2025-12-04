from .import views
from django.urls import path

urlpatterns = [
    path('', views.AdministradorAPIView.as_view(), name="AdministradorApiView"),
    path('primeiroCadastroAdmin/', views.primeiroAdministradorAPIView.as_view(), name="PrimeiroCadastroAdmin"),
    path('administradorDetail/<int:id>/', views.AdministradorDetail.as_view(), name="AdministradorDetail"),
    path('alterarSenha/', views.AlterarSenha.as_view(), name="AlterarSenha"),
    path('verProfissional/', views.VerProfissional.as_view(), name="VerProfissional"),
    path('mostrarServico/', views.MostrarServico.as_view(), name="MostrarServico"),
    path('ServicoDetail/<int:id>/', views.ServicoDetail.as_view(), name="ServicoDetail"),
    path('alterarCategoria/', views.AlterarCategoria.as_view(), name="AlterarCategoria"),
    path('verCliente/', views.VerCliente.as_view(), name="VerCliente"),
    path('VerPlano/', views.VerPlano.as_view(), name="VerPlano"),
]