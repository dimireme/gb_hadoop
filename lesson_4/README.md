## Урок 4. Заливка данных в Hadoop. Форматы данных.

### Часть 1. Форматы данных.

Есть большая таблица по имени

```
create external table hive_db.citation_data
(
  oci string,
  citing string,
  cited string,
  creation string,
  timespan string,
  journal_sc string,
  author_sc string
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
location '/test_datasets/citation'
```

Её размер вот такой:

```
hdfs dfs -du -h -s /test_datasets/citation
97.2 G 291.5 G /test_datasets/citation
```

Что вам нужно сделать

**1. Создать таблицы в форматах PARQUET/ORC/AVRO c компрессией и без оной. (Выберите один вариант, например ORC с компрессией).**

Выберем вариант PARQUET с компрессией.

```
set parquet.compression=SNAPPY;

create external table citation_data_parquet (
    oci string,
    citing string,
    cited string,
    creation string,
    timespan string,
    journal_sc string,
    author_sc string
)
STORED AS PARQUET
LOCATION '/user/student3_7/citation_data_parquet';
```

**2. Заполнить данными из большой таблицы hive_db.citation_data**

```
-- set hive.exec.parallel=true;

insert into student3_7_les3.citation_data_parquet
select * from hive_db.citation_data;
```

**3. Посмотреть на получившийся размер данных.**

```
[student3_7@manager ~]$ hdfs dfs -du -h -s /user/student3_7/citation_data_parquet
22.7 G  68.2 G  /user/student3_7/citation_data_parquet
```

**4. Сделать выводы о эффективности хранения и компресии.**

Объём данных изменился с 97.2 до 22.7 гигабайт. Данные в таблица с форматом PARQUET с сжатием занимают в ~4 раза меньше места чем исходные csv файлы.

### Часть 2. SQOOP.

Простое задание довольно :)

**1. Создать отдельную БД в HIve.**

```
create database student3_7_les4;
```

**2. Посмотреть при помощи SQOOP содержимое БД в PosgreSQL.**

```
[student3_7@manager ~]$ sqoop list-tables --connect jdbc:postgresql://node3.novalocal/pg_db --username exporter -P
Warning: /opt/cloudera/parcels/CDH-5.16.2-1.cdh5.16.2.p0.8/bin/../lib/sqoop/../accumulo does not exist! Accumulo imports will fail.
Please set $ACCUMULO_HOME to the root of your Accumulo installation.
20/04/18 00:36:28 INFO sqoop.Sqoop: Running Sqoop version: 1.4.6-cdh5.16.2
Enter password:
20/04/18 00:36:36 INFO manager.SqlManager: Using default fetchSize of 1000
character
character_work
paragraph
sales_large
wordform
work
chapter
```

В БД 7 таблиц: `character`, `character_work`, `paragraph`, `sales_large`, `wordform`, `work`, `chapter`.

**3. Импортировать в нее три любые таблицы из базы pg_db в PosgreSQL используя SQOOP. Для каждой таблице используйте отдельный формат хранения -- ORC/Parquet/AVRO. Рекомендую захватить таблицу sales_large - там порядка 10 миллионов записей, она будет достаточно репрезентативна для проверки компрессии.**

Попробуем скопировать таблицу `work` в формат AVRO.

<details>

<summary>Способ 1 (долгий)</summary>

Узнаем структуру таблицы следующим образом:

```
[student3_7@manager ~]$ sqoop import --m 1 --connect jdbc:postgresql://node3.novalocal/pg_db --username exporter -P --query "SELECT column_name, DATA_TYPE FROM INFORMATION_SCHEMA.Columns WHERE table_name='work' AND \$CONDITIONS" --target-dir '/user/student3_7/shakespeare/work/'
```

```
[student3_7@manager ~]$ hdfs dfs -ls -r /user/student3_7/shakespeare/work/
Found 2 items
-rw-r--r--   3 student3_7 student3_7        197 2020-04-18 09:55 /user/student3_7/shakespeare/work/part-m-00000
-rw-r--r--   3 student3_7 student3_7          0 2020-04-18 09:55 /user/student3_7/shakespeare/work/_SUCCESS
```

```
[student3_7@manager ~]$ hdfs dfs -cat /user/student3_7/shakespeare/work/part-m-00000
workid,character varying
title,character varying
longtitle,character varying
year,integer
genretype,character varying
notes,text
source,character varying
totalwords,integer
totalparagraphs,integer
```

