// consumindo a API de serviço
const API_URLl = "http://127.0.0.1:8000/servico/"; //LINK DA API

// Faça a requisiçao da API GET usando o Axios
axios.get(API_URLl).then(response =>{
    // os dados da API vem no formato response.data
    const data = response.data;

    // Seleciona o container HTML que vai mostrar os serviços
    const container = document.getElementById("conteudo");

    // Mostra o carrousel se tiver mais de três serviços
    if(data.length > 3){
        const carousel = document.createElement("div");
        carousel.className = "owl-carousel pricing-carrousel";

        // Percorre cada serviço retornado pela API
        data.forEach(servico => {
            // Monta o HTML para cada serviço do carrousel
            carousel.innerHTML += `
                <div class="pricing-item">
                    <div class="rounded princig-content">
                        <div class="d-flex flex-wrap align-items-center justify-content-between bg-light rounded-top border-3 border-bottom border-primary p-4">
                            <h1 class="display-4 mb-0">
                                <small class="align-top text-muted" style="font-size: 22px;">R$</small>${servico.preco}
                            </h1>
                            <img src="${servico.arquivo}" class="img-thumbnail w-80 h-40" alt="Imagem">
                            <div>
                                <h5 class="text-primary text-uppercase mb-1">${servico.tipo}</h5>
                                <h5 class="text-primary text-uppercase mb-1">${servico.profissional}</h5>
                                <h5 class="text-primary text-uppercase mb-1">${servico.descricao}</h5>
                            </div>
                        </div>
                        <div class="p-4">
                            <!-- Lista os sub-serviços -->
                            ${servico.servico.map(s => `<p><i class="fa fa-check text-primary me-2"></i>${s.servico}</p>`).join("")}
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
        $('.owl-carousel').owlCarousel({ loop:true, margin:10, nav:true, items:3 });

    } else if (data.length >= 1){
        // Se houver até 3 serviços, exibe em cards
        const row = document.createElement("div");
        row.className = "row";

        // Pecorre cada plano retornado pela API
        data.forEach(plano => {
            row.innerHTML += `
                <div class="col-md-4 mb-4">
                    <div class="pricing-item h-100">
                        <div class="rounded pricing-content h-100 d-flex flex-column justify-content-between">
                            <div class="bg-light rounded-top border-3 border-bottom border-primary p-4">
                                <h1 class="display-4 mb-0">
                                    <small class="text-muted" style="font-size: 22px;">R$</small>${plano.preco}
                                </h1>
                                <h5 class="text-primary text-uppercase mt-2">${plano.tipo}</h5>
                            </div>
                             <div class="p-4">
                                <!-- Lista os sub-serviços -->
                                ${plano.servico.map(s => `<p><i class="fa fa-check text-primary me-2"></i>${s.servico}</p>`).join("")}
                                <!-- Botão de solicitação -->
                                <a href="#" class="btn btn-primary rounded-pill my-2 px-4">Solicitar</a>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });

        // coloca os cards no container
        container.appendChild(row);
    }
    
})
// mostra os erros no terminal
    .catch(err => console.error("Erro ao carregar os serviço: ", err));