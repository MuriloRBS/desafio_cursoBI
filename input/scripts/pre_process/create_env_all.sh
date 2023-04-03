#!/bin/bash

# Criação das pastas, cópia dos arquivos para o hdfs e criação das tabelas

DADOS=("CLIENTES" "DIVISAO" "ENDERECO" "REGIAO" "VENDAS")

for i in "${DADOS[@]}"
do
	echo "$i"
    cd /input/raw/
    hdfs dfs -mkdir /datalake/raw/$i
    hdfs dfs -chmod 777 /datalake/raw/$i
    hdfs dfs -copyFromLocal $i.csv /datalake/raw/$i
    beeline -u jdbc:hive2://hive-server:10000 -f /input/scripts/hql/create_table_$i.hql 
done
