// Endereço base para listar e criar planos (GET e POST)
const API_PLANOS = "http://127.0.0.1:8000/plano/api/planos/";
// consumindo a API de serviço
const API_TIPOSERVICO = "http://127.0.0.1:8000/servico/";
// Endereço para atualizar plano específico (PUT/PATCH)
const API_UPDATE_PLANO = "http://127.0.0.1:8000/plano/update/";

// Endereço para deletar plano específico (DELETE)
const API_DELETE_PLANO = "http://127.0.0.1:8000/plano/delete/";

// Esse token é obtido após o login
const token = sessionStorage.getItem("acessToken");

// LISTAR PLANOS (GET) – CARREGAR TUDO DO DJANGO

// Envia requisição GET para o Django buscar todos os planos cadastrados
axios.get(API_PLANOS, {
    headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}` // Envia o token no cabeçalho
    }
})
.then(response => {
    // Recebe os planos retornados pela API
    const planos = response.data;

    // Elemento HTML onde os cards/listagem serão inseridos
    const container = document.getElementById("conteudoPlanos");

    // Caso a página não tenha esse container, evita erro
    if (!container) return;

    // Percorre cada plano e renderiza na tela
    planos.forEach(plano => {
        container.innerHTML += `
            <div class="card p-3 mb-3">
                <h3>${plano.nome}</h3>
                <p><strong>Preço:</strong> R$ ${plano.valor}</p>
                <p><strong>Descrição:</strong> ${plano.descricao}</p>

                <!-- Botões para editar e excluir -->
                <a href="/plano/editar/${plano.id}" class="btn btn-primary">Editar</a>
                <button onclick="deletarPlano(${plano.id})" class="btn btn-danger">Excluir</button>
            </div>
        `;
    });
})
.catch(err => {
    console.error("Erro ao carregar planos:", err);
});

// CRIAR PLANO (POST)


// Formulário de criação de plano no HTML
const formAddPlano = document.getElementById("planoFormulario");
if(formAddPlano){
    carregarServico();
}

formAddPlano.addEventListener("submit", async (e) => {

    e.preventDefault();  // Evita que a página recarregue ao enviar o form

    // Colhe os dados digitados no formulário
    const formData = new FormData(e.target);

    try {
        // Envia os dados para o Django
        const response = await axios.post(API_PLANOS, formData, {
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`
            }
        });

        alert("Plano criado com sucesso!");
        console.log(response.data);

    } catch (err) {
        console.error("Erro ao criar plano:", err.response?.data || err);
        alert("Erro ao criar plano");
    }
});


const formAdicionarPlano =document.getElementById("planoFormulario");

    // carrega as categorias registradas no banco de dados
async function carregarServico(){
    try{
        const response = await axios.get(API_TIPOSERVICO, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });
        const servicos = response.data;
        const selectTipo = document.getElementById("servico_nome");

        servicos.forEach(servico => {
            const option = document.createElement("option");
            option.value = servico.servico;
            option.textContent = servico.servico;
            selectTipo.appendChild(option);
        });
    } catch (err){
        console.error("Erro ao carregar servico: ", err);
    }
    }


// ATUALIZAR PLANO (PUT/PATCH)

// Função chamada ao clicar no botão "Salvar Alterações"
async function atualizarPlano(id) {

    // Pega o formulário da página de edição
    const form = document.getElementById("formEditarPlano");

    // Pega os dados preenchidos pelo usuário
    const formData = new FormData(form);

    try {
        // Envia PUT para atualizar os dados do plano
        const response = await axios.put(`${API_UPDATE_PLANO}${id}/`, formData, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        alert("Plano atualizado com sucesso!");
        console.log(response.data);

    } catch (err) {
        console.error("Erro ao atualizar plano:", err.response?.data || err);
        alert("Erro ao atualizar plano");
    }
}

// DELETAR PLANO (DELETE)

async function deletarPlano(id) {

    // Confirmação para evitar exclusão acidental
    if (!confirm("Tem certeza que deseja excluir este plano?")) return;

    try {
        // Envia DELETE para remover o plano
        await axios.delete(`${API_DELETE_PLANO}${id}/`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        alert("Plano deletado com sucesso!");

        // Recarrega a página para mostrar a lista atualizada
        location.reload();

    } catch (err) {
        console.error("Erro ao deletar plano:", err.response?.data || err);
        alert("Erro ao deletar plano");
    }
}
