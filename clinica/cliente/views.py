

from cliente.models import Cliente
# from cliente.forms import AgendarServicoForm, ClienteForm, EditClienteForm
# from servico.utils import mostrarCategoria
# from cliente.forms import AgendarServicoForm, ClienteForm, EditClienteForm, SenhaForm
# from clinicaEstetica.forms import AdicionarUsuarioForm, EditUsuarioForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from servico.models import TipoServico
from django.contrib.auth import get_user_model, logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.models import Group
from django.urls import reverse

from rest_framework.views import APIView
from .serializer import ClienteSerializer, AlterarSenhaSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

# Create your views here.

class ClienteAPIView(APIView):
    # permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
        # permite o acesso sem login
    permission_classes = [AllowAny]
    # permite usuários não autenticado
    authenticatication_classes = []

    #ver todos os clientes
    def get(self, request):
        clientes = Cliente.objects.all()
        serializer = ClienteSerializer(clientes, many=True)
        return Response(serializer.data)
    
    #adicionar cliente
    def post(self, request):
        serializer = ClienteSerializer(data=request.data)
        if serializer.is_valid():
            cliente = serializer.save()
            cliente.identificador = 'cliente'
            cliente.save()

            grupo, _ = Group.objects.get_or_create(name='Clientes')
            cliente.user.groups.add(grupo)
            print("Cliente promovido a cliente:", cliente.nome)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class ClienteDetailAPIView(APIView):
    # permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    #     # permite o acesso sem login
    # permission_classes = [AllowAny]
    # # permite usuários não autenticado
    # authenticatication_classes = []
    
    def get(self, request, username):
        cliente = get_object_or_404(Cliente.objects.all(), username=username)
        serializer = ClienteSerializer(cliente)
        return Response(serializer.data)
    
    #Update
    def put(self, request, username):
        cliente = get_object_or_404(Cliente.objects.all(), user__username=username)
        serializer = ClienteSerializer(cliente, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    #Delete
    def delete(self, request, username):
        cliente = get_object_or_404(Cliente.objects.all(), user__username=username)
        cliente.user.delete()
        cliente.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AlterarSenhaAPIView(APIView):
    # permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    
    def put(self, request):
        serializer = AlterarSenhaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Senha alterada com sucesso."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# #Read
# def indexCliente(request):
#     contexto = mostrarCategoria()
#     return render(request, 'cliente/indexCliente.html', contexto)

# #Adicionar Cliente
# # @permission_required('cliente.add_cliente', raise_exception=True)
# def add_cliente(request):
#     form_user = AdicionarUsuarioForm(request.POST or None)
#     form = ClienteForm(request.POST or None)
#     if form_user.is_valid() and form.is_valid():
#         user_cliente = form_user.save()
#         cliente = form.save(commit=False)
#         cliente.user = user_cliente
#         cliente.identificador = 'cliente'
#         cliente.save()

#     #Adiciona o usuário ao grupo cliente -----------------------

#         nomeGrupo = cliente.identificador
#         grupo, _ = Group.objects.get_or_create(name='Clientes')
#         user_cliente.groups.add(grupo)
#         print("Cliente promovido a cliente:", cliente.nome)

#     #-----------------------------------------------------------------
#         #Realizando a autenticação do cliente, após ele realizar o login
#         cliente_autenticado = authenticate(request, username=user_cliente.username, password=form_user.cleaned_data['password1']
# )


#         if cliente_autenticado:
#             login(request, cliente_autenticado)
#             print("autenticado:")
#         return redirect('indexCliente')
#     return render(request, 'cliente/criarContaForm.html', {'form_user': form_user, 'form': form})

# #Read com condição
# @permission_required('cliente.detail_cliente', raise_exception=True)
# def verPerfil(request, username):
#     cliente = Cliente.objects.get(user__username=username)
#     userCliente = cliente.user

#     return render(request, 'cliente/verPerfil.html', {'user' : userCliente, 'cliente' : cliente})


# #Update
# @login_required
# @permission_required('cliente.change_cliente', raise_exception=True)
# def editarDadosCliente(request, username):
#     cliente = get_object_or_404(Cliente, user__username=username)
#     user = cliente.user
    
#     editarUserForm = EditUsuarioForm(request.POST, instance=user)
#     editarClienteForm = EditClienteForm(request.POST, instance=cliente)

#     if request.method == 'POST':
#         if editarUserForm.is_valid() and editarClienteForm.is_valid():
#             editarUserForm.save()
#             editarClienteForm.save()
#             return redirect('verPerfil')

#     return render(request, 'cliente/addClienteForm.html', {'editarUserForm' : editarUserForm, 'editarClienteForm' : editarClienteForm, 'cliente' : cliente} )


# #Delete
# @permission_required('cliente.delete_cliente', raise_exception=True)
# def deletarContaCliente(request, username):
#     apagarCliente = get_object_or_404(Cliente, user__username=username)

#     clienteUser = apagarCliente.user
#     apagarCliente.delete()
#     clienteUser.delete()
#     return redirect('indexClinica')

# # Agendar Servico
# # EditUsuarioForm
# @login_required
# def marcarServico(request):
#     formCliente = EditUsuarioForm(request.POST or None)
#     formAgendaServico = AgendarServicoForm(request.POST or None)
#     if formCliente.is_valid() and formAgendaServico.is_valid():
#         clienteForm = formCliente.save()
#         agendaServicoForm = formAgendaServico.save(commit=False)
#         agendaServicoForm.user = clienteForm
#         agendaServicoForm.save()
#         formAgendaServico.save_m2m()
#         return redirect('indexClinica')
#     else:
#         return render(request, 'cliente/agendarForm.html', {'formCliente': formCliente, 'formAgendaServico': formAgendaServico})
    

# # Mostrar fotos de categoria
# def mostrarFotosCategoria(request):
#     servicos = {}
#     servicos.update(mostrarCategoria())
#     return render(request,'clinicaEstetica/indexClinica.html', servicos)


# from collections import defaultdict

# # def mostrarCategoria():
# #     categorias = TipoServico.objects.values_list('categoria', flat=True).distinct()
# #     servicoPorCategoria = defaultdict(list)

# #     for categoria in categorias:
# #         servicos = TipoServico.objects.filter(categoria=categoria)
# #         servicoPorCategoria[categoria].extend(servicos)

# #     return {'servicoPorCategoria': dict(servicoPorCategoria)}


# # def mostrarTodasImagens(request):
# #     imagens = TipoServico.objects.all()
# #     return render(request, 'cliente/indexCliente.html', {
# #         'imagens': imagens
# #     })


# def mostrarCategoria():
#     # Essa linha retorna para a variavél categorias os valores do atrbuto
#     # categoria, onde flat=True tranforma os valores retornados pela a lista
#     # em uma lista simples, e o distinc não permite que valores iguais entre
#     # na lista.
#     categorias = TipoServico.objects.values_list('categoria', flat=True).distinct()
#     # Essa linha cria um dicionário vázio
#     servicoPorCategoria = {}

#     for categoria in categorias:
#         servico = TipoServico.objects.filter(categoria=categoria).first()
#         if servico:
#             servicoPorCategoria[categoria] = servico
#     return {'servicoPorCategoria': servicoPorCategoria}

# #alterar senha do cliente
# @permission_required('cliente.change_cliente', raise_exception=True)
# def editSenha(request, username):
#     User = get_user_model()
#     if request.user.is_authenticated:
#         verificarUsuario = Cliente.objects.filter(user__username=username).first()
#         if verificarUsuario and request.user.username == verificarUsuario.user.username:
#             if request.method == 'GET':
#                 clientes = User.objects.all()
#                 cliente= Cliente.objects.filter(user__username=username).first()
#                 formSenha = SenhaForm(instance=cliente)

#                 return render(request, 'cliente/senhaForm.html', {'formSenha' : formSenha ,'clientes': clientes})
                
#             elif request.method == 'POST':
#                 clientes = User.objects.all()
#                 cliente = Cliente.objects.get(user__username=username)
#                 formSenha = SenhaForm(request.POST, instance=cliente)

#                 if formSenha.is_valid():
#                     formSenha.save()
                        
#                     return redirect('indexCliente')
#                 else:
#                     pessoas = User.objects.all()
        
#                     return render(request, 'cliente/senhaForm.html')
#         else:
#             messages.error(request, "Não é possivél alterar a senha de outro usuário")
#             return redirect('indexCliente')
        

# #realizar logout
# @login_required
# def realizarLogout(request):
#     logout(request)
#     return redirect('indexClinica')

# #Redireciona para a pagina clinicaEstetica
# def redirecionaParaIndexClinica(request):
#     return redirect(reverse('indexClinica'))
