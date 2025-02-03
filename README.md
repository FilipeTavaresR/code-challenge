# Indicium Tech Code Challenge - Filipe Tavares

Relatório desafio indicium tech para Engenheiro de Dados, o código foi entregue na branch LH_ED_FILIPETAVARES, todos os projetos foram colocados juntos pela facilidade para entregar o desafio aqui no github.

# Ferramentas necessárias para executar o projeto.
Linux
Postgres
Github
Airflow
Meltano (optei por utilizar o meltano ao invés do embulk por ter material indicado na indicium academy e por ter mais material disponível de documentação)
(Teria sido muito melhor eu ter configurado uma máquina virtual no docker, mas eu já estava em um passo muito avançado do projeto e não daria tempo para configurar e entregar essa máquina a tempo, mas para um projeto de produção eu acredito que seria a melhor opção)

# Cronograma
O cronograma foi criado conforme os requisitos do projeto separado por etapas menores para quando todas estiverem completas o desafio ser entregue em sua complitude.
![image](dados/cronograma.jpg)

# Meltano

Na pasta ELT contém 2 projetos (para melhor organização das etapas), o de extração dos dados de uma base postgres e arquivo .CSV e de carregamento dos dados para uma base postgres.

## Extração de dados

O projeto de extração utiliza 2 plugins para extrair dados, 1 para capturar os dados da base postgres(tap-postgres) em cada tabela e exportar para um arquivo CSV através de um plugin de carregamento(target-csv).
A base de dados foi instalado um postgres local e importado o backup .sql do repositório do desafio.
O segundo plugin utiliza um extrator de arquivo .CSV (tap-csv) e utiliza o mesmo plugin para carregamento(target-csv) utilizado na extração dos dados do postgres.
O arquivo .csv foi adicionado a um diretório local (simulando um diretório externo ao projeto), copiado do repositório do desafio.
Ambos salvam arquivos .CSV com os respectivos nomes seguindo o padrão:

output/data/postgres/{table}/2024-01-01/file.csv
output/data/postgres/{table}/2024-01-02/file.csv
output/data/csv/2024-01-02/file.csv

(Ficou um gap que está salvando o nome do eschema do postgres no nome dos arquivos, mantive dessa forma pois iria extrapolar o tempo de entrega do projeto para solucionar)

## Carregamento de dados

O projeto de carregamento de dados utiliza um plugin para ler os dados dos arquivos .CSV (tap-csv) que faz o stream para carregar os dados na base postgres através do plugin (target-postgres).
Este salva as tabelas com os mesmos nomes dos arquivos.
(Ficou um gap para retirar o ".csv" do nome das tabelas, mas o tempo estava esgotando para entrega do projeto e acabei optando por manter dessa forma sem pesquisar uma solução)

# Airflow

No projeto do airflow foram criados 2 arquivos DAG para separar as pipelines de extração e carregamento, elas são agendadas com um intervalo de 15 minutos entre a de extração para de carregamento para não ter problema de execução conconrrente entre elas.

## Pipeline de extração de dados

Foi criado o arquivo data_extract.py dentro da pasta dags para configurar a pipeline de extração de dados.
A extração de dados foi configurada para executar diáriamente de forma automática e configurada para executar 15 minutos antes da pipeline de carregamento dos dados para garantir que seja finalizada a execução antes de realizar o carregamento dos dados. 

## Pipeline de carregamento de dados

Foi criado o arquivo data_loader.py dentro da pasta dags para configurar a pipeline de carregamento de dados.
Foi adicionado a possibilidade de parametrizar a data de carregamento através das variáveis personalizadas do airflow "testedata" com a data desejada para execução no formato (YYYY-MM-DD).
Esta variável pode ser criada diretamente na interface do airflow, no meu admin>variáveis, basta criar uma variável com a chave "testedata" e valor com a data, caso não tenha data preenchida na variável será utilizado a data do dia da execução para carregar os dados para o postgres (não pode esquecer de manter a variável vazia para execução diária de forma natural).

