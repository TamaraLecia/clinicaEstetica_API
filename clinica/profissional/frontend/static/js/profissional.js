const formCadastro = document.getElementById('profissionalForm')

// pega o tokén que é criado quando o usuário realiza o login
const token = sessionStorage.getItem("acessToken");

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
            nome: document.getElementById('nome').value,
            endereco: document.getElementById('endereco').value,
            especializacao: document.getElementById('especializacao').value,
            numTelefone: document.getElementById('telefone').value,
            salario: document.getElementById('salario').value
        };

        //o axios é o que possibilita eviar a requisição do javaScript puro para
        //a API django rest framework
        axios.post('http://localhost:8000/apiProfissional/profissionalApi/', formData, {
            //envia os dados no formato json
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token
            },
            withCredentials: true
        })
        .then(function(res){
            alert("Cadastro de profissional realizado com sucesso!");
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
            alert("Erro ao cadastrar profissional: " + JSON.stringify(err.response?.data));
            // alert("Erro ao cadastrar: " + (err.response?.data?.detail || err.message));
        });
    });
}

// chama a função mostrarprofissionalistrador
document.addEventListener("DOMContentLoaded", () => {
    mostrarProfissional();
});

function mostrarProfissional(){ 
    try{

        axios.get('http://localhost:8000/apiProfissional/profissionalApi/', {
            headers: {
                Authorization: "Bearer " + token,
            }
        }).then(response => {
            // os dados da API vem no formato json
            const data = response.data;

            const container = document.getElementById("listProfissional");

            // const tabela = document.createElement("div");
            // tabela.className = "table table-bordered table-hover";

            // const editar = window.location.href = "/clinica/profissionalistrador/frontend/editarprofissionalForm.html";

            // cria tabela base
            let tabela = `
                <table class="table table-bordered table-hover">
                    <thead class="table-primary">
                        <tr>
                            <th>Nome de usuário</th>
                            <th>Especialização</th>
                            <th>Endereço</th>
                            <th>Telefone</th>
                            <th>Email</th>
                            <th>Nome de completo</th>
                            <th>Ações</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            if(data.length > 0){
                data.forEach(profissional => {
                    tabela += `
                        <tr>
                            <td>${profissional.user.username}</td>
                            <td>${profissional.especializacao}</td>
                            <td>${profissional.endereco}</td>
                            <td>${profissional.numTelefone}</td>
                            <td>${profissional.user.email}</td>
                            <td>${profissional.nome}</td>
                        </tr>
                    `;
                });
            } else {
                tabela += `
                    <tr>
                        <td colspan="4">Nenhum profissional cadastrado.</td>
                    </tr>
                `;
            }

            tabela += `</tbody></table>`;
            container.innerHTML = tabela;

        });
    }catch(err){
        console.error("Erro ao carregar os profissional: ", err);
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
