from django.urls import path 
from .import views
from .views import ServicoAPIView 

urlpatterns = [
    path("index/", ServicoAPIView.as_view(), name="indexServico"),
    path("addServico/", views.addServico, name="addServico"),
    path("alterarServico/<int:id>/", views.alterarServico, name="alterarServico"),
    path("deletarServico/<int:id>/", views.deletarServico, name="deletarServico"),
    # path("addCategoria/",views.addCategoria, name="addCategoria"),
    path("alterarCategoria/<int:id>/", views.alterarCategoria, name="alterarCategoria"),
    path("deletarCategoria/<int:id>/", views.deletarCategoria, name="deletarCategoria"),
    #path("mostrarCategoria/", views.mostrarCategoria, name="mostrarCategoria"),
    path("redirecionaParaAdministrador/", views.redirecionarParaAdministrador, name='redirecionaParaAdministrador'),

]
