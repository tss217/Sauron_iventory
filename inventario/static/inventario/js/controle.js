const hhidInput = document.querySelector("#controle-hhid");
const nomeInput = document.querySelector("#controle-equipamento");
const feedback = document.querySelector("#controle-feedback");

async function buscarEquipamento() {
  const hhid = hhidInput.value.trim();

  if (!hhid) {
    nomeInput.value = "";
    feedback.hidden = true;
    return;
  }

  const url = hhidInput.dataset.urlBusca.replace(
    "HHID",
    encodeURIComponent(hhid)
  );

  try {
    const resposta = await fetch(url, {
      headers: { Accept: "application/json" },
    });
    const dados = await resposta.json();

    if (!resposta.ok) {
      nomeInput.value = "";
      feedback.hidden = false;
      return;
    }

    hhidInput.value = dados.hhid;
    nomeInput.value = dados.nome;
    feedback.hidden = true;
  } catch (erro) {
    nomeInput.value = "";
    feedback.hidden = false;
  }
}

if (hhidInput) {
  hhidInput.addEventListener("blur", buscarEquipamento);

  hhidInput.addEventListener("input", () => {
    feedback.hidden = true;
  });
}
