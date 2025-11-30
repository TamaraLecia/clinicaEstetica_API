#importações utilizadas de Api
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import AdministradorSerializer, AlterarCategoriaSerializer, AlterarSenhaSerializer, MostrarServicoSerializer, VerClienteSerializer, VerPlanoSerializer, VerProfissionalSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, permissions

# importações do oauth2 - oauth-toolkit
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
# Create your views here.

#usando APIView do rest_framework
class AdministradorAPIView(APIView):
    # forma de realizar a authenticação com oauth-toolkit
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

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
            administrador.groups.add(grupo)
            print("Administrador promovido a administrador:", administrador.nome)

            tornarAdmin(request, administrador.username)
            print("Administrador salvo:", administrador.id)
            return Response(serializer.data)

class AdministradorDetail(APIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    
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
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def put(self, request):
        serializer = AlterarSenhaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.errors, status=400)

class VerProfissional(APIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]

    def get(self, request):
        profissionais = Profissional
        serializer = VerProfissionalSerializer(profissionais, many=True)
        return Response(serializer.data)

class MostrarServico(APIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]

    def get(self, request):
        servicos = Servico
        serializer = MostrarServicoSerializer(servicos, many=True)
        return Response(serializer.data)
    
class ServicoDetail(APIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

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
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def put(self, request, id):
        categoria = get_object_or_404(TipoServico.objects.all(), id=id)
        serializer = AlterarCategoriaSerializer(categoria, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

class VerCliente(APIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]

    def get(self, request):
        clientes = Cliente
        serializer = VerClienteSerializer(clientes, many=True)
        return Response(serializer.data)

class VerPlano(APIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]

    def get(self, request):
        planos = Plano
        serializer = VerPlanoSerializer(planos, many=True)
        return Response(serializer.data)
    
def tornarAdmin(request, userName): 
    administrador = get_object_or_404(User, username = userName) 
    if administrador.is_superuser: 
        messages.error(request, "Você já é um Administrador") 
        
    else: 
        administrador.is_superuser = True #Transforma o administrador em superUsuário 
        administrador.is_staff = True #Permite que o usuário acesse o painel de administração do django 
        administrador.save() 
        messages.success(request, "Usuário promovido a administrador") 
    
    return redirect('indexAdm')