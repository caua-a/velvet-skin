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