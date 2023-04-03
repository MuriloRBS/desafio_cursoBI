CREATE EXTERNAL TABLE IF NOT EXISTS desafio_curso.REGIAO(
  `Region Code` string,
  `Region Name` string
)
COMMENT 'Tabela Regiao'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ';'
STORED AS TEXTFILE
LOCATION '/datalake/raw/REGIAO'
TBLPROPERTIES ("skip.header.line.count"="1");
