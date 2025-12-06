*Integrantes do grupo:* 

Lecia Tamara Ferreira dos Santos Ribeiro \- 2021GBI02GT0021  
Leomira de Oliveira Couto \- 2022GBI02GT0011  
Tamara Lécia Ferreira dos Santos Ribeiro \- 20211GBI02GT0027


✅ Instruções de Uso do Sistema

Clone o projeto do GitHub, utilizando o link abaxo: https://github.com/TamaraLecia/clinicaEstetica_API.git

Após clonar o projeto acesse o seu editor de código e instale estas ferramentas necessárias para o funcionamento da API no django

✅ Ferramentas necessárias para utilizar a API: 

Devem ser instaladas na pasta do projeto
Python 3.12+
pip (gerenciador de pacotes)
Virtualenv
Django 5.2.3
Django REST Framework
drf-yasg (Swagger)
django-cors-headers
 Já instalado no django por padrão.
SQLite (padrão)
		
✅ Acesso da API pelo Navegador

Para acessar o frontend da API no navegador tem que abrir o arquivo index.html na pasta frontend que está dentro da pasta clínica técnica, antes de executar o index.html com o liver server é necessário rodar o terminal do django com o comando python3 manage.py runserver.
Agora com o servidor do django ligado é possível acessar os recursos da API
Caso não tenha um administrador pode criá-lo clicando no botão criar conta e respondendo o formulário.
Após criar o administrador, o usuário tem acesso às funcionalidades da API, de serviço, profissionais, planos e a as funcionalidades da própria API de questionário.
Após o primeiro administrador criado os demais são criados a partir dele

Após o cadastro do administrador, quando ele for entrar novamente ele tem que passar o nome de usuário ou seja o username  e a senha.


✅ Acesso da API pelo o Postman
Para acessar a api pelo o postman é necessário passar no cabeçalho a chave: 

Authorization que recebe o valor Bearer e o access token, retornado pelo método POST após passar a url http://127.0.0.1:8000/api/token/ que retorna o refresh token e o token.

Após obter o token, pode ser passada a url da API desejada.
URLs do sistema:

Para adicionar o  primeiro adminidtrador: 
'http://localhost:8000/apiAdministrador/primeiroCadastroAdmin/

Para adicionar os demasis administradores
http://localhost:8000/apiAdministrador/


Para utilizar o refresh token

	http://localhost:8000/api/token/refresh

Para mostrar os administradores
http://localhost:8000/apiAdministrador/

Para editar um administrador específico e para  deletar

http://localhost:8000/apiAdministrador/administradorDetail/${username}/

Para alterar a senha do adminidtrador
http://localhost:8000/apiAdministrador/alterarSenha/

	As Urls das APIs dos outros modelos pode ser acessada no arquivo ursl.py de cada modelo e o arquivo as Urls principais são encontradas no arquivo urls.py da pasta clinicaConfig.

✅  Acesso da API pelo o Aplicativo desenvolvido utilizando o flutter

clone o projeto no GitHub pelo o link : https://github.com/LeciaTamara/ClinicaDeEsteticaAPP.git

Instalar essas ferramentas:

Dependências Flutter já listadas no pubspec.yaml:
	Flutter SDK (>= 3.9.0, conforme pubspec.yaml)
Dart SDK
Android Studio ou VS Code
Emulador Android ou dispositivo físico
http,
 mobx, 
flutter_mobx, 
get_it, 
sqflite, 
intl,
 mask_text_input_formatter, 
flutter_secure_storage

Executar o comando flutter pub get
Acessar o arquivo api_config.dart na pasta app/api_config/, este arquivo serve para adaptar automaticamente o endereço da API conforme o ambiente em que o app está rodando (emulador, celular físico via USB, celular físico via Wi‑Fi, simulador iOS). Acesse o arquivo e realize a configuração de acordo com o método que será utilizado para rodar o aplicativo.

Após isso, coloque o servidor do django para rodar com o comando python3 manage.py runserver, e depois rode o projeto flutter com o comando flutter run
Quando o aplicativo abrir realize o cadastro de um cliente
Após o cadastro, realize o login com o username(nome de usuário) e senha cadastrada.

✅ A api desenvolvida possui a documentação swagger e a redoc do app drf_yasg, utilizado para documentar a api.
	Para ter acesso a essas duas documentação da API é preciso rodar o servidor django com o comando python3 manage.py runserver e acessar o navegador e passar a url da documentação

✅ Url da documentação do swagger: http://127.0.0.1:8000/swagger/
✅ Url da documentação do redoc: http://127.0.0.1:8000/redoc/

✅ Link da documentação da api no docs: https://docs.google.com/document/d/1XbAj1UJX3cTPF6rnIoI4_uAOJHT0BRvpnAtTXXS_L5A/edit?usp=sharing



