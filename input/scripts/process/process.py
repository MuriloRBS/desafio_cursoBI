# Importando todas as funções que serão usadas no código abaixo
from pyspark.sql import SparkSession, dataframe
from pyspark.sql.functions import trim
from pyspark.sql.functions import when, col, sum, count, isnan, round
from pyspark.sql.functions import regexp_replace, concat_ws, sha2, rtrim, substring
from pyspark.sql.functions import unix_timestamp, from_unixtime, to_date
from pyspark.sql.types import StructType, StructField
from pyspark.sql.types import DoubleType, IntegerType, StringType
from pyspark.sql import HiveContext

import os
import re

from pyspark.sql.functions import regexp_replace
from pyspark.sql.functions import when

spark = SparkSession.builder.master("local[*]")\
    .enableHiveSupport()\
    .getOrCreate()

# Criando dataframes diretamente do Hive
df_vendas = spark.sql("select * from desafio_curso.tbl_vendas")
df_clientes = spark.sql("select * from desafio_curso.tbl_clientes")
df_divisao = spark.sql("select * from desafio_curso.tbl_divisao")
df_endereco = spark.sql("select * from desafio_curso.tbl_endereco")
df_regiao = spark.sql("select * from desafio_curso.tbl_regiao")

# Criação da Df_Stage, que é um dataframe com as informações de todas as tabelas, assim contendo as colunas de todas elas em apenas 1 dataframe
df_stage = df_vendas.alias('v') \
    .join(df_clientes.alias('c'), on='customerkey', how='inner') \
    .join(df_divisao.alias('d'), on='division', how='left') \
    .join(df_endereco.alias('e'), on='address number', how='left') \
    .join(df_regiao.alias('r'), on='region code', how='left')

cols = df_stage.columns

#Aqui foi colocado um trim para as colunas que possuem vários espaços vazios dentro, e que assim a substituição por "Não informado" de Strings
# E a substituição de colunas numéricas vazias por 0 seja feita corretamente

df_stage = df_stage.select([
  when(trim(col(c)) == "", "Não Informado").otherwise(col(c)).alias(c) if df_stage.schema[c].dataType == StringType()
  else when(col(c).isNull() | (col(c) == ""), 0).otherwise(col(c)).alias(c)
  for c in cols
])

# Criação das PKs
# Primary Key Clientes
df_stage = df_stage.withColumn('pk_clientes', sha2(concat_ws('_', df_stage['Business Family'],df_stage['Business Unit'],df_stage['Customer'],df_stage['CustomerKey'],df_stage['Customer Type'],df_stage['Division'],df_stage['Line of Business'],df_stage['Phone'],df_stage['Regional Sales Mgr'],df_stage['Search Type']), 256))

# Primary Key Local
df_stage = df_stage.withColumn('pk_local', sha2(concat_ws('_', df_stage['Region Code'], df_stage['Region Name'],df_stage['Division'], df_stage['Division Name'],df_stage['Address Number'], df_stage['City'], df_stage['Country'],df_stage['Customer Address 1'],df_stage['Customer Address 2'],df_stage['Customer Address 3'],df_stage['Customer Address 4'],df_stage['State'],df_stage['Zip Code']), 256))

# Primary Key Tempo
df_stage = df_stage.withColumn('pk_tempo', sha2(concat_ws('_', df_stage['DateKey'],df_stage['Promised Delivery Date'],df_stage['Actual Delivery Date'],df_stage['Invoice Date']), 256))

# Criando a Fato Vendas
ft_vendas = spark.sql("""
                        SELECT DISTINCT pk_clientes, 
                            pk_local,
                            pk_tempo,
                            `invoice number`,
                            COUNT(`invoice number`) as `Qtd Pedidos`,
                            SUM(`Sales Amount`) as `Valor Total`,
                            SUM(`Sales Quantity`) as `Qtd Total`
                            FROM stage 
                            GROUP BY `invoice number`, pk_clientes, pk_local,pk_tempo ORDER BY `Valor Total` DESC
""")

# Criando as Dimensões Clientes, Local e Tempo
dim_clientes = spark.sql("""
    SELECT DISTINCT
        pk_clientes,
        CustomerKey,
        Customer,
        `Customer Type`,
        `Line of Business`,
        `Business Unit`,
        `Business Family`,
        `Regional Sales Mgr`,
        Phone,
        Division
       
   FROM stage
""").dropDuplicates()


dim_local = spark.sql('''
    SELECT DISTINCT
        pk_local,
        `Region Code`,
        `Region Name`,
        `Address Number`,
        City,
        Country,
        `Customer Address 1`,
        `Customer Address 2`,
        `Customer Address 3`,
        `Customer Address 4`,
        State,
        `Zip Code`
        
    FROM stage
''').dropDuplicates()

dim_tempo = spark.sql('''
    SELECT DISTINCT
        pk_tempo,
        `Actual Delivery Date`,
        DateKey,
        `Invoice Date`,
        `Promised Delivery Date`
    FROM
        stage
''').dropDuplicates()

# Função para salvar os dados na pasta input/gold
def salvar_df(df, file):
    output = "/input/desafio_hive/gold/" + file
    erase = "hdfs dfs -rm " + output + "/*"
    rename = "hdfs dfs -get /datalake/gold/"+file+"/part-* /input/desafio_hive/gold/"+file+".csv"
    print(rename)
    
    
    df.coalesce(1).write\
        .format("csv")\
        .option("header", True)\
        .option("delimiter", ";")\
        .mode("overwrite")\
        .save("/datalake/gold/"+file+"/")

    os.system(erase)
    os.system(rename)

# Função na prática para salvar as dimensões em CSVs na pasta Gold
salvar_df(dim_clientes, 'DIM_CLIENTES')
salvar_df(dim_tempo, 'DIM_TEMPO')
salvar_df(dim_clientes, 'DIM_LOCAL')

# Mesma função de salvamento, agora salvando a ft_vendas

salvar_df(ft_vendas,'FT_VENDAS')
