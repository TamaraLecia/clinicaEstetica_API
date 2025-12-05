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
            // window.location.href = "/clinica/administrador/frontend/indexADM.html";
} catch(err){
        alert("Erro ao realizar login: " +(err.responnse?.data?.detaill || err.message));
}