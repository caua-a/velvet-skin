// Função auxiliar para formatar moeda no padrão brasileiro (R$ 129,90)


// Função auxiliar para formatar moeda no padrão brasileiro (R$ 129,90)
// const formatarMoeda = (valor) => {
//     return valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
// };

// Funções de Controle Visual do Carrinho
function abrirCarrinho() {
    const overlay = document.querySelector(".velvet-cart-overlay");
    if (overlay) {
        overlay.classList.add("active");
        mostrarCarrinho(); // Atualiza os dados sempre que abrir
    }
}

function fecharCarrinho() {
    const overlay = document.querySelector(".velvet-cart-overlay");
    if (overlay) overlay.classList.remove("active");
}

// Renderizar itens e atualizar totais
async function mostrarCarrinho() {
    // Note que alterei para buscar a div do corpo do carrinho dinâmico
    const carrinhoConteudo = document.querySelector(".cart-body");
    const campoTotal = document.getElementById("valor-total");

    if (!carrinhoConteudo || !campoTotal) return;

    try {
        const resposta = await fetch("/api/get/carrinho");

        if (!resposta.ok) throw new Error("Erro na resposta do servidor");

        const dados = await resposta.json();
        console.log("Dados recebidos do banco:", dados);

        if (!dados || dados.length === 0) {
            carrinhoConteudo.innerHTML = `
                <div style="text-align: center; color: #707070; margin-top: 40px; font-family: sans-serif;">
                    <p>Sua sacola está vazia =(</p>
                </div>
            `;
            campoTotal.textContent = "R$ 0,00";
            return;
        }

        let total = 0;
        let htmlAcumulado = ""; 

        // Função auxiliar para formatar moeda localmente se não houver a formatarMoeda global
        const formatarMoeda = (valor) => valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });

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
            body: JSON.stringify({ "id_produto": id_produto, "quantidade": quantidade })
        });

        if (!resposta.ok) {
            alert("Erro ao inserir item!");
            return;
        }

        abrirCarrinho(); // Abre o carrinho automaticamente ao adicionar um item!
    } catch (erro) {
        console.error("Erro na requisição:", erro);
    }
}

async function removerItemCarrinho(id_carrinho, id_produto) {
    try {
        const resposta = await fetch("/api/delete/item_carrinho", {
            method: "DELETE", 
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ "id_carrinho": id_carrinho, "id_produto": id_produto })
        });

        if (!resposta.ok) {
            alert("Erro ao excluir item!");
            return;
        }

        await mostrarCarrinho(); 
    } catch (erro) {
        console.error("Erro na requisição:", erro);
    }
}

async function alterarQuantidade(id_produto, novaQuantidade) {
    if (novaQuantidade < 1) return; 
    
    try {
        const resposta = await fetch("/api/post/item_carrinho", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ "id_produto": id_produto, "quantidade": novaQuantidade })
        });

        if (!resposta.ok) return;
        await mostrarCarrinho();
    } catch (erro) {
        console.error("Erro ao alterar quantidade:", erro);
    }
}

// Inicialização dos eventos ao carregar a página
document.addEventListener("DOMContentLoaded", () => {
    // Ouvinte para o botão de fechar (X)
    const btnFechar = document.querySelector(".close-cart-btn");
    if (btnFechar) {
        btnFechar.addEventListener("click", fecharCarrinho);
    }

    // Fechar ao clicar fora da área branca (na overlay escura)
    const overlay = document.querySelector(".velvet-cart-overlay");
    if (overlay) {
        overlay.addEventListener("click", (e) => {
            if (e.target === overlay) {
                fecharCarrinho();
            }
        });
    }

    // Carrega o carrinho inicialmente caso ele comece aberto por algum motivo
    mostrarCarrinho();
});



