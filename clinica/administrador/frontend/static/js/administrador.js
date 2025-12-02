// import axios from 'axios';

const form = document.getElementById('formulario');

form.addEventListener('submit', function(e){
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