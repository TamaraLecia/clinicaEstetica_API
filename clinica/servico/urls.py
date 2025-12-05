from django.urls import path 
from .import views
from .views import ServicoAPIView, CategoriaAPIView, AlterarServicoAPIView, AgendamentoAPIView, AgendamentoDetailAPIView

urlpatterns = [
    path("", ServicoAPIView.as_view(), name="indexServicoAPI"),
    path("categoriaApi/", CategoriaAPIView.as_view(), name="categoriaApi"),
    path("alterarServico/<int:id>/", AlterarServicoAPIView.as_view(), name="alterarservicoApi"),
    path("agendarServico/", AgendamentoAPIView.as_view(), name="agendarServico"),
    path("agendarAlterarServico/<int:id>/", AgendamentoDetailAPIView.as_view(), name="agendarAlterarServico")
    # path("addServico/", views.addServico, name="addServico"),
    # path("alterarServico/<int:id>/", views.alterarServico, name="alterarServico"),
    # path("deletarServico/<int:id>/", views.deletarServico, name="deletarServico"),
    # # path("addCategoria/",views.addCategoria, name="addCategoria"),
    # path("alterarCategoria/<int:id>/", views.alterarCategoria, name="alterarCategoria"),
    # path("deletarCategoria/<int:id>/", views.deletarCategoria, name="deletarCategoria"),
    # #path("mostrarCategoria/", views.mostrarCategoria, name="mostrarCategoria"),
    # path("redirecionaParaAdministrador/", views.redirecionarParaAdministrador, name='redirecionaParaAdministrador'),

]
