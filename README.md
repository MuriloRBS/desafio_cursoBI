<h1 align="center">DESAFIO BIG DATA/BI</h3>

## Tecnologias e Linguagens Utilizadas
<p align="left"> <a href="https://www.docker.com/" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original-wordmark.svg" alt="docker" width="40" height="40"/> </a> <a href="https://git-scm.com/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/git-scm/git-scm-icon.svg" alt="git" width="40" height="40"/> </a> <a href="https://hadoop.apache.org/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/apache_hadoop/apache_hadoop-icon.svg" alt="hadoop" width="40" height="40"/> </a> <a href="https://hive.apache.org/" target="_blank" rel="noreferrer"> <img src="https://www.vectorlogo.zone/logos/apache_hive/apache_hive-icon.svg" alt="hive" width="40" height="40"/> </a> <a href="https://www.python.org" target="_blank" rel="noreferrer"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a> </p>

## 📌 QUAL FOI A PROPOSTA DO DESAFIO?
Foi proposto neste desafio uma pipeline de ingestão de dados, utilizando Hive, em um banco de dados, com esses dados esses vindos inicialmente dos seguintes arquivos CSVs:

 - VENDAS.CSV
 - CLIENTES.CSV
 - ENDERECO.CSV
 - REGIAO.CSV
 - DIVISAO.CSV

## :bulb: O PROCESSO
### O processo é resumidamente é tratar os dados citados acima e transformá-los em tabelas dimensionais, assim facilitando sua utilização em gráficos no Power BI



## 📑 ETAPAS DETALHADAS DO DESAFIO

**Etapa 1** - Envio dos arquivos para o HDFS
     Foi criado um shell script dentro da pasta input/scripts/pre_process que automatiza a criação do ambiente no HDFS, assim criando as pastas datalake e raw.
     Após isso o código copia os CSVs para o ambiente do HDFS em pastas com o mesmo nome do arquivo em si.

**Etapa 2** - Criação do banco DESAFIO_CURSO dentro do Hive Server Criar o banco DEASFIO_CURSO e dentro tabelas no Hive usando o HQL e executando um script shell dentro do hive server na pasta scripts/pre_process.
     Nesta etapa foi apenas executado o shell script criado na etapa anterior, que cria o database desafio_curso dentro do Hive Server e as tabelas baseadas nos CSVs, seguindo essa estrtutura abaixo:
     
    - DESAFIO_CURSO 
        - TBL_VENDAS
        - TBL_CLIENTES
        - TBL_ENDERECO
        - TBL_REGIAO
        - TBL_DIVISAO  
   As tabelas foram criadas a partir do shell script, que dentro de seu loop utiliza os arquivos HQL presentes na pasta input/scripts/hql 

**Etapa 3** - Processamento dos dados no Spark
     Utilizando o spark, os dados foram tratados e processados, dentro de dataframes que buscam os dados diretamente do Hive Server.
     Os dados de todas as tabelas foram armazenados em um único dataframe com o nome df_stage, para que fosse facilitada a criação da tabela fato e suas dimensões.
     Todo o código deste processo descrito está armazenado no arquivo process.py dentro da pasta input/scripts/process e lá contendo mais detalhes do processo realizado junto a seus códigos

**Etapa 4** - Armazenamento das informações na tabela fato e suas dimensões
    
   Como descrito na etapa anterior, os dados tratados foram colocados na fato vendas e suas dimensões(Clientes, Tempo e Local) como é possível ver na estrutura abaixo:

        - FT_VENDAS
        - DIM_CLIENTES
        - DIM_TEMPO
        - DIM_LOCALIDADE

**Etapa 5** - Exportação dos dados para a pasta input/gold
     A exportação dos dados presentes na tabela fato e suas dimensões foram exportados para arquivos CSVs para a pasta input/gold, código também presente no arquivo process.py

**Etapa 6** - Criação de gráficos no Power BI a partir dos dados salvos na pasta Gold. Estes gráficos estão salvos no arquivo Proj_Vendas.pbix na pasta input/app