Создадим hive-таблицу:

```
SET avro.output.codec=snappy;

CREATE EXTERNAL TABLE student3_7_les4.work
(
    workid STRING,
    title STRING,
    longtitle STRING,
    `year` INT,
    genretype STRING,
    notes STRING,
    source STRING,
    totalwords INT,
    totalparagraphs INT
)
STORED AS AVRO
LOCATION '/user/student3_7/shakespeare/work'
;
```

Скопируем данные из postgresql в HDFS

```
[student3_7@manager ~]$ sqoop import --connect jdbc:postgresql://node3.novalocal:5432/pg_db --username exporter -P --table work --target-dir /user/student3_7/shakespeare/work --as-avrodatafile
```

Посмотрим результат

```
select * from work limit 10;
```

| work.workid  | work.title                | work.longtitle                            | work.year | work.genretype | work.notes | work.source | work.totalwords | work.totalparagraphs |
| ------------ | ------------------------- | ----------------------------------------- | --------- | -------------- | ---------- | ----------- | --------------- | -------------------- |
| 12night      | Twelfth Night             | Twelfth Night, Or What You Will           | 1599      | c              | NULL       | Moby        | 19837           | 1031                 |
| allswell     | All's Well That Ends Well | All's Well That Ends Well                 | 1602      | c              | NULL       | Moby        | 22997           | 1025                 |
| antonycleo   | Antony and Cleopatra      | Antony and Cleopatra                      | 1606      | t              | NULL       | Moby        | 24905           | 1344                 |
| asyoulikeit  | As You Like It            | As You Like It                            | 1599      | c              | NULL       | Gutenberg   | 21690           | 872                  |
| comedyerrors | Comedy of Errors          | The Comedy of Errors                      | 1589      | c              | NULL       | Moby        | 14692           | 661                  |
| coriolanus   | Coriolanus                | Coriolanus                                | 1607      | t              | NULL       | Moby        | 27577           | 1226                 |
| cymbeline    | Cymbeline                 | Cymbeline, King of Britain                | 1609      | h              | NULL       | Moby        | 27565           | 971                  |
| hamlet       | Hamlet                    | Tragedy of Hamlet, Prince of Denmark, The | 1600      | t              | NULL       | Gutenberg   | 30558           | 1275                 |
| henry4p1     | Henry IV, Part I          | History of Henry IV, Part I               | 1597      | h              | NULL       | Moby        | 24579           | 884                  |
| henry4p2     | Henry IV, Part II         | History of Henry IV, Part II              | 1597      | h              | NULL       | Gutenberg   | 25692           | 1013                 |

</details>

<details>
<summary>Способ 2 (оптитмальный)</summary>

Удалим папку `/user/student3_7/shakespeare/work` и дропнем таблицу `student3_7_les4.work`.

Скопируем данные из postgresql в HDFS.

```
[student3_7@manager ~]$ sqoop import --connect jdbc:postgresql://node3.novalocal:5432/pg_db --username exporter -P --table work --target-dir /user/student3_7/shakespeare/work --as-avrodatafile
```

При этом в теукущей локальной дирекутории создаётся файл `work.avsc`, содержащий схему таблицы. Скопируем её в HDFS.

```
[student3_7@manager ~]$ hdfs dfs -copyFromLocal work.avsc /user/student3_7/shakespeare/
```

Создадим hive-таблицу, указав путь до AVRO-файлов в HDFS и путь до схемы таблицы.

```
CREATE EXTERNAL TABLE student3_7_les4.work
STORED AS AVRO
LOCATION '/user/student3_7/shakespeare/work'
TBLPROPERTIES ('avro.schema.url'='/user/student3_7/shakespeare/work.avsc');
```

```
select * from work limit 10;
```

