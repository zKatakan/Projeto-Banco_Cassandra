# Bem-vindo ao nosso Projeto de Banco de Dados!

1. Descrição do projeto
* Este projeto consiste na implementação e construção de um Banco de Dados destinado a uma faculdade ficticia com o objetivo de organizar seus dados, utilizamos neste projeto o banco de dados não relacional (NoSQL) Apache Cassandra, este banco trabalha no formato Wide-column Store para armazenar os dados, assim, facilitando as queries de buscas realizadas no Banco e otimizando o tempo de processamento das mesmas.

2. Observações
* Utilizamos do site Datastax para a criação dos Keyspaces e das Tables e utilizamos o proprio CQL Console para a inserção de dados e realização das queries no Banco.
* Foi adaptado o algoritmo de geração de dados do semestre passado para que ele pudesse gerar dados com base na sintaxe aceita pelo Apache Cassandra.
*  Por conta de ser um banco não relacional, o CAssandra não suporta nenhum tipo de JOINS como em bancos relacionais, então utilizamos a desnormalização dos dados em varias tabelas proprias.

3. Como utilizar o código
* Primeiramente é necessario gerar as Tables onde serão armazenados os dados, para isso, basta abrir o documento de criação de coleções clicando aqui e inserir o conteudo no CQL Console
* Após a criação das Tables, você pode utilizar o código de geração de dados para gerar dados novos para inserir clicando aqui ou utilizar o preset de dados clicando aqui, então basta copiar e colar os dados no CQL Console para inserir os dados.
* As queries que atendem os objetivos propostos podem ser vistas clicando aqui.  
