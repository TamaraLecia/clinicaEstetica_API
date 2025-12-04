// import axios from 'axios';

const formPrimeiroCadastroAdmin = document.getElementById('formPrimeiroAdmin');
const formCadastro = document.getElementById('formulario');
const formLogin = document.getElementById('formularioLogin');

if (formPrimeiroCadastroAdmin){
    formPrimeiroCadastroAdmin.addEventListener('submit', function(e){
        //permite que o formulário não recarregue após o seu envio.
        e.preventDefault();

        const formData = {
            //esse é o formato que a API está aceitando o user.
            //o user é nesse caso uma lista de arrays que contém as váriavéis esperadas pelo o django
            user:{
                username: document.getElementById('username').value,
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
            },
            nome: document.getElementById('nome').value
        };

        //o axios é o que possibilita eviar a requisição do javaScript puro para
        //a API django rest framework
        axios.post('http://localhost:8000/apiAdministrador/primeiroCadastroAdmin/', formData, {
            //envia os dados no formato json
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(function(res){
            alert("Cadastro realizado com sucesso!");
            console.log(res.data);
        })
        .catch(function(err){
            alert("Erro ao cadastrar: " + (err.response?.data?.detail || err.message));
        });
    });
}


if (formCadastro){
    formCadastro.addEventListener('submit', function(e){
        //permite que o formulário não recarregue após o seu envio.
        e.preventDefault();

        // pega o tokén que é criado quando o usuário realiza o login
        const token = sessionStorage.getItem("acessToken");

        const formData = {
            //esse é o formato que a API está aceitando o user.
            //o user é nesse caso uma lista de arrays que contém as váriavéis esperadas pelo o django
            user:{
                username: document.getElementById('username').value,
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
            },
            nome: document.getElementById('nome').value
        };

        //o axios é o que possibilita eviar a requisição do javaScript puro para
        //a API django rest framework
        axios.post('http://localhost:8000/apiAdministrador/', formData, {
            //envia os dados no formato json
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
            withCredentials: true
        })
        .then(function(res){
            alert("Cadastro realizado com sucesso!");
            console.log(res.data);
        })
        .catch(async function(err){
            if (err.response?.status === 401){
                //tenta renovar o tokén através da função refresh tokén criada aqui no JavaScript
                await refreshAccessToken();
                // tenta fazer o cadastro novamente
                return formCadastro.dispatchEvent(new Event('submit'));
            }
            alert("Erro ao cadastrar: " + (err.response?.data?.detail || err.message));
        });
    });
}

if(formLogin){
    formLogin.addEventListener('submit', async function(e){
        // não permite que a página recarregue após enviar as informações
        e.preventDefault();

        const username = document.getElementById('loginUsername').value;
        const password = document.getElementById('loginPassword').value;

        try{
            const response = await axios.post('http://localhost:8000/api/token/', {
                username,
                password
            },
            {
                headers : {"Content-Type": "application/json"},
                // O withCredentials permite enviar e receber cookies
                // ele está sendo utilizado aqui porque o refresh tokén
                // é armazenado em cookies
                withCredentials: true
            });
            const accessToken = response.data.access;

            //armazena o acess tokén (tokén de acesso) no navegador
            sessionStorage.setItem("acessToken", accessToken);

            // alert("Login reaalizado com sucesso");
            window.location.href = "/clinica/administrador/frontend/indexADM.html";
        }
        catch(err){
            alert("Erro ao realizar login: " +(err.responnse?.data?.detaill || err.message));
        }
    });
}

async function refreshAccessToken() {
    try{
        const response = await axios.post("http://localhost:8000/api/token/refresh", {}, {
            withCredentials: true
        });

        const novoAcesso = response.data.access;
        sessionStorage.setItem("acessToken", novoAcesso);
        console.log("Novo access token:", novoAcesso);
    }catch(err){
        alert("Sessão expirada. Faça login novamente");
    }
}
function mostrarAdministrador(){
    const token = sessionStorage.getItem("acessToken")

    axios.get('http://localhost:8000/apiAdministrador/', {
        headers: {
            Authorization: "Bearer " + token,
        }
    }).then(response => {
        // os dados da API vem no formato json
        const data = response.data;

        const container = document.getElementById("listAdmin");
        

    })
}