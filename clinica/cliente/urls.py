from django.urls import path
from .views import ClienteAPIView, ClienteDetailAPIView
# from clinicaEstetica.views import 

urlpatterns = [
    path("clienteapi/",ClienteAPIView.as_view(), name="clienteapi"),
    path("alterarCliente/<str:username>/",ClienteDetailAPIView.as_view(), name="alterarCliente"),
    # path("login/", login_usuario, name="login"), 
    # path('index/', views.indexCliente, name='indexCliente'),
    # path('adicionarCliente/', views.add_cliente, name='adicionarCliente'),
    # path('editar/<str:username>/', views.editarDadosCliente, name='editar'),
    # path('verPerfil/<str:username>/', views.verPerfil, name='verPerfil'),
    # path('alterarSenha/<str:username>/', views.editSenha, name="alterarSenha"),
    # path("logout/", views.realizarLogout, name="logout"),
    # path('excluirConta/<str:username>/', views.deletarContaCliente, name='excluirConta'),
    # path('marcarServico/', views.marcarServico, name='marcarServico'),
    # path('mostrarCategoria/', views.mostrarCategoria, name='mostrarCategoria'),
    # path("redirecionaParaIndexClinica/", views.redirecionaParaIndexClinica, name = "redirecionaParaIndexClinica"),

]