| work.workid  | work.title                | work.longtitle                            | work.year | work.genretype | work.notes | work.source | work.totalwords | work.totalparagraphs |
| ------------ | ------------------------- | ----------------------------------------- | --------- | -------------- | ---------- | ----------- | --------------- | -------------------- |
| 12night      | Twelfth Night             | Twelfth Night, Or What You Will           | 1599      | c              | NULL       | Moby        | 19837           | 1031                 |
| allswell     | All's Well That Ends Well | All's Well That Ends Well                 | 1602      | c              | NULL       | Moby        | 22997           | 1025                 |
| antonycleo   | Antony and Cleopatra      | Antony and Cleopatra                      | 1606      | t              | NULL       | Moby        | 24905           | 1344                 |
| asyoulikeit  | As You Like It            | As You Like It                            | 1599      | c              | NULL       | Gutenberg   | 21690           | 872                  |
| comedyerrors | Comedy of Errors          | The Comedy of Errors                      | 1589      | c              | NULL       | Moby        | 14692           | 661                  |
| coriolanus   | Coriolanus                | Coriolanus                                | 1607      | t              | NULL       | Moby        | 27577           | 1226                 |
| cymbeline    | Cymbeline                 | Cymbeline, King of Britain                | 1609      | h              | NULL       | Moby        | 27565           | 971                  |
| hamlet       | Hamlet                    | Tragedy of Hamlet, Prince of Denmark, The | 1600      | t              | NULL       | Gutenberg   | 30558           | 1275                 |
| henry4p1     | Henry IV, Part I          | History of Henry IV, Part I               | 1597      | h              | NULL       | Moby        | 24579           | 884                  |
| henry4p2     | Henry IV, Part II         | History of Henry IV, Part II              | 1597      | h              | NULL       | Gutenberg   | 25692           | 1013                 |

Результат такой же, как и в предыдущем случае.

</details>

Данные из таблицы `paragraph` импортируем в формате Parquet. При выполнении команды `sqoop` с флагом `--as-parquetfile` схема импортированной таблицы не создаётся. Создадим таблицу вручную. Структуру таблицы узнали, посмотрев в таблицу `INFORMATION_SCHEMA.Columns` в postgresql.

```
set parquet.compression=SNAPPY;

CREATE EXTERNAL TABLE paragraph (
    workid STRING,
    paragraphid INT,
    paragraphnum INT,
    charid STRING,
    plaintext STRING,
    phonetictext STRING,
    stemtext STRING,
    paragraphtype STRING,
    section INT,
    chapter INT,
    charcount INT,
    wordcount INT
)
STORED AS PARQUET
LOCATION '/user/student3_7/shakespeare/paragraph';
```

Импорт данных:

```
[student3_7@manager ~]$ sqoop import --connect jdbc:postgresql://node3.novalocal/pg_db --username exporter -P --table paragraph --hive-import --hive-database student3_7_les4 --hive-table paragraph --as-parquetfile
```

<details>

<summary>Лог выполнения</summary>

```
Warning: /opt/cloudera/parcels/CDH-5.16.2-1.cdh5.16.2.p0.8/bin/../lib/sqoop/../accumulo does not exist! Accumulo imports will fail.
Please set $ACCUMULO_HOME to the root of your Accumulo installation.
20/04/18 12:26:21 INFO sqoop.Sqoop: Running Sqoop version: 1.4.6-cdh5.16.2
Enter password:
20/04/18 12:26:27 INFO tool.BaseSqoopTool: Using Hive-specific delimiters for output. You can override
20/04/18 12:26:27 INFO tool.BaseSqoopTool: delimiters with --fields-terminated-by, etc.
20/04/18 12:26:27 INFO manager.SqlManager: Using default fetchSize of 1000
20/04/18 12:26:27 INFO tool.CodeGenTool: Beginning code generation
20/04/18 12:26:27 INFO tool.CodeGenTool: Will generate java class as codegen_paragraph
20/04/18 12:26:27 INFO manager.SqlManager: Executing SQL statement: SELECT t.* FROM "paragraph" AS t LIMIT 1
20/04/18 12:26:27 INFO orm.CompilationManager: HADOOP_MAPRED_HOME is /opt/cloudera/parcels/CDH/lib/hadoop-mapreduce
Note: /tmp/sqoop-student3_7/compile/9958c7e61eb08dbeda4cc5399655d4d0/codegen_paragraph.java uses or overrides a deprecated API.
Note: Recompile with -Xlint:deprecation for details.
20/04/18 12:26:29 INFO orm.CompilationManager: Writing jar file: /tmp/sqoop-student3_7/compile/9958c7e61eb08dbeda4cc5399655d4d0/codegen_paragraph.jar
20/04/18 12:26:29 INFO manager.DirectPostgresqlManager: Beginning psql fast path import
20/04/18 12:26:29 WARN manager.DirectPostgresqlManager: File import layoutParquetFile is not supported by
20/04/18 12:26:29 WARN manager.DirectPostgresqlManager: Postgresql direct import; import will proceed as text files.
20/04/18 12:26:29 INFO manager.SqlManager: Executing SQL statement: SELECT t.* FROM "paragraph" AS t LIMIT 1
20/04/18 12:26:29 INFO manager.DirectPostgresqlManager: Copy command is COPY (SELECT "workid", "paragraphid", "paragraphnum", "charid", "plaintext", "phonetictext", "stemtext", "paragraphtype", "section", "chapter", "charcount", "wordcount" FROM "paragraph" WHERE 1=1) TO STDOUT WITH DELIMITER E'\1' CSV ;
20/04/18 12:26:29 INFO manager.DirectPostgresqlManager: Performing import of table paragraph from database pg_db
20/04/18 12:26:31 INFO manager.DirectPostgresqlManager: Transfer loop complete.
20/04/18 12:26:31 INFO manager.DirectPostgresqlManager: Transferred 13.3311 MB in 1.127 seconds (11.8286 MB/sec)
[student3_7@manager ~]$ sqoop import --connect jdbc:postgresql://node3.novalocal/pg_db --username exporter -P --table paragraph --hive-import --hive-database student3_7_les4 --hive-table paragraph --as-parquetfile
Warning: /opt/cloudera/parcels/CDH-5.16.2-1.cdh5.16.2.p0.8/bin/../lib/sqoop/../accumulo does not exist! Accumulo imports will fail.
Please set $ACCUMULO_HOME to the root of your Accumulo installation.
20/04/18 12:30:03 INFO sqoop.Sqoop: Running Sqoop version: 1.4.6-cdh5.16.2
Enter password:
20/04/18 12:30:08 INFO tool.BaseSqoopTool: Using Hive-specific delimiters for output. You can override
20/04/18 12:30:08 INFO tool.BaseSqoopTool: delimiters with --fields-terminated-by, etc.
20/04/18 12:30:08 INFO manager.SqlManager: Using default fetchSize of 1000
20/04/18 12:30:08 INFO tool.CodeGenTool: Beginning code generation
20/04/18 12:30:08 INFO tool.CodeGenTool: Will generate java class as codegen_paragraph
20/04/18 12:30:09 INFO manager.SqlManager: Executing SQL statement: SELECT t.* FROM "paragraph" AS t LIMIT 1
20/04/18 12:30:09 INFO orm.CompilationManager: HADOOP_MAPRED_HOME is /opt/cloudera/parcels/CDH/lib/hadoop-mapreduce
Note: /tmp/sqoop-student3_7/compile/548be7603351a1ae3b1c9137715f2304/codegen_paragraph.java uses or overrides a deprecated API.
Note: Recompile with -Xlint:deprecation for details.
20/04/18 12:30:10 INFO orm.CompilationManager: Writing jar file: /tmp/sqoop-student3_7/compile/548be7603351a1ae3b1c9137715f2304/codegen_paragraph.jar
20/04/18 12:30:10 WARN manager.PostgresqlManager: It looks like you are importing from postgresql.
20/04/18 12:30:10 WARN manager.PostgresqlManager: This transfer can be faster! Use the --direct
20/04/18 12:30:10 WARN manager.PostgresqlManager: option to exercise a postgresql-specific fast path.
20/04/18 12:30:10 INFO mapreduce.ImportJobBase: Beginning import of paragraph
20/04/18 12:30:11 INFO Configuration.deprecation: mapred.jar is deprecated. Instead, use mapreduce.job.jar
20/04/18 12:30:12 INFO manager.SqlManager: Executing SQL statement: SELECT t.* FROM "paragraph" AS t LIMIT 1
20/04/18 12:30:12 INFO manager.SqlManager: Executing SQL statement: SELECT t.* FROM "paragraph" AS t LIMIT 1
20/04/18 12:30:13 INFO hive.metastore: Trying to connect to metastore with URI thrift://manager.novalocal:9083
20/04/18 12:30:13 INFO hive.metastore: Opened a connection to metastore, current connections: 1
20/04/18 12:30:13 INFO hive.metastore: Connected to metastore.
20/04/18 12:30:13 WARN mapreduce.DataDrivenImportJob: Target Hive table 'paragraph' exists! Sqoop will append data into the existing Hive table. Consider using --hive-overwrite, if you do NOT intend to do appending.
20/04/18 12:30:14 INFO Configuration.deprecation: mapred.map.tasks is deprecated. Instead, use mapreduce.job.maps
20/04/18 12:30:14 INFO client.RMProxy: Connecting to ResourceManager at manager.novalocal/89.208.221.132:8032
20/04/18 12:30:40 INFO db.DBInputFormat: Using read commited transaction isolation
20/04/18 12:30:40 INFO db.DataDrivenDBInputFormat: BoundingValsQuery: SELECT MIN("paragraphid"), MAX("paragraphid") FROM "paragraph"
20/04/18 12:30:40 INFO db.IntegerSplitter: Split size: 8866; Num splits: 4 from: 630863 to: 666327
20/04/18 12:30:40 INFO mapreduce.JobSubmitter: number of splits:4
20/04/18 12:30:40 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1583843553969_0490
20/04/18 12:30:41 INFO impl.YarnClientImpl: Submitted application application_1583843553969_0490
20/04/18 12:30:41 INFO mapreduce.Job: The url to track the job: http://manager.novalocal:8088/proxy/application_1583843553969_0490/
20/04/18 12:30:41 INFO mapreduce.Job: Running job: job_1583843553969_0490
20/04/18 12:30:55 INFO mapreduce.Job: Job job_1583843553969_0490 running in uber mode : false
20/04/18 12:30:55 INFO mapreduce.Job:  map 0% reduce 0%
20/04/18 12:31:10 INFO mapreduce.Job:  map 25% reduce 0%
20/04/18 12:31:14 INFO mapreduce.Job:  map 50% reduce 0%
20/04/18 12:31:17 INFO mapreduce.Job:  map 75% reduce 0%
20/04/18 12:31:25 INFO mapreduce.Job:  map 100% reduce 0%
20/04/18 12:31:25 INFO mapreduce.Job: Job job_1583843553969_0490 completed successfully
20/04/18 12:31:25 INFO mapreduce.Job: Counters: 30
        File System Counters
                FILE: Number of bytes read=0
                FILE: Number of bytes written=989420
                FILE: Number of read operations=0
                FILE: Number of large read operations=0
                FILE: Number of write operations=0
                HDFS: Number of bytes read=22741
                HDFS: Number of bytes written=8865687
                HDFS: Number of read operations=152
                HDFS: Number of large read operations=0
                HDFS: Number of write operations=40
        Job Counters
                Launched map tasks=4
                Other local map tasks=4
                Total time spent by all maps in occupied slots (ms)=41780
                Total time spent by all reduces in occupied slots (ms)=0
                Total time spent by all map tasks (ms)=41780
                Total vcore-milliseconds taken by all map tasks=41780
                Total megabyte-milliseconds taken by all map tasks=42782720
        Map-Reduce Framework
                Map input records=35465
                Map output records=35465
                Input split bytes=505
                Spilled Records=0
                Failed Shuffles=0
                Merged Map outputs=0
                GC time elapsed (ms)=1048
                CPU time spent (ms)=32690
                Physical memory (bytes) snapshot=1792454656
                Virtual memory (bytes) snapshot=11387936768
                Total committed heap usage (bytes)=1361051648
        File Input Format Counters
                Bytes Read=0
        File Output Format Counters
                Bytes Written=0
20/04/18 12:31:25 INFO mapreduce.ImportJobBase: Transferred 8.455 MB in 70.4625 seconds (122.8723 KB/sec)
20/04/18 12:31:25 INFO mapreduce.ImportJobBase: Retrieved 35465 records.
```

</details>

То же самое, но таблица создаётся автоматически и данные помещаются в папку `/user/hive/warehouse/student3_7_les4.db/paragraph_2/`.

Посмотрим на созданные файлы:

```
[student3_7@manager ~]$ hdfs dfs -ls /user/student3_7/shakespeare/paragraphFound 5 items
drwxr-xr-x   - student3_7 student3_7          0 2020-04-18 13:20 /user/student3_7/shakespeare/paragraph/.signals
-rw-r--r--   3 student3_7 supergroup    2025889 2020-04-18 13:20 /user/student3_7/shakespeare/paragraph/5b0c51dc-4a1e-4c30-b349-d4b5e11b8313.parquet
-rw-r--r--   3 student3_7 supergroup    2155202 2020-04-18 13:20 /user/student3_7/shakespeare/paragraph/9b8041c5-0163-4c3c-988d-54fa05be1da6.parquet
-rw-r--r--   3 student3_7 supergroup    2389502 2020-04-18 13:20 /user/student3_7/shakespeare/paragraph/dacf4058-fa57-4ea3-bca5-882f987b1d1c.parquet
-rw-r--r--   3 student3_7 supergroup    2281342 2020-04-18 13:20 /user/student3_7/shakespeare/paragraph/f3042c29-1715-48e9-8a99-db2815be4f0d.parquet
```

