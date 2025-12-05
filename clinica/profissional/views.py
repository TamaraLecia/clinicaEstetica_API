from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django.contrib.auth import get_user_model, logout
from django.contrib import messages
from clinicaEstetica.forms import AdicionarUsuarioForm, EditUsuarioForm
from profissional.models import Profissional
from profissional.forms import EditProfissionalForm, ProfissionalForm, SenhaForm
from django.contrib.auth.decorators import login_required, permission_required

from rest_framework.views import APIView
from .serializers import ProfissionalSerializer
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class ProfissionalAPIView(APIView):
    # VER todos os profissionais
    def get(self, request):
        profissionais = Profissional.objects.all()
        serializer = ProfissionalSerializer(profissionais, many=True)
        return Response(serializer.data)
    
    # Adiciona profissionais
    def post(self, request):
        serializer = ProfissionalSerializer(data=request.data)
        if serializer.is_valid():
            profissional = serializer.save()
            profissional.identificador = "profissional"
            profissional.save()

            grupo, _ = Group.objects.get_or_create(name='Profissionais')
            profissional.user.groups.add(grupo)

            mensagem = {"mensagem": "Profissional cadastrado com sucesso"}

            return Response({
                "profissional": serializer.data, **mensagem
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @login_required()
# @permission_required('profissional.view_profissional', raise_exception=True)
# def index(request):
#      profissionais = Profissional.objects.all()
#      usuario = User.objects.all()

#      contexto = {
#          'profissionais' :profissionais,
#          'title' :'Listas de profissionais',
#          'usuario' : usuario
#      }
#      return render(request, 'profissional/verPerfil.html', contexto)

# #criar profissional
# @permission_required('profissional.add_profissional', raise_exception=True)
# def add_profissional(request):
#     form_user = AdicionarUsuarioForm(request.POST or None)
#     form = ProfissionalForm(request.POST or None)
#     if form_user.is_valid() and form.is_valid():
#         user_profissional = form_user.save()
#         profissional = form.save(commit=False)
#         profissional.user = user_profissional
#         profissional.identificador = 'profissional'
#         profissional.save()

#     #Adiciona o usuário ao grupo Profissional -----------------------

#         nomeGrupo = profissional.identificador
#         grupo, _ = Group.objects.get_or_create(name='Profissionais')
#         user_profissional.groups.add(grupo)
#         print("Profissional promovido a profissional:", profissional.nome)

#     #-----------------------------------------------------------------

#         return redirect(reverse('indexAdm'))
#     return render(request, 'profissional/profissionalForm.html', {'form_user': form_user, 'form': form})

# #alterar informações
# @permission_required('profissional.change_profissional', raise_exception=True)


# @login_required
# def editarDadosProfissional(request):
#     user = request.user
#     profissional = get_object_or_404(Profissional, user=user)

#     if request.method == 'POST':
#         editarUserForm = EditUsuarioForm(request.POST, instance=user)
#         editarProfissionalForm = EditProfissionalForm(request.POST, instance=profissional)

#         if editarUserForm.is_valid() and editarProfissionalForm.is_valid():
#             editarUserForm.save()
#             editarProfissionalForm.save()
#             return redirect('verProfissional')
#     else:
#         editarUserForm = EditUsuarioForm(instance=user)
#         editarProfissionalForm = EditProfissionalForm(instance=profissional)

#     return render(request, 'profissional/profissionalForm.html', {
#         'editarUserForm': editarUserForm,
#         'editarProfissionalForm': editarProfissionalForm,
#         'profissional': profissional
#     })        
# #Editar senha
# @permission_required('profissional.change_profissional', raise_exception=True)
# def editSenha(request, username):
#     User = get_user_model()
#     if request.user.is_authenticated:
#         verificarUsuario = Profissional.objects.filter(user__username=username).first()
#         if verificarUsuario and request.user.username == verificarUsuario.user.username:
#             if request.method == 'GET':
#                 profissionais = User.objects.all()
#                 profissional= Profissional.objects.filter(user__username=username).first()
#                 formSenha = SenhaForm(instance=profissional.user)

#                 return render(request, 'profissional/senhaForm.html', {'formSenha' : formSenha ,'profissionais': profissionais})
                
#             elif request.method == 'POST':
#                 profissionais = User.objects.all()
#                 profissional = Profissional.objects.get(user__username=username)
#                 formSenha = SenhaForm(request.POST, instance=profissional.user)

#                 if formSenha.is_valid():
#                     formSenha.save()
                        
#                     return redirect('verProfissional')
#                 else:
#                     administradores = User.objects.all()
        
#                     return render(request, 'profissional/senhaForm.html')
#         else:
#             messages.error(request, "Não é possivél alterar a senha de outro usuário")
#             return redirect('verProfissional')


# #Ver Profissionais detalhes de profissionais
# @login_required()
# @permission_required('profissional.detail_profissional', raise_exception=True)
# def verProfissional (request):
#     #pega o profissional pelo o username
#     user = request.user
#     profissional= Profissional.objects.get(user=user)
#     userProfissional = profissional.user

#     return render(request, 'profissional/verPerfil.html', {'user' : userProfissional, 'profissional' : profissional})

# # Apagar profissional

# @login_required()
# def deletarContaProfissional(request, username):
#     #pega o profissional pelo o username
#     apagarProfissional= get_object_or_404(Profissional, user__username =username)
  
#     profissionalUser = apagarProfissional.user
#     apagarProfissional.delete()
#     profissionalUser.delete()
#     return redirect(reverse('indexAdm'))


# #Redireciona para a pagina clinicaEstetica
# def redirecionaParaIndexClinica(request):
#     return redirect(reverse('indexClinica'))


# #realizar logout
# @login_required
# def realizarLogout(request):
#     logout(request)
#     return redirect('indexClinica')