from django.shortcuts import get_object_or_404
from plano.models import Plano

#importações utilizadas de Api
from rest_framework.views import APIView
from .serializers import PlanoSerializer
from rest_framework.response import Response
from rest_framework import status
# , permissions

# importações do oauth2 - oauth-toolkit
# from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope

#Criar plano

class PlanoAPIView(APIView):
     # forma de realizar a authenticação com oauth-toolkit
    # permissions_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def get(self, request):
        planos = Plano.objects.all()
        serializer = PlanoSerializer(planos, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = PlanoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
class PlanoDetail(APIView):
     # forma de realizar a authenticação com oauth-toolkit
    # permissions_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def put(self, request, id):
        plano = get_object_or_404(Plano.objects.all(), id=id)
        serializer = PlanoSerializer(plano, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    
    #Delete
    def delete(self, request, id):
        plano = get_object_or_404(Plano.objects.all(), id=id)
        plano.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)








# from django.shortcuts import redirect, render
# from django.urls import reverse
# from plano.models import Plano
# from plano.forms import EditPlanoForm, PlanoForm
# from django.contrib.auth.decorators import permission_required

# # IMPORTAÇÕES DE API
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.parsers import MultiPartParser, FormParser
# from .serializer import PlanoSerializer
# from rest_framework import generics


# class PlanoAPIView(APIView):
#     parser_classes = [MultiPartParser, FormParser]

#     # LISTAR TODOS OS PLANOS
#     def get(self, request):
#         planos = Plano.objects.all()
#         serializer = PlanoSerializer(planos, many=True)
#         return Response(serializer.data)

#     # CRIAR UM NOVO PLANO
#     def post(self, request):
#         serializer = PlanoSerializer(data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 {
#                     "mensagem": "Plano criado com sucesso!",
#                     "plano": serializer.data
#                 },
#                 status=status.HTTP_201_CREATED
#             )

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # EDITAR um plano específico (GET, PUT, PATCH)
# class PlanoUpdateAPIView(generics.RetrieveUpdateAPIView):
#     queryset = Plano.objects.all()
#     serializer_class = PlanoSerializer
#     lookup_field = 'id'


# # DELETAR um plano específico
# class PlanoDeleteAPIView(generics.DestroyAPIView):
#     queryset = Plano.objects.all()
#     serializer_class = PlanoSerializer
#     lookup_field = 'id'


# # Criar plano
# @permission_required('plano.add_plano', raise_exception=True)
# def addPlano(request):
#     formPlano = PlanoForm(request.POST)

#     if formPlano.is_valid():
#         plano = formPlano.save(commit=False)
#         plano.save()
#         formPlano.save_m2m()
#         return redirect('indexPlano')

#     return render(request, 'plano/planoForm.html', {'formPlano': formPlano})


# # Ver planos
# def index(request):
#     return render(request, 'plano/indexPlano.html')


# # Editar planos
# @permission_required('plano.change_plano', raise_exception=True)
# def alterarPlano(request, id):
#     if request.method == 'GET':
#         planos = Plano.objects.all()
#         plano = Plano.objects.filter(pk=id).first()
#         formPlano = EditPlanoForm(instance=plano)

#         return render(request, 'plano/planoForm.html', {'formPlano': formPlano, 'planos': planos})

#     elif request.method == 'POST':
#         planos = Plano.objects.all()
#         plano = Plano.objects.get(pk=id)
#         formPlano = EditPlanoForm(request.POST, instance=plano)

#         if formPlano.is_valid():
#             formPlano.save()
#             return redirect('indexAdm')
#         else:
#             planos = Plano.objects.all()
#             return render(request, 'plano/planoForm.html')


# # Deletar planos
# @permission_required('plano.delete_plano', raise_exception=True)
# def deletarPlano(request, id):
#     form = Plano.objects.get(pk=id)
#     form.delete()
#     return redirect('indexAdm')


# # Redireciona para o painel de administrador
# def redirecionarParaAdministrador(request):
#     return redirect(reverse('indexAdm'))


# # Mostrar planos para cliente
# def mostrarPlano(request):
#     planos = Plano.objects.all()
#     return render(request, 'plano/__pricingStart.html', {'verPlano': planos})