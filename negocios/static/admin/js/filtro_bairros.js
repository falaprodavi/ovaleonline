document.addEventListener("DOMContentLoaded", function () {
  let cidadeSelect = document.querySelector("#id_cidade");
  let bairroSelect = document.querySelector("#id_bairro");

  if (cidadeSelect && bairroSelect) {
    cidadeSelect.addEventListener("change", function () {
      let cidadeId = this.value;
      bairroSelect.innerHTML = "<option value=''>Carregando...</option>";

      if (cidadeId) {
        fetch(`/carregar_bairros/?cidade_id=${cidadeId}`)
          .then((response) => response.json())
          .then((data) => {
            bairroSelect.innerHTML =
              "<option value=''>Selecione um bairro</option>";
            data.forEach((bairro) => {
              let option = document.createElement("option");
              option.value = bairro.id;
              option.textContent = bairro.nome;
              bairroSelect.appendChild(option);
            });
          });
      } else {
        bairroSelect.innerHTML =
          "<option value=''>Selecione uma cidade primeiro</option>";
      }
    });
  }
});
