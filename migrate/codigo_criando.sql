-- 1. CRIAÇÃO DO BANCO DE DADOS E SELEÇÃO
CREATE DATABASE IF NOT EXISTS velvetskin;
USE velvetskin;

-- 2. CRIAÇÃO DAS TABELAS
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


-- 3. INSERÇÃO DOS DADOS DE EXEMPLO (COM URLS DE IMAGENS REAIS)

-- Inserindo Usuário
INSERT INTO usuarios (usuario, senha, email, telefone, endereco_principal) 
VALUES (
    'mariasilva', 
    'senha_criptografada_aqui', 
    'maria.silva@email.com', 
    '(11) 99999-8888', 
    'Rua das Flores, 123 - São Paulo, SP'
);

-- Inserindo Produtos (Categorias: diurno ou noturno)
INSERT INTO produtos (produto, descricao, preco, categoria, imagem) 
VALUES 
(
    'Protetor Solar Facial', 
    'Proteção solar diária com controle de oleosidade e rápida absorção.', 
    79.90, 
    'diurno', 
    'static/img/protetor solar.png'
),
(
    'Sérum de Retinol Noturno', 
    'Tratamento noturno antidade que renova a textura da pele enquanto você dorme.', 
    129.90, 
    'noturno', 
    'static/img/serum retinol noturno.png'
),
(
    'Gel de Limpeza Facial', 
    'Limpeza profunda diária que remove a oleosidade sem ressecar.', 
    45.00, 
    'diurno', 
    'static/img/gel de limpeza facial.png'
),
(
    'Máscara de Argila Noturna', 
    'Tratamento intensivo noturno para purificação dos poros e controle de brilho.', 
    59.90, 
    'noturno', 
    'static/img/argila noturn.jpg'
);
-- Inserindo no Carrinho (Vincula o usuário 'mariasilva' ao produto ID 1)
INSERT INTO carrinho (usuario, id_produto) 
VALUES ('mariasilva', 1);

-- Inserindo Comentário (Vincula o usuário 'mariasilva' ao produto ID 2)
INSERT INTO comentarios (usuario, comentario, id_produto) 
VALUES (
    'mariasilva', 
    'Estou usando há duas semanas e já notei minha pele muito mais iluminada e macia!', 
    2
);