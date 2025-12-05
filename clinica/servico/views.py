from queue import Full
from django.shortcuts import redirect, render
from servico.models import Servico, TipoServico
from servico.forms import EditCategoriaForm, EditServicoForm, ServicoCategoriaForm, ServicoForm
from django.urls import reverse
from django.contrib.auth.decorators import permission_required

#IMPORTAÇÕES DE API
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import ServicoSerializer, CategoriaSerializer
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.parsers import MultiPartParser, FormParser

    # categorias = Servico.objects.values_list('categoria', flat=True).distinct()
    # servicoPorCategoria = {}


class ServicoAPIView(APIView):
    # faz com que a view aceite as requisições dos arquivos
    parser_classes = [MultiPartParser, FormParser]

    # permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    #ver todos os servicos
    def get(self, request):
        servicos = Servico.objects.all()
        serializer = ServicoSerializer(servicos, many=True)
        return Response(serializer.data)
    
    #adicionar servicos
    def post(self, request):
        serializer = ServicoSerializer(data=request.data)
        if serializer.is_valid():
            servico = serializer.save()
            mensagem = {"mensagem": "Serviço cadastrado com sucesso"}
            return Response({
                "servico": serializer.data, **mensagem}, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # servico.save()
            # return Response(serializer.data)

class CategoriaAPIView(APIView):
    # faz com que a view aceite as requisições dos arquivos
    parser_classes = [MultiPartParser, FormParser]

    # mostra as categorias cadastradas
    def get(self, request):
        categorias = TipoServico.objects.all()
        serializer = CategoriaSerializer(categorias,many=True)
        return Response(serializer.data)
    
    # adiciona as categorias
    def post(self, request):
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            categoria = serializer.save()
            mensagem = {"mensagem": "Categoria cadastrada com sucesso"}
            return Response({
                "categoria": serializer.data, **mensagem
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Editar categoria
    def put(self, request):
        serializer = CategoriaSerializer(data=request.data)
        if serializer.is_valid():
            categoria = serializer.save()
            mensagem = {"mensagem": "Categoria atualizada com sucesso"}
            return Response({
                "categoria": serializer.data, **mensagem
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# mostra as categorias de cada servico
# Ela tem como argumento o request, o template = '', que permite que
# a ela ser chamada em outros apps e exibir essas informações.
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

# Editar Categoria
@permission_required('servico.change_servico', raise_exception=True)
def alterarCategoria(request, id):
    if request.method == 'GET':
        categorias = TipoServico.objects.all()
        categoria = TipoServico.objects.filter(pk=id).first()
        formServico = EditCategoriaForm(instance=categoria)
        return render(request, 'servico/servicoForm.html', {'formServico': formServico, 'categorias': categorias})
    elif request.method == 'POST':
        categorias = TipoServico.objects.all()
        categoria = TipoServico.objects.get(pk=id)
        formServico = EditCategoriaForm(request.POST, request.FILES, instance=categoria)

        if formServico.is_valid():
            formServico.save()
            return redirect('indexServico')
        else:
            categorias = TipoServico.objects.all()
            return render(request, 'servico/servicoForm.html')
        
# Deletar Categoria
@permission_required('servico.delete_servico', raise_exception=True)
def deletarCategoria(request, id):
    categoria = TipoServico.objects.get(pk=id)
    categoria.delete()


# Adicionar Serviço
@permission_required('servio.add_servico', raise_exception=True)
def addServico(request):
    formServico = ServicoForm(request.POST, request.FILES)

    print(formServico.errors)
    if formServico.is_valid():
        servico = formServico.save(commit=False)
        servico.save()
        return redirect('indexServico')
    return render(request, 'servico/servicoForm.html',{'formServico': formServico})      

#Editar servico
@permission_required('servico.change_servico', raise_exception=True)
def alterarServico(request, id):
    if request.method == 'GET':
        servicos = Servico.objects.all()
        servico = Servico.objects.filter(pk=id).first()
        formServico = EditServicoForm(instance=servico)

        return render(request, 'servico/servicoForm.html',{'formServico': formServico, 'servicos': servicos})
    
    elif request.method == 'POST':
        servicos = Servico.objects.all()
        servico = Servico.objects.get(pk=id)
        formServico = EditServicoForm(request.POST, request.FILES, instance=servico)


        if formServico.is_valid():
            formServico.save()
            return redirect('indexServico')
        else:
            servicos = Servico.objects.all()
            return render(request, 'servico/servicoForm.html')


#Deletar Servico
@permission_required('servico.delete_sevico', raise_exception=True)
def deletarServico(request, id):
    servico = Servico.objects.get(pk=id)

    servico.delete()
    return redirect('indexServico')

#Redireciona para o painel de administrador
def redirecionarParaAdministrador(request):
    return redirect(reverse('indexAdm'))