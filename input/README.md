Aqui estão as pastas mencionadas no README da pasta principal e uma breve descrição de cada

Na pasta Raw estão os CSVs originais, sem tratamento

Dentro da pasta script existem a pasta de pre_process e process, onde uma guarda o arquivo que preparou o ambiente HDFS e do hive, enquanto a outra o arquivo com todo o tratamento de dados dos CSVs da Raw e exportação para CSV para ser usado no Power BI.

Na pasta Run está o arquivo que executa o arquivo process.py, que se encontra na pasta process de scripts

Na pasta Gold estão os CSVs tratados, dentre eles a Fato venda e suas dimensões: Clientes, Tempo e Local prontos para serem usados no Power BI

E por último, na pasta app está o arquivo do Power BI, consumindo dados presentes na pasta Gold e apresentando alguns gráficos feitos por mim
