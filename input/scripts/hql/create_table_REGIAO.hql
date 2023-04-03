CREATE EXTERNAL TABLE IF NOT EXISTS desafio.curso.REGIAO (
  `Region Code` string,
  `Region Name` string
)
COMMENT 'Tabela Regiao'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ';'
LOCATION '/datalake/raw/REGIAO'
TBLPROPERTIES ("skip.header.line.count"="1");
