CREATE EXTERNAL TABLE IF NOT EXISTS desafio_curso.DIVISAO( 
    Division string,
  `Division Name` string
)
COMMENT 'Tabela Divisao'
ROW FORMAT DELIMITED
FIELDS TERMINATED BY ';'
STORED AS TEXTFILE
location '/datalake/raw/ENDERECO/'
TBLPROPERTIES ("skip.header.line.count"="1");