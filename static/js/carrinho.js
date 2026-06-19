// Função auxiliar para formatar moeda no padrão brasileiro (R$ 129,90)


// Função auxiliar para formatar moeda no padrão brasileiro (R$ 129,90)
// const formatarMoeda = (valor) => {
//     return valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
// };

// Funções de Controle Visual do Carrinho
// Renderizar itens e atualizar totais
// Função para abrir o carrinho lateral (Adiciona a classe active na overlay)
function abrirCarrinho() {
    const overlay = document.querySelector(".velvet-cart-overlay");
    if (overlay) {
        overlay.classList.add("active"); // Certifique-se de que seu CSS usa .active para mostrar o carrinho
        // Opcional: se o CSS usar display, mude para: overlay.style.display = "flex";
    }
    mostrarCarrinho(); // Atualiza os dados sempre que abrir
}

// Função para fechar o carrinho lateral
function fecharCarrinho() {
    const overlay = document.querySelector(".velvet-cart-overlay");
    if (overlay) {
        overlay.classList.remove("active");
        // Opcional: se o CSS usar display, mude para: overlay.style.display = "none";
    }
}

// Renderizar itens e atualizar totais
async function mostrarCarrinho() {
    const carrinhoConteudo = document.querySelector(".cart-body");
    const campoTotal = document.getElementById("valor-total");
    const campoSubtotal = document.getElementById("valor-subtotal");

    if (!carrinhoConteudo) return;

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
            if (campoTotal) campoTotal.textContent = "R$ 0,00";
            if (campoSubtotal) campoSubtotal.textContent = "R$ 0,00";
            return;
        }

        let total = 0;
        let htmlAcumulado = ""; 

        const formatarMoeda = (valor) => valor.toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });

        for (let dado of dados) {
            total += dado.preco * dado.quantidade;
            
            // Tratamento caso a imagem simulada não comece com /static/
            let caminhoImagem = dado.imagem.startsWith('/static/') ? dado.imagem : `/static/${dado.imagem}`;

            htmlAcumulado += `
                <div class="cart-item" style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 15px; padding: 10px; border: 1px solid #eee;">
                    <img src="${caminhoImagem}" alt="${dado.produto}" class="item-img" style="width: 60px; height: 60px; object-fit: cover;" onerror="this.src='https://placehold.co/60'">
                    <div class="item-details" style="flex: 1; margin-left: 10px;">
                        <h3 class="item-title" style="font-size: 14px; margin: 0;">${dado.produto}</h3>
                        <span class="item-price" style="color: #2F3E1B; font-weight: bold;">${formatarMoeda(dado.preco)}</span>
                        <div class="quantity-selector" style="display: flex; align-items: center; margin-top: 5px;">
                            <button class="qty-btn" onclick="alterarQuantidade(${dado.id_produto}, ${dado.quantidade - 1})">-</button>
                            <input type="number" value="${dado.quantidade}" min="1" class="qty-input" style="width: 40px; text-align: center;" readonly>
                            <button class="qty-btn" onclick="alterarQuantidade(${dado.id_produto}, ${dado.quantidade + 1})">+</button>
                        </div>
                    </div>
                    <button 
                        class="remove-item-btn" 
                        style="background: none; border: none; cursor: pointer; display: flex; align-items: center; justify-content: center; margin-bottom: 35px;"
                        onclick="removerItemCarrinho(${dado.id_produto})"
                    >
                        <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#A83232">
                            <path d="M280-120q-33 0-56.5-23.5T200-200v-520h-40v-80h200v-40h240v40h200v80h-40v520q0 33-23.5 56.5T680-120H280Zm400-600H280v520h400v-520ZM360-280h80v-360h-80v360Zm160 0h80v-360h-80v360ZM280-720v520-520Z"/>
                        </svg>
                    </button>
                </div>
            `;
        }

        carrinhoConteudo.innerHTML = htmlAcumulado;
        
        if (campoTotal) campoTotal.textContent = formatarMoeda(total);
        if (campoSubtotal) campoSubtotal.textContent = formatarMoeda(total);

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

        abrirCarrinho(); 
        // CORREÇÃO AQUI: Espera a resposta do servidor para recarregar os dados na tela
        await mostrarCarrinho(); 
    } catch (erro) {
        console.error("Erro na requisição:", erro);
    }
}

async function removerItemCarrinho(id_produto) {
    try {
        const resposta = await fetch(`/api/delete/item_carrinho/${id_produto}`, {
            method: "DELETE"
        });

        if (resposta.ok) {
            // Recarrega os dados do carrinho na tela imediatamente após deletar
            await mostrarCarrinho();
        } else {
            alert("Erro ao remover o produto do carrinho.");
        }
    } catch (erro) {
        console.error("Erro ao deletar item:", erro);
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
    const btnFechar = document.querySelector(".close-cart-btn");
    if (btnFechar) {
        btnFechar.addEventListener("click", fecharCarrinho);
    }

    const overlay = document.querySelector(".velvet-cart-overlay");
    if (overlay) {
        overlay.addEventListener("click", (e) => {
            if (e.target === overlay) {
                fecharCarrinho();
            }
        });
    }

    mostrarCarrinho();
});



