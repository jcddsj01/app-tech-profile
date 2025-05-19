CREATE TABLE `profissionais` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `nome` varchar(100),
  `genero` enum(M,F,O,N),
  `email` varchar(150) UNIQUE,
  `senioridade` varchar(20)
);

CREATE TABLE `habilidades` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `nome` varchar(50) UNIQUE
);

CREATE TABLE `profissional_habilidades` (
  `profissional_id` int UNIQUE,
  `habilidade_id` int UNIQUE,
  `nivel` varchar(20)
);

CREATE TABLE `experiencias` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `profissional_id` int,
  `empresa` varchar(100),
  `cargo` varchar(100),
  `tempo_meses` int
);

CREATE TABLE `salarios` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `profissional_id` int,
  `salario_mensal` decimal(10,2),
  `data_referencia` date
);

CREATE TABLE `localizacoes` (
  `id` int PRIMARY KEY AUTO_INCREMENT,
  `profissional_id` int,
  `estado` varchar(2),
  `cidade` varchar(100),
  `remoto` tinyint(1)
);

CREATE UNIQUE INDEX `profissional_habilidades_index_0` ON `profissional_habilidades` (`profissional_id`, `habilidade_id`);

ALTER TABLE `profissional_habilidades` ADD FOREIGN KEY (`profissional_id`) REFERENCES `profissionais` (`id`);

ALTER TABLE `profissional_habilidades` ADD FOREIGN KEY (`habilidade_id`) REFERENCES `habilidades` (`id`);

ALTER TABLE `experiencias` ADD FOREIGN KEY (`profissional_id`) REFERENCES `profissionais` (`id`);

ALTER TABLE `salarios` ADD FOREIGN KEY (`profissional_id`) REFERENCES `profissionais` (`id`);

ALTER TABLE `localizacoes` ADD FOREIGN KEY (`profissional_id`) REFERENCES `profissionais` (`id`);