Проверим компрессию файлов:

```
[student3_7@manager ~]$ parquet-tools meta hdfs://manager.novalocal:8020/user/student3_7/shakespeare/paragraph/5b0c51dc-4a1e-4c30-b349-d4b5e11b8313.parquet
```

<details>

<summary>Результат</summary>

```
creator:       parquet-mr version 1.5.0-cdh5.16.2 (build ${buildNumber})
extra:         parquet.avro.schema = {"type":"record","name":"paragraph","fields":[{"name":"workid","type":["null","string"],"doc":"Converted from 'string'","default":nul [more]...

file schema:   paragraph
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
workid:        OPTIONAL BINARY O:UTF8 R:0 D:1
paragraphid:   OPTIONAL INT32 R:0 D:1
paragraphnum:  OPTIONAL INT32 R:0 D:1
charid:        OPTIONAL BINARY O:UTF8 R:0 D:1
plaintext:     OPTIONAL BINARY O:UTF8 R:0 D:1
phonetictext:  OPTIONAL BINARY O:UTF8 R:0 D:1
stemtext:      OPTIONAL BINARY O:UTF8 R:0 D:1
paragraphtype: OPTIONAL BINARY O:UTF8 R:0 D:1
section:       OPTIONAL INT32 R:0 D:1
chapter:       OPTIONAL INT32 R:0 D:1
charcount:     OPTIONAL INT32 R:0 D:1
wordcount:     OPTIONAL INT32 R:0 D:1

row group 1:   RC:8866 TS:2994824
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
workid:         BINARY SNAPPY DO:0 FPO:4 SZ:210/210/1.00 VC:8866 ENC:RLE,BIT_PACKED,PLAIN_DICTIONARY
paragraphid:    INT32 SNAPPY DO:0 FPO:214 SZ:35520/35511/1.00 VC:8866 ENC:RLE,BIT_PACKED,PLAIN
paragraphnum:   INT32 SNAPPY DO:0 FPO:35734 SZ:27836/27828/1.00 VC:8866 ENC:RLE,BIT_PACKED,PLAIN_DICTIONARY
charid:         BINARY SNAPPY DO:0 FPO:63570 SZ:11172/14075/1.26 VC:8866 ENC:RLE,BIT_PACKED,PLAIN_DICTIONARY
plaintext:      BINARY SNAPPY DO:0 FPO:74742 SZ:788033/1171846/1.49 VC:8866 ENC:RLE,BIT_PACKED,PLAIN
phonetictext:   BINARY SNAPPY DO:0 FPO:862775 SZ:501506/721887/1.44 VC:8866 ENC:RLE,BIT_PACKED,PLAIN
stemtext:       BINARY SNAPPY DO:0 FPO:1364281 SZ:634052/998462/1.57 VC:8866 ENC:RLE,BIT_PACKED,PLAIN
paragraphtype:  BINARY SNAPPY DO:0 FPO:1998333 SZ:63/59/0.94 VC:8866 ENC:RLE,BIT_PACKED,PLAIN_DICTIONARY
section:        INT32 SNAPPY DO:0 FPO:1998396 SZ:210/204/0.97 VC:8866 ENC:RLE,BIT_PACKED,PLAIN_DICTIONARY
chapter:        INT32 SNAPPY DO:0 FPO:1998606 SZ:615/612/1.00 VC:8866 ENC:RLE,BIT_PACKED,PLAIN_DICTIONARY
charcount:      INT32 SNAPPY DO:0 FPO:1999221 SZ:14247/14240/1.00 VC:8866 ENC:RLE,BIT_PACKED,PLAIN_DICTIONARY
wordcount:      INT32 SNAPPY DO:0 FPO:2013468 SZ:9899/9890/1.00 VC:8866 ENC:RLE,BIT_PACKED,PLAIN_DICTIONARY
```

</details>

Проверим содержимое таблицы:

