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

Импортируем таблицу `sales_large` в формате ORC, так как у этого формата наилучшее сжатие.

Таблицу `paragraph` импортируем в формат Parquet.

`paragraph`

```
workid,character varying
paragraphid,integer
paragraphnum,integer
charid,character varying
plaintext,text
phonetictext,text
stemtext,text
paragraphtype,character varying
section,integer
chapter,integer
charcount,integer
wordcount,integer
```

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
