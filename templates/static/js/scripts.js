// Atualiza os bairros quando a cidade é alterada
document.addEventListener("DOMContentLoaded", function() {
    const cidadeSelect = document.getElementById("cidade");
    const bairroSelect = document.getElementById("bairro");

    if (cidadeSelect) {
        cidadeSelect.addEventListener("change", function() {
            let cidadeId = this.value;

            fetch(`/carregar_bairros/?cidade_id=${cidadeId}`)
            .then(response => response.json())
            .then(data => {
                bairroSelect.innerHTML = '<option value="">Selecione o Bairro</option>';
                data.forEach(bairro => {
                    bairroSelect.innerHTML += `<option value="${bairro.id}">${bairro.nome}</option>`;
                });
            });
        });
    }

    
});


