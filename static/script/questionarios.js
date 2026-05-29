const perguntas = [
    document.querySelector('.pergunta-1'),
    document.querySelector('.pergunta-2')
];

let perguntaAtual = 0;

// garante que só a primeira aparece
perguntas.forEach((p, index) => {
    if(index !== 0){
        p.classList.remove('ativa');
    }
});

function proxima(){

    const resposta =
        perguntas[perguntaAtual]
        .querySelector('input[type="radio"]:checked');

    if(!resposta){
        alert("Selecione uma opção");
        return;
    }

    perguntas[perguntaAtual].classList.remove('ativa');

    perguntaAtual++;

    if(perguntaAtual < perguntas.length){
        perguntas[perguntaAtual].classList.add('ativa');
    } else {
        alert("Quiz finalizado!");
    }
}

function voltar(){

    if(perguntaAtual === 0) return;

    perguntas[perguntaAtual].classList.remove('ativa');

    perguntaAtual--;

    perguntas[perguntaAtual].classList.add('ativa');
}

