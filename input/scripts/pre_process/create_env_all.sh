#!/bin/bash

# Criação das pastas, cópia dos arquivos para o hdfs e criação das tabelas

DADOS=("CLIENTES" "DIVISAO" "ENDERECO" "REGIAO" "VENDAS")

#Criação das pastas Datalake e Raw usando o HDFS
echo "Criando a pasta /datalake"
hdfs dfs -mkdir /datalake/
echo "Criando a pasta /datalake/raw"
hdfs dfs -mkdir /datalake/raw

# Loop para criar as pastas dos CSVs usando HDFS, copiar os CSV para as devidas pastas
# e criar as tabelas usando o beeline, usando os dados dos CSV e os scripts de criação da pasta HQL
for i in "${DADOS[@]}"
do
	echo "$i"
    cd /input/raw/
    hdfs dfs -mkdir /datalake/raw/$i
    hdfs dfs -chmod 777 /datalake/raw/$i
    hdfs dfs -copyFromLocal $i.csv /datalake/raw/$i
    beeline -u jdbc:hive2://hive-server:10000 -f /input/scripts/hql/create_table_$i.hql 
done
