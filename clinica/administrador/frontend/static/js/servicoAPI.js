// consumindo a API de serviço
const API_URLl = "http://127.0.0.1:8000/servico/"; //LINK DA API
// consumindo a API de categoria do serviço
const API_TIPOCATEGORIA = "http://127.0.0.1:8000/servico/categoriaApi/";
// consumindo a API de profissional
const API_PROFISSIONAIS = "http://127.0.0.1:8000/profissional/profissionalApi/";

// Utilizando o token obtido no login
const token = sessionStorage.getItem("acessToken")

// Faça a requisiçao da API GET usando o Axios
axios.get(API_URLl,{
    // utilizando o token para realizar a requisiçao do get
    headers: {
        Authorization: `Bearer ${token}`  //autenticação JWT
    }
}).then(response =>{
    // os dados da API vem no formato response.data
    let data = response.data;

    // Se vier apenas um objeto é transformado em um array
    if(!Array.isArray(data)){
        data = [data];
    }

    // Seleciona o container HTML que vai mostrar os serviços
    const container = document.getElementById("conteudo");

    // Mostra o carrousel se tiver mais de três serviços
    if(data.length > 3){
        const carousel = document.createElement("div");
        carousel.className = "owl-carousel pricing-carrousel";

        // Percorre cada serviço retornado pela API
        data.forEach(servico => {
            // Montar a URL completa da imagem que vem da API
            const BASE_URL = "http://127.0.0.1:8000";
            const imagemURL = `${BASE_URL}${servico.arquivo}`; //concatena a imagem com a BASE_URL do Django
            let listaServico = "";

            if(Array.isArray(servico.servico)){
                //se for uma lista, utiliza o map para percorrer
                listaServico = servico.servico.map(s => `<p><i class="fa fa-check text-primary me-2"></i>${s.servico}</p>`).join("");
            } else if(servico.servico){
                // se for um valor mostra a string ou o objeto ǘnico
                listaServico = `<p><i class="fa fa-check text-primary me-2"></i>${servico.servico}</p>`;
            }

            // Monta o HTML para cada serviço do carrousel
            carousel.innerHTML += `
                <div class="pricing-item">
                    <div class="rounded pricing-content">
                        <div class="d-flex flex-wrap align-items-center justify-content-between bg-light rounded-top border-3 border-bottom border-primary p-4">
                            <h1 class="display-4 mb-0">
                                <small class="align-top text-muted" style="font-size: 22px;">R$</small>${servico.preco}
                            </h1>
                            <img src="${imagemURL}" class="img-thumbnail" style="width:80%; height:40%;" alt="Imagem">
                            <div>
                                <h5 class="text-primary text-uppercase mb-1">${servico.tipo}</h5>
                                <h5 class="text-primary text-uppercase mb-1">${servico.profissional}</h5>
                                <h5 class="text-primary text-uppercase mb-1">${servico.descricao}</h5>
                            </div>
                        </div>
                        <div class="p-4">
                            <!-- Lista os sub-serviços -->
                            ${listaServico}
                            <!-- Botões de ação -->
                            <a href="/administrador/alterarServico/${servico.id}" class="btn btn-primary rounded-pill my-2 px-4">Alterar Serviço</a>
                            <a href="/administrador/alterarCategoria/${servico.id}" class="btn btn-warning"><i class="bi bi-pencil-fill"></i> Alterar Categoria</a>
                            <a href="/administrador/deletarCategoria/${servico.id}" class="btn btn-danger"><i class="bi bi-trash"></i> Apagar Categoria</a>
                            <a href="/administrador/deletarServico/${servico.id}" class="btn btn-primary rounded-pill my-2 px-4">Apagar Serviço</a>
                        </div>
                    </div>
                </div>
            
            `;
        });
        // Adiciona o carroussel ao container
        container.appendChild(carousel);

        // Inicia o Owl Carousel
        $('.owl-carousel').owlCarousel({ loop:true, margin:10, nav:true, items: 3, autoplay: true, autoplayTimeout: 1000, autoplayHoverPause: true, navText: [
        "<i class='bi bi-chevron-left'></i>", 
        "<i class='bi bi-chevron-right'></i>"
    ]});

    } else if (data.length >= 1){
        // Se houver até 3 serviços, exibe em cards
        const row = document.createElement("div");
        row.className = "row";

        data.forEach(servico => {
            const BASE_URL = "http://127.0.0.1:8000";
            const imagemURL = `${BASE_URL}${servico.arquivo}`;

            row.innerHTML +=`
                <div class="col-md-4 mb-4">
                    <div class="pricing-item h-100">
                        <div class="rounded pricing-content h-100 d-flex flex-column justify-content-between">
                            <div class="bg-light rounded-top border-3 border-bottom border-primary p-4">
                                <h1 class="display-4 mb-0">
                                    <small class="text-muted" style="font-size: 22px;">R$</small>${servico.preco}
                                </h1>
                                <div class="p-4">
                                    <p class="text-dark"><i class="fa fa-check text-primary me-2"></i>${servico.servico}</p>
                                    <img src="${imagemURL}" class="img-thumbnail" style="width:90%; height:45%;" alt="Imagem">
                                    <h5 class="text-primary text-uppercase mb-1 mt-3 fs-6">${servico.tipo}</h5>
                                    <h5 class="text-primary text-uppercase mb-1 fs-6">${servico.profissional}</h5>
                                </div>
                            </div>
                            <div class="p-4">
                                <a href="/administrador/alterarServico/${servico.id}" class="btn btn-primary rounded-pill my-2 px-4 fs-14">Alterar Serviço</a> 
                                <a href="/administrador/alterarCategoria/${servico.id}" class="btn btn-warning rounded-pill my-2 px-4"><i class="bi bi-pencil-fill"></i> Alterar Categoria</a>
                                <a href="/administrador/deletarCategoria/${servico.id}" class="btn btn-danger rounded-pill my-2 px-4"><i class="bi bi-trash"></i> Apagar Categoria</a>
                                <a href="/administrador/deletarServico/${servico.id}" class="btn btn-primary rounded-pill my-2 px-4">Apagar Serviço</a>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });
         container.appendChild(row);
    }    
    
})
// mostra os erros no terminal
    .catch(err => console.error("Erro ao carregar os serviço: ", err));

// Adicionando serviço usando a API
// verifica se o formulário existe na página
const formAdicionarServico =document.getElementById("formulario");
if(formAdicionarServico){
    // carrega as categorias registradas no banco de dados
    async function carregarCategorias(){
        try{
            const response = await axios.get(API_TIPOCATEGORIA, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });
            const categorias = response.data;
            const selectTipo = document.getElementById("tipo_nome");

            categorias.forEach(categoria => {
                const option = document.createElement("option");
                option.value = categoria.categoria;
                option.textContent = categoria.categoria;
                selectTipo.appendChild(option);
            });
        } catch (err){
            console.error("Erro ao carregar categorias: ", err);
        }
    }

    // carrega os profissionais cadastrados no banco de dados
    async function carregarProfissionais() {
        try{
            const response = await axios.get(API_PROFISSIONAIS, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });
            const profissionais = response.data;
            const selectProfissional = document.getElementById("profissional_nome");

            profissionais.forEach(prof => {
                const option = document.createElement("option");
                option.value = prof.nome;
                option.textContent = prof.nome;
                selectProfissional.appendChild(option);
            });
        } catch (err){
            console.error("Erro ao carregar profissionais: ", err);
        }
    }

    // Executa ao carregar a página
    window.addEventListener("DOMContentLoaded", () => {
        carregarCategorias();
        carregarProfissionais();
    })


    document.getElementById("formulario").addEventListener("submit", async (e) => {
        e.preventDefault();
        const formData = new FormData(e.target);

        try{
            const response = await axios.post(API_URLl, formData, {
                headers: {
                    Authorization: `Bearer ${token}`,
                    // "Content-Type": "multipart/form-data"
                }
            });
            alert("Servico adicionado com sucesso!");
            console.log(response.data);
        } catch (err){
            console.error("Erro ao adicionar o serviço:", err.response?.data || err);
            alert("Erro ao adicionar o serviço");
        }
    });

    // carregar o tipo de categoria somente se existir
    const selectTipoCategoria = document.getElementById("tipo_nome");
    if(selectTipoCategoria){
        carregarCategorias();
    }

    // carregar os profissionais somente se existir algum
    const selectProfissionais = document.getElementById("profissional_nome");
    if(selectProfissionais){
        carregarProfissionais();
    }
}

// ADICIONANDO A CATEGORIA DO SERVIÇO

const formAdicionarCategoria = document.getElementById("formularioCategoria");

if (formAdicionarCategoria) {
    formAdicionarCategoria.addEventListener("submit", async (e) => {
        e.preventDefault();

        // Guarda os dados passados no formulário
        const formData = new FormData(e.target);

        try{
            // Faz o post para a API de categoria
            const response = await axios.post(API_TIPOCATEGORIA, formData, {
                headers: {
                    Authorization: `Bearer ${token}`,
                }
            });

            alert("Categoria adicionada com sucesso!");
            console.log(response.data);
        } catch (err) {
            console.error("Erro ao adicionar categoria: ", err.response?.data || err);
            alert("Erro ao adicionar categoria");
        }
    });
}