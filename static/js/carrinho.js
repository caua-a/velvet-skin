// Função auxiliar para formatar moeda no padrão brasileiro (R$ 129,90)


// Função auxiliar para formatar moeda no padrão brasileiro (R$ 129,90)
const formatarMoeda = (valor) => {
    return valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
};

async function mostrarCarrinho() {
    const carrinhoConteudo = document.getElementById("carrinho-itens");
    const campoTotal = document.getElementById("valor-total");

    // Elementos de salvaguarda caso não existam na página atual
    if (!carrinhoConteudo || !campoTotal) return;

    try {
        const resposta = await fetch("/api/get/carrinho");

        if (!resposta.ok) {
            throw new Error("Erro na resposta do servidor");
        }

        const dados = await resposta.json();
        console.log("Dados recebidos do banco:", dados);

        // Se não houver itens, mostra a mensagem de vazio estilizada
        if (!dados || dados.length === 0) {
            carrinhoConteudo.innerHTML = `
                <div style="text-align: center; color: #707070; margin-top: 40px; font-family: sans-serif;">
                    <p>Sua sacola está vazia =(</p>
                </div>
            `;
            campoTotal.textContent = formatarMoeda(0);
            return;
        }

        let total = 0;
        let htmlAcumulado = ""; 

        for (let dado of dados) {
            total += dado.preco * dado.quantidade;
            
            htmlAcumulado += `
                <div class="cart-item">
                    <img src="../static/${dado.imagem}" alt="${dado.produto}" class="item-img">
                    <div class="item-details">
                        <h3 class="item-title">${dado.produto}</h3>
                        <span class="item-price">${formatarMoeda(dado.preco)}</span>
                        <div class="quantity-selector">
                            <button class="qty-btn" onclick="alterarQuantidade(${dado.id_produto}, ${dado.quantidade - 1})">-</button>
                            <input type="number" value="${dado.quantidade}" min="1" class="qty-input" readonly>
                            <button class="qty-btn" onclick="alterarQuantidade(${dado.id_produto}, ${dado.quantidade + 1})">+</button>
                        </div>
                    </div>
                    <button 
                        class="remove-item-btn" 
                        onclick="removerItemCarrinho(${dado.id_carrinho}, ${dado.id_produto})"
                    >
                        &times;
                    </button>
                </div>
            `;
        }

        carrinhoConteudo.innerHTML = htmlAcumulado;
        campoTotal.textContent = formatarMoeda(total);

    } catch (erro) {
        console.error("Erro ao carregar o carrinho:", erro);
        carrinhoConteudo.innerHTML = `<p style="color: red; text-align: center;">Erro ao carregar produtos.</p>`;
    }
}

async function inserirItemCarrinho(id_produto, quantidade = 1) {
    try {
        const resposta = await fetch("/api/post/item_carrinho", {
            method: "POST", 
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                "id_produto": id_produto,
                "quantidade": quantidade
            })
        });

        if (!resposta.ok) {
            alert("Erro ao inserir item!");
            return;
        }

        await mostrarCarrinho();
    } catch (erro) {
        console.error("Erro na requisição:", erro);
    }
}

async function removerItemCarrinho(id_carrinho, id_produto) {
    try {
        const resposta = await fetch("/api/delete/item_carrinho", {
            method: "DELETE", 
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                "id_carrinho": id_carrinho,
                "id_produto": id_produto
            })
        });

        if (!resposta.ok) {
            alert("Erro ao excluir item!");
            return;
        }

        // CORREÇÃO: Adicionado para fazer o item sumir da tela na hora
        await mostrarCarrinho(); 
    } catch (erro) {
        console.error("Erro na requisição:", erro);
    }
}

// CORREÇÃO: Função adicionada de volta para os botões + e - funcionarem
async function alterarQuantidade(id_produto, novaQuantidade) {
    if (novaQuantidade < 1) return; // Evita que a quantidade seja menor que 1
    
    try {
        const resposta = await fetch("/api/post/item_carrinho", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                "id_produto": id_produto,
                "quantidade": novaQuantidade
            })
        });

        if (!resposta.ok) return;
        await mostrarCarrinho();
    } catch (erro) {
        console.error("Erro ao alterar quantidade:", erro);
    }
}

// Inicializa chamando a função quando o documento estiver pronto
document.addEventListener("DOMContentLoaded", () => {
    mostrarCarrinho();
});



