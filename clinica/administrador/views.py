#importações utilizadas de Api
from pyexpat.errors import messages
from administrador.models import Administrador
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import AdministradorSerializer, AlterarCategoriaSerializer, AlterarSenhaSerializer, MostrarServicoSerializer, VerClienteSerializer, VerPlanoSerializer, VerProfissionalSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

# importações do oauth2 - oauth-toolkit
# from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
# Create your views here.

#usando APIView do rest_framework

# API para a primeira vez que criar um usuário no sistema
class primeiroAdministradorAPIView(APIView):
    # permite o acesso sem login
    permission_classes = [AllowAny]
    # permite usuários não autenticado
    authenticatication_classes = []

    def post(self, request):
        if User.objects.filter(is_superuser=True).exists():
            return Response(
                {"error": "Já existe um administrador cadastrado"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = AdministradorSerializer(data=request.data)
        if serializer.is_valid():
            administrador = serializer.save()
            administrador.identificador = 'administrador'
            administrador.save()

            # adiciona ao grupo de Administradores
            grupo, _= Group.objects.get_or_create(name='Administradores')
            administrador.user.groups.add(grupo)

            # chama a função de tornar Admin
            # chama a função tornar ADMIN
            msg = tornarAdmin(administrador.user.username)

            return Response({
                "administrador": serializer.data,
                **msg
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdministradorAPIView(APIView):
    # forma de realizar a authenticação com oauth-toolkit
    # permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    #ver todos os administradores
    def get(self, request):
        administradores = Administrador.objects.all()
        serializer = AdministradorSerializer(administradores, many=True)
        return Response(serializer.data)
    
    #adicionar administradores
    def post(self, request):
        serializer = AdministradorSerializer(data=request.data)
        if serializer.is_valid():
            administrador = serializer.save()
            administrador.identificador = 'administrador'
            administrador.save()

            grupo, _ = Group.objects.get_or_create(name='Administradores')
            administrador.user.groups.add(grupo)

            # chama a função tornar ADMIN
            msg = tornarAdmin(administrador.user.username)

            # retorna o objeto criado e a mensagem que está na função tornar ADMIN
            return Response({
                "administrador": serializer.data,
                **msg
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdministradorDetail(APIView):
    # permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    
    def get(self, request, id):
        administrador = get_object_or_404(Administrador.objects.all(), id=id)
        serializer = AdministradorSerializer(administrador)
        return Response(serializer.data)
    
    #Update
    def put(self, request, id):
        administrador = get_object_or_404(Administrador.objects.all(), id=id)
        serializer = AdministradorSerializer(administrador, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    
    #Delete
    def delete(self, request, id):
        administrador = get_object_or_404(Administrador.objects.all(), id=id)
        administrador.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AlterarSenha(APIView):
    # permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def put(self, request):
        serializer = AlterarSenhaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.errors, status=400)

class VerProfissional(APIView):
    # permission_classes = [permissions.IsAuthenticated, TokenHasScope]

    def get(self, request):
        profissionais = Profissional
        serializer = VerProfissionalSerializer(profissionais, many=True)
        return Response(serializer.data)

class MostrarServico(APIView):
    # permission_classes = [permissions.IsAuthenticated, TokenHasScope]

    def get(self, request):
        servicos = Servico
        serializer = MostrarServicoSerializer(servicos, many=True)
        return Response(serializer.data)
    
class ServicoDetail(APIView):
    # permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def put(self, request, id):
        servico = get_object_or_404(Servico.objects.all(), id=id)
        serializer = MostrarServicoSerializer(servico, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, id):
        servico = get_object_or_404(Servico.objects.all(), id=id)
        servico.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AlterarCategoria(APIView):
    # permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def put(self, request, id):
        categoria = get_object_or_404(TipoServico.objects.all(), id=id)
        serializer = AlterarCategoriaSerializer(categoria, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

class VerCliente(APIView):
    # permission_classes = [permissions.IsAuthenticated, TokenHasScope]

    def get(self, request):
        clientes = Cliente
        serializer = VerClienteSerializer(clientes, many=True)
        return Response(serializer.data)

class VerPlano(APIView):
    # permission_classes = [permissions.IsAuthenticated, TokenHasScope]

    def get(self, request):
        planos = Plano
        serializer = VerPlanoSerializer(planos, many=True)
        return Response(serializer.data)
    
def tornarAdmin(userName):
    administrador = get_object_or_404(User, username=userName)
    if administrador.is_superuser:
        return {"detail": "Usuário já é um Administrador"}
    else:
        administrador.is_superuser = True
        administrador.is_staff = True
        administrador.save()
        # retorna uma mensagem informando que o usuário foi promovido
        return {"detail": f"Usuário {userName} promovido a administrador"}