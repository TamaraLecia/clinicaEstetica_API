from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response

# Create your views here.
# view criada para guarda o refresh tokén por meio de cookies

class AutenticacaoCustomizada(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        data = response.data

        # refresh tokén com o cookie para dar mais segurança
        response.set_cookie(
            key = 'refresh_token',
            value = data['refresh'],
            httponly = True,
            samesite = 'Strict',
            max_age = 7*24*60*60
        )

        # tira o refresh do corpo da resposta, devolvendo só o acess
        del data['refresh']
        response.data = data
        return response