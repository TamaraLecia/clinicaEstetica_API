from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response

# Create your views here.
# view criada para guarda o refresh tokén por meio de cookies

class AutenticacaoCustomizada(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        # age como o TokenObtainPairView
        response = super().post(request, *args, **kwargs)
        data = response.data

        # refresh tokén com o cookie para dar mais segurança
        # adiciona um cookie na resposta HTTP
        response.set_cookie(
            # nome do cookie
            key = 'refresh_token',
            # o valor do cookie é o refresh_tokén que foi passado para a variável data
            value = data['refresh'],
            # impede o acesso via document.cookie no navegador, dificultando ataque por XSS
            httponly = True,
            # Não permite que o browser envie cookie em requisições cross-site
            samesite = 'Strict',
            # tempo de validade do cookie
            max_age = 7*24*60*60
        )

        # tira o refresh do corpo da resposta, devolvendo só o acess
        del data['refresh']
        response.data = data
        return response