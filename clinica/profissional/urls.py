from django.urls import path
from . import views 
from .views import ProfissionalAPIView, ProfissionalDetail

urlpatterns = [
    # path("index/", views.index, name="indexProfissional"),
    path('profissionalApi/', ProfissionalAPIView.as_view(), name="profissionalApi"),
    path('profissionalDetail/<str:username>/', ProfissionalDetail.as_view(), name="profissionalDetailApi"),
    # path("criarProfissional/", views.add_profissional, name="criarProfissional"),
    # path('deletarContaProfissional/', views.deletarContaProfissional, name='deletarContaProfissional'),
    # path('alterarSenha/<str:username>/', views.editSenha, name='alterarSenha'),
    # path("editarDadosProfissional/", views.editarDadosProfissional, name="editarDadosProfissional"),
    # path("verProfissional/", views.verProfissional, name="verProfissional"),
    # path("redirecionaParaIndexClinica/", views.redirecionaParaIndexClinica, name = "redirecionaParaIndexClinica"),
    # path("logout/", views.realizarLogout, name="lougout"),
    # path('excluirConta/<str:username>/', views.deletarContaProfissional, name='excluirConta'),
]