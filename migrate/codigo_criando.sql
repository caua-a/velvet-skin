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


-- INSERÇÃO DE TODOS OS PRODUTOS DA PASTA (COM CAMINHO ABSOLUTO /)
INSERT INTO produtos (produto, descricao, preco, categoria, imagem) 
VALUES 

(
    'Máscara de Argila Noturna (Night Clay Mask)', 
    'Purificação noturna profunda com argila rica em minerais, lavanda e camomila. Revitaliza e refina a pele.', 
    89.90, 
    'noturno', 
    '/static/img/argila noturn.jpg'
),
(
    'Imagem de Teste 1',
    'Produto de teste para validação de layout do catálogo.',
    29.90,
    'diurno',
    '/static/img/img_teste1.png'
),

(
    'Protetor Solar Facial & Corporal FPS 50+', 
    'Proteção de amplo espectro UVA/UVB, resistente à água. Ação anti-manchas com Niacinamida e Óleo de Amêndoas. Toque seco.', 
    85.00, 
    'diurno', 
    '/static/img/protetor solar.png'
),
(
    'Sérum Facial Normal',
    'Sérum de manutenção diária para hidratação leve e controle de textura.',
    95.00,
    'diurno',
    '/static/img/seru normal.jpg'
),
(
    'Sérum Hidratante Facial (Hydrating Facial Serum)', 
    'Sérum diário com AHA (Alfa-hidroxiácidos) e Ácido Hialurónico. Promove revitalização e efeito Glow radiante.', 
    119.90, 
    'diurno', 
    '/static/img/serum facial branco.png'
),
(
    'Sérum Noturno Renovador (Night Serum)', 
    'Tratamento intensivo de reparação noturna (Night Recovery & Repair). Estimula a renovação celular para acordar com uma pele iluminada.', 
    134.90, 
    'noturno', 
    '/static/img/serum retinol noturno.png'
),
(
    'Duo Creme Marrom e Sérum Diurno',
    'Tratamento combinado de alta performance para o período do dia.',
    159.90,
    'diurno',
    '/static/img/serum e um creme marrom diurno.png'
),
(
    'Creme Noturno Restaurador de Ceramidas (Night Restoring Cream)', 
    'Deep Night Hydration • Ceramides & Peptides • Restores and Nourishes the Skin Barrier. Hidratação profunda para restauração da barreira cutânea.', 
    94.90, 
    'noturno', 
    '/static/img/creme_restoring.png'
),
(
    'Sérum Noturno de Peptídeos e Colágeno (Night Peptide Serum)', 
    'Targeted Night Repair • Peptides & Collagen Complex • Firms and Improves Skin Elasticity. Atua diretamente na firmeza e linhas de expressão.', 
    124.00, 
    'noturno', 
    '/static/img/serum_night.png'
),
(
    'Bálsamo Facial de Reparação Intensiva (Deep Repair Facial Balm)', 
    'Intense Night Nourishment • High Concentration • Repairs and Rejuvenates Damaged Skin. Nutrição noturna concentrada e reparação celular.', 
    139.90, 
    'noturno', 
    '/static/img/balm.png'
),
(
    'Tônico Esfoliante Noturno AHA + BHA', 
    'Night Exfoliating Toner • Gentle Renewal Formula • Promotes Even Skin Tone. Renovador celular líquido de uso exclusivo noturno.', 
    68.00, 
    'noturno', 
    '/static/img/esfoliante.png'
);


-- INSERT INTO produtos (produto, descricao, preco, categoria, imagem) VALUES ('Tônico Esfoliante Noturno AHA + BHA', 'Night Exfoliating Toner • Gentle Renewal Formula • Promotes Even Skin Tone. Renovador celular líquido de uso exclusivo noturno.', 68.00, 'noturno', /static/img/esfoliante.png');