CREATE DATABASE velvetskin;
USE velvetskin;

CREATE TABLE usuarios (
    usuario VARCHAR(50) PRIMARY KEY,
    senha VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    telefone VARCHAR(20),
    endereco_principal TEXT
);

CREATE TABLE produtos (
    id_produto INT AUTO_INCREMENT PRIMARY KEY,
    produto VARCHAR(100) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10, 2) NOT NULL,
    categoria VARCHAR(50),
    imagem VARCHAR(255)
);


CREATE TABLE carrinho (
    id_carrinho INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50),
    id_produto INT,
    quantidade INT,
    FOREIGN KEY (usuario) REFERENCES usuarios(usuario),
    FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
);

CREATE TABLE comentarios (
    id_comentario INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(50),
    comentario TEXT NOT NULL,
    data_postado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_produto INT,
    FOREIGN KEY (usuario) REFERENCES usuarios(usuario),
    FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
);

-- 1. INSERTS PARA A TABELA 'usuarios'
-- Nota: Em produção, as senhas devem ser guardadas como hashes (ex: usando bcrypt), mas para o exemplo usei texto simples.
INSERT INTO usuarios (usuario, senha, email, telefone, endereco_principal) VALUES
('ana_silva', 'senha123', 'ana.silva@email.com', '+351912345678', 'Rua das Flores, nº 10, 4º Esq, Lisboa'),
('carlos_mendes', 'carlos2026', 'carlos.mendes@email.com', '+351933445566', 'Avenida Central, Bloco B, Apt 202, Porto'),
('mariana_costa', 'velvet_secure!', 'mariana.costa@email.com', '+351967890123', 'Praça da República, nº 45, Coimbra');


-- 2. INSERTS PARA A TABELA 'produtos'
INSERT INTO produtos (produto, descricao, preco, categoria, imagem) VALUES
('Sérum de Ácido Hialurónico', 'Sérum hidratante intensivo que reduz linhas de expressão e melhora a elasticidade da pele.', 24.99, 'Séruns', 'imagens/serum_hialuronico.jpg'),
('Gel de Limpeza Purificante', 'Gel de limpeza facial com ácido salicílico, ideal para peles oleosas e com tendência acneica.', 14.50, 'Limpeza', 'imagens/gel_limpeza.jpg'),
('Creme Hidratante Velvet Night', 'Creme de noite nutritivo com ceramidas e niacinamida para reparação profunda da barreira cutânea.', 29.90, 'Hidratantes', 'imagens/creme_noite.jpg'),
('Protetor Solar FPS 50+', 'Fluido protetor solar invisível com toque seco e alta proteção UVA/UVB.', 19.95, 'Proteção Solar', 'imagens/protetor_solar.jpg'),
('Tónico Renovador AHA', 'Tónico esfoliante químico com ácido glicólico para uma pele mais radiante e textura uniforme.', 18.00, 'Tónicos', 'imagens/tonico_aha.jpg');


-- 3. INSERTS PARA A TABELA 'carrinho'
-- Simula utilizadores que adicionaram produtos ao carrinho de compras
INSERT INTO carrinho (usuario, id_produto) VALUES
('ana_silva', 1, 5), -- Ana adicionou o Sérum
('ana_silva', 4, 2), -- Ana também adicionou o Protetor Solar
('carlos_mendes', 2, 3), -- Carlos adicionou o Gel de Limpeza
('mariana_costa', 3, 3); -- Mariana adicionou o Creme de Noite


-- 4. INSERTS PARA A TABELA 'comentarios'
-- Simula avaliações e comentários deixados pelos clientes nos produtos
INSERT INTO comentarios (usuario, comentario, id_produto) VALUES
('ana_silva', 'Adorei este sérum! A minha pele ficou super hidratada e com um brilho natural logo na primeira semana.', 1),
('carlos_mendes', 'Muito bom para controlar a oleosidade, limpa profundamente sem ressecar a pele. Recomendo!', 2),
('mariana_costa', 'O creme é bastante nutritivo, mas achei um pouco pesado para a minha pele mista. Ideal para o inverno.', 3),
('ana_silva', 'Não deixa a pele esbranquiçada e o toque seco é real. O melhor protetor que já usei.', 4);