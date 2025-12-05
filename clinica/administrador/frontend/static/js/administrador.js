// import axios from 'axios';

const formPrimeiroCadastroAdmin = document.getElementById('formPrimeiroAdmin');
const formCadastro = document.getElementById('formulario');
const formLogin = document.getElementById('formularioLogin');
const formEditar = document.getElementById('editAdminformulario');
const formAlterarSenha = document.getElementById("senhaFormulario");

// pega o tokén que é criado quando o usuário realiza o login
const token = sessionStorage.getItem("acessToken");


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
             console.error("Erros do serializer:", err.response?.data);
            alert("Erro ao cadastrar: " + JSON.stringify(err.response?.data));
            // alert("Erro ao cadastrar: " + (err.response?.data?.detail || err.message));
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

// chama a função mostrarAdministrador
document.addEventListener("DOMContentLoaded", () => {
    mostrarAdministrador();
});

function mostrarAdministrador(){ 
    try{

        axios.get('http://localhost:8000/apiAdministrador/', {
            headers: {
                Authorization: "Bearer " + token,
            }
        }).then(response => {
            // os dados da API vem no formato json
            const data = response.data;

            const container = document.getElementById("listAdmin");

            // const tabela = document.createElement("div");
            // tabela.className = "table table-bordered table-hover";

            // const editar = window.location.href = "/clinica/administrador/frontend/editarAdminForm.html";

            // cria tabela base
            let tabela = `
                <table class="table table-bordered table-hover">
                    <thead class="table-primary">
                        <tr>
                            <th>Nome de usuário</th>
                            <th>Email</th>
                            <th>Nome completo</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            if(data.length > 0){
                data.forEach(admin => {
                    tabela += `
                        <tr>
                            <td>${admin.user.username}</td>
                            <td>${admin.user.email}</td>
                            <td>${admin.nome}</td>
                            <td class="d-flex justify-content-between">
                                <a href="editarAdminForm.html?username=${admin.user.username}/">
                                    <i class="bi bi-pencil-square text-blue"></i>
                                </a>

                                <button class="btn btn-link text-danger" onclick="deletarAdministrador('${admin.user.username}')">
                                    <i class="bi bi-trash3-fill"></i>
                                </button>

                                <a href="senhaForm.html?username=${admin.user.username}">
                                    <i class="bi bi-file-lock2-fill"></i>
                                    Alterar senha
                                </a>
                            </td>
                        </tr>
                    `;
                });
            } else {
                tabela += `
                    <tr>
                        <td colspan="4">Nenhum administrador cadastrado.</td>
                    </tr>
                `;
            }

            tabela += `</tbody></table>`;
            container.innerHTML = tabela;

        });
    }catch(err){
        console.error("Erro ao carregar os administrador: ", err);
    }
}


if (formEditar){
    formEditar.addEventListener('submit', function(e){
        //permite que o formulário não recarregue após o seu envio.
        e.preventDefault();

        // pega o parâmetro que veio da url ao clicar no botão de editar usuário
        const parametro = new URLSearchParams(window.location.search);
        // o replace tira simbolos que podem vim junto com o parâmetro
        const username = parametro.get("username")?.replace(/\/+$/, "");


        const formData = {
            user:{
                email: document.getElementById('email').value,
            },
            nome: document.getElementById('nome').value
        };

        //o axios é o que possibilita eviar a requisição do javaScript puro para
        //a API django rest framework
        axios.put(`http://localhost:8000/apiAdministrador/administradorDetail/${username}/`, formData, {
            //envia os dados no formato json
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
        })
        .then(response => {
            alert("Nome atualizado com sucesso");
            console.log(response.data)
        })
        .catch(async function(err){
            if (err.response?.status === 401){
                //tenta renovar o tokén através da função refresh tokén criada aqui no JavaScript
                await refreshAccessToken();
                // tenta fazer o cadastro novamente
                return formEditar.dispatchEvent(new Event('submit'));
            }
            console.error(err.response?.data);
            alert("Erro ao editar dado: " + (err.response?.data?.detail || err.message));
        });
    });
}

function deletarAdministrador(username){
    // pega o parâmetro que veio da url ao clicar no botão de editar usuário
        // const parametro = new URLSearchParams(window.location.search);
        // // o replace tira simbolos que podem vim junto com o parâmetro
        // const username = parametro.get("username")?.replace(/\/+$/, "");

    axios.delete(`http://localhost:8000/apiAdministrador/administradorDetail/${username}/`, {
        headers: {
            Authorization: "Bearer " + token
        }
    }).then(responnse => {
        alert("Administardor deletado com sucesso");
    }).catch(err => {
        alert("Erro ao deletar administrador: " + (err));
    });
}

if (formAlterarSenha){
    formAlterarSenha.addEventListener('submit', function(e){
        //permite que o formulário não recarregue após o seu envio.
        e.preventDefault();

        // pega o parâmetro que veio da url ao clicar no botão de editar usuário
        const parametro = new URLSearchParams(window.location.search);
        // o replace tira simbolos que podem vim junto com o parâmetro
        const username = parametro.get("username")?.replace(/\/+$/, "");


        const formData = {
            username,
            senha: document.getElementById('password').value,
            senhaConfirme: document.getElementById('senhaConfirme').value
        };

        //o axios é o que possibilita eviar a requisição do javaScript puro para
        //a API django rest framework
        axios.put(`http://localhost:8000/apiAdministrador/alterarSenha/`, formData, {
            //envia os dados no formato json
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
        })
        .then(response => {
            alert("senha atualizada com sucesso");
            console.log(response.data)
        })
        .catch(async function(err){
            if (err.response?.status === 401){
                //tenta renovar o tokén através da função refresh tokén criada aqui no JavaScript
                await refreshAccessToken();
                // tenta fazer o cadastro novamente
                return formEditar.dispatchEvent(new Event('submit'));
            }
            console.error(err.response?.data);
            alert("Erro ao editar dado: " + (err.response?.data?.detail || err.message));
        });
    });
}