```
select * from student3_7_les4.paragraph limit 3;
```

| paragraph.workid | paragraph.paragraphid | paragraph.paragraphnum | paragraph.charid | paragraph.plaintext                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | paragraph.phonetictext                                                                                                                                                                                                                                                                                                                                                                                      | paragraph.stemtext                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | paragraph.paragraphtype | paragraph.section | paragraph.chapter | paragraph.charcount | paragraph.wordcount |
| ---------------- | --------------------- | ---------------------- | ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------- | ----------------- | ----------------- | ------------------- | ------------------- |
| 12night          | 630863                | 3                      | xxx              | [Enter DUKE ORSINO, CURIO, and other Lords; Musicians attending]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | ENTR TK ORSN KR ANT O0R LRTS MSXNS ATNTNK                                                                                                                                                                                                                                                                                                                                                                   | enter duke orsino curio and other lord musician attend                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | b                       | 1                 | 1                 | 65                  | 9                   |
| 12night          | 630864                | 4                      | ORSINO           | If music be the food of love, play on; [p]Give me excess of it, that, surfeiting, [p]The appetite may sicken, and so die. [p]That strain again! it had a dying fall: [p]O, it came o'er my ear like the sweet sound, [p]That breathes upon a bank of violets, [p]Stealing and giving odour! Enough; no more: [p]'Tis not so sweet now as it was before. [p]O spirit of love! how quick and fresh art thou, [p]That, notwithstanding thy capacity [p]Receiveth as the sea, nought enters there, [p]Of what validity and pitch soe'er, [p]But falls into abatement and low price, [p]Even in a minute: so full of shapes is fancy [p]That it alone is high fantastical. | IF MSK B 0 FT OF LF PL ON JF M EKSSS OF IT 0T SRFTNK 0 APTT M SKN ANT S T 0T STRN AKN IT HT A TYNK FL O IT KM OR M ER LK 0 SWT SNT 0T BR0S UPN A BNK OF FLTS STLNK ANT JFNK OTR ENF N MR TS NT S SWT N AS IT WS BFR O SPRT OF LF H KK ANT FRX ART 0 0T NTW0STNTNK 0 KPST RSF0 AS 0 S NFT ENTRS 0R OF HT FLTT ANT PTX SR BT FLS INT ABTMNT ANT L PRS EFN IN A MNT S FL OF XPS IS FNS 0T IT ALN IS HF FNTSTKL | if music be the food of love plai on give me excess of it that surfeit the appetit mai sicken and so die that strain again it had a dy fall o it came oer my ear like the sweet sound that breath upon a bank of violet steal and give odour enough no more ti not so sweet now a it wa befor o spirit of love how quick and fresh art thou that notwithstand thy capac receiveth a the sea nought enter there of what valid and pitch soeer but fall into abat and low price even in a minut so full of shape i fanci that it alon i high fantast | b                       | 1                 | 1                 | 646                 | 114                 |
| 12night          | 630865                | 19                     | CURIO            | Will you go hunt, my lord?                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | WL Y K HNT M LRT                                                                                                                                                                                                                                                                                                                                                                                            | will you go hunt my lord                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | b                       | 1                 | 1                 | 27                  | 6                   |

Импортируем таблицу `sales_large` в формате ORC, так как у этого формата наилучшее сжатие.

`sales_large`

```
region,text
country,text
itemtype,text
saleschannel,text
orderpriority,text
orderdate,text
orderid,integer
shipdate,text
unitssold,numeric
unitprice,numeric
unitcost,numeric
totalrevenue,numeric
totalcost,numeric
totalprofit,numeric
```

**4. Найдите папки на файловой системе куда были сохранены данные. Посмотрите их размер.**

**5. Сделайте несколько произвольных запросов к этим таблицам.**

**6. [Продвинутое задание] Сделать тоже самое с любой другой таблицей в любой другой БД вне кластера. Это задание автматически покрывает предыдущие пять пунктов -- если сделаете, то пункты 1-5 не обязательны :)**

Пример запуска SQOOP
Импорт:
sqoop import --connect jdbc:postgresql://node3.novalocal/pg_db --username exporter -P --table character --hive-import --hive-database default --hive-table character
Посмотреть в схему:
sqoop import --connect jdbc:postgresql://node3.novalocal/pg_db --username exporter -P --table character --hive-import --hive-database default --hive-table character
