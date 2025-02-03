# Indicium Tech Code Challenge - Filipe Tavares

Relatório desafio indicium tech para Engenheiro de Dados, o código foi entregue na branch LH_ED_FILIPETAVARES, todos os projetos foram colocados juntos pela facilidade para entregar o desafio aqui no github.


# Meltano

Na pasta ELT contém 2 projetos, o de extração dos dados de uma base postgres e arquivo .CSV e de carregamento dos dados para uma base postgres.


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

No projeto do airflow foram criados 2 arquivos DAG para separar as pipelines de extração e carregamento, elas são agendadas com um intervalo de 15 minutos entre a de extração para de carregamento 
para não ter problema de execução conconrrente entre elas.
Foi adicionado a possibilidade de parametrizar a data de carregamento através de uma variável do airflow "testedata" com a data desejada para execução no formato (YYYY-MM-DD), caso não tenha data preenchida 
será utilizado a data do dia da execução para carregar os dados para o postgres.

