DESAFIO BIG DATA/BI

📌 O QUE FOI FEITO?
Neste desafio foram feitas as ingestões dos dados que estão na pasta /raw onde vamos ter alguns arquivos .csv de um banco relacional de vendas.

 - VENDAS.CSV
 - CLIENTES.CSV
 - ENDERECO.CSV
 - REGIAO.CSV
 - DIVISAO.CSV

O Objetivo do trabalho foi atingido, que era basicamente prover dados em uma pasta desafio_curso/gold em .csv para ser consumido por um relatório em PowerBI dentro da pasta 'app'

📑 ETAPAS DO DESAFIO

Etapa 1 - Envio dos arquivos para o HDFS
     Foi criado um shell script dentro da pasta input/scripts/pre_process que automatiza a criação do ambiente no HDFS, assim criando as pastas datalake e raw.
     Após isso o código copia os CSVs para o ambiente do HDFS em pastas com o mesmo nome do arquivo em si.

Etapa 2 - Criação do banco DESAFIO_CURSO dentro do Hive Server Criar o banco DEASFIO_CURSO e dentro tabelas no Hive usando o HQL e executando um script shell dentro do hive server na pasta scripts/pre_process.
     Nesta etapa foi apenas executado o shell script criado na etapa anterior, que cria o database desafio_curso dentro do Hive Server e as tabelas baseadas nos CSVs, seguindo essa estrtutura abaixo:
     
    - DESAFIO_CURSO 
        - TBL_VENDAS
        - TBL_CLIENTES
        - TBL_ENDERECO
        - TBL_REGIAO
        - TBL_DIVISAO
    As tabelas foram criadas a partir do shell script, que dentro de seu loop utiliza os arquivos HQL presentes na pasta input/scripts/hql 

Etapa 3 - Processamento dos dados no Spark
     Utilizando o spark, os dados foram tratados e processados, dentro de dataframes que buscam os dados diretamente do Hive Server.
     Os dados de todas as tabelas foram armazenados em um único dataframe com o nome df_stage, para que fosse facilitada a criação da tabela fato e suas dimensões.
     Todo o código deste processo descrito está armazenado no arquivo process.py dentro da pasta input/scripts/process e lá contendo mais detalhes do processo realizado junto a seus códigos

Etapa 4 - Armazenamento das informações na tabela fato e suas dimensões
    
   Como descrito na etapa anterior, os dados trataram foram colocados na fato vendas e suas dimensões(Clientes, Tempo e Local) como é possível ver na estrutura abaixo:

        - FT_VENDAS
        - DIM_CLIENTES
        - DIM_TEMPO
        - DIM_LOCALIDADE

Etapa 5 - Exportação dos dados para a pasta input/gold
     A exportação dos dados presentes na tabela fato e suas dimensões foram exportados para arquivos CSVs para a pasta input/gold, código também presente no arquivo process.py

Última etapa - Criação de gráficos no Power BI a partir dos dados salvos na pasta Gold. Estes gráficos estão salvos no arquivo Proj_Vendas.pbix na pasta input/app
