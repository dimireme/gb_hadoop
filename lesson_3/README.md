## Урок 3. SQL движки PIG, HIVE, Impala.

**1. Скачать любой датасет из списка ниже.**

https://www.kaggle.com/shuyangli94/food-com-recipes-and-user-interactions
https://www.kaggle.com/datasnaek/youtube-new
https://www.kaggle.com/akhilv11/border-crossing-entry-data
https://www.kaggle.com/tristan581/17k-apple-app-store-strategy-games
https://www.kaggle.com/gustavomodelli/forest-fires-in-brazil

Выберем датасет `border-crossing-entry-data`, который содержит данные о въезжающих в США транспортных средствах на границах с Мексикой и Канадой за период 01.01.1996-01.03.2019. В датасете 8 столбцов (`Port Name`, `State`, `Port Code`, `Border`, `Date`, `Measure`, `Value`, `Location`) и 347 тыс. наблюдений.

**2. Загрузить этот датасет в HDFS в свою домашнюю папку.**

Нормализуем датасет, выделив тип измерения `measure` и штат `state` в отдельные таблицы. В исходной таблице заменим значения этих колонок на получившиеся `id`. Это нужно чтобы было что джойнить в 6-м задании.

<details>
<summary>Преобразования таблиц на локальной машине в MySQL и выгрузка результата в csv.</summary>

```
drop table if exists state;
create table state (
	id INT auto_increment primary key,
	state VARCHAR(255)
) as select distinct state from border_crossing bc;
select * from state;

select * from border_crossing bc;

update border_crossing bc
inner join state s
on s.state = bc.state
set bc.state = s.id;

drop table if exists measure;
create table measure (
	id INT auto_increment primary key,
	measure VARCHAR(255)
) as select distinct measure from border_crossing bc;
select * from measure;

update border_crossing bc
inner join measure m
on m.measure = bc.measure
set bc.measure = m.id;
```

</details>

Загрузим данные в HDFS используя интерфейс HUE. Данные будем хранить в папке `/user/student3_7/datasets/`, каждый файл в одноимённой папке. Проверим наличие файлов.

```
[student3_7@manager ~]$ hdfs dfs -ls -R /user/student3_7/datasets/
drwxr-xr-x   - student3_7 student3_7          0 2020-04-16 12:18 /user/student3_7/datasets/border_crossing
-rw-r--r--   3 student3_7 student3_7   30733097 2020-04-16 12:07 /user/student3_7/datasets/border_crossing/border_crossing.csv
drwxr-xr-x   - student3_7 student3_7          0 2020-04-16 12:18 /user/student3_7/datasets/measure
-rw-r--r--   3 student3_7 student3_7        240 2020-04-16 12:06 /user/student3_7/datasets/measure/measure.csv
drwxr-xr-x   - student3_7 student3_7          0 2020-04-16 12:18 /user/student3_7/datasets/state
-rw-r--r--   3 student3_7 student3_7        177 2020-04-16 12:06 /user/student3_7/datasets/state/state.csv
```

```
[student3_7@manager ~]$ hdfs dfs -cat /user/student3_7/datasets/border_crossing/border_crossing.csv | less
```

Файлы успешно загружены.

**3. Создать собственную базу данных в HIVE. Жлательно чтобы имя базы содержало номер вашего пользователя.**

```
create database student3_7_les3;
```

**4. Создать EXTERNAL таблицы внутри базы данных с использованием всех загруженных файлов. Один файл – одна таблица.**

```
drop table student3_7_les3.border_crossing;
create external table student3_7_les3.border_crossing
(
    port_name string,
    state int,
    port_code int,
    border string,
    `date` date,
    measure int,
    value int,
    `location` string
)
ROW FORMAT SERDE
    'org.apache.hadoop.hive.serde2.OpenCSVSerde'
LOCATION
    '/user/student3_7/datasets/border_crossing'
TBLPROPERTIES (
    'serialization.null.format' = '',
    'skip.header.line.count' = '1')
;
select * from student3_7_les3.border_crossing;

drop table student3_7_les3.state;
create external table student3_7_les3.state
(
    id int,
    state string
)
ROW FORMAT SERDE
    'org.apache.hadoop.hive.serde2.OpenCSVSerde'
LOCATION
    '/user/student3_7/datasets/state'
TBLPROPERTIES (
    'serialization.null.format' = '',
    'skip.header.line.count' = '1')
;
select * from state;

drop table student3_7_les3.measure;
create external table student3_7_les3.measure
(
    id int,
    measure string
)
ROW FORMAT SERDE
    'org.apache.hadoop.hive.serde2.OpenCSVSerde'
LOCATION
    '/user/student3_7/datasets/measure'
TBLPROPERTIES (
    'serialization.null.format' = '',
    'skip.header.line.count' = '1')
;
select * from measure;
```

Посмотрим как была создана таблица `border_crossing`:

```
show create table student3_7_les3.border_crossing;
```

Почему-то все столбцы созданных таблиц имеют тип `string`.

**5. Сделать любой отчет по загруженным данным используя груповые и агрегатные функции.**

```
select count(*), measure, sum(value)
from student3_7_les3.border_crossing
group by measure;
```

<details>
  <summary>Лог выполнения в HUE</summary>

```
INFO  : Compiling command(queryId=hive_20200416171212_c3c08d24-31c7-43b0-a2f1-2e4331597ff5): select count(*), measure, sum(value)
from student3_7_les3.border_crossing
group by measure
INFO  : Semantic Analysis Completed
INFO  : Returning Hive schema: Schema(fieldSchemas:[FieldSchema(name:_c0, type:bigint, comment:null), FieldSchema(name:measure, type:string, comment:null), FieldSchema(name:_c2, type:double, comment:null)], properties:null)
INFO  : Completed compiling command(queryId=hive_20200416171212_c3c08d24-31c7-43b0-a2f1-2e4331597ff5); Time taken: 0.34 seconds
INFO  : Executing command(queryId=hive_20200416171212_c3c08d24-31c7-43b0-a2f1-2e4331597ff5): select count(*), measure, sum(value)
from student3_7_les3.border_crossing
group by measure
INFO  : Query ID = hive_20200416171212_c3c08d24-31c7-43b0-a2f1-2e4331597ff5
INFO  : Total jobs = 1
INFO  : Launching Job 1 out of 1
INFO  : Starting task [Stage-1:MAPRED] in serial mode
INFO  : Number of reduce tasks not specified. Estimated from input data size: 1
INFO  : In order to change the average load for a reducer (in bytes):
INFO  :   set hive.exec.reducers.bytes.per.reducer=<number>
INFO  : In order to limit the maximum number of reducers:
INFO  :   set hive.exec.reducers.max=<number>
INFO  : In order to set a constant number of reducers:
INFO  :   set mapreduce.job.reduces=<number>
INFO  : number of splits:1
INFO  : Submitting tokens for job: job_1583843553969_0442
INFO  : The url to track the job: http://manager.novalocal:8088/proxy/application_1583843553969_0442/
INFO  : Starting Job = job_1583843553969_0442, Tracking URL = http://manager.novalocal:8088/proxy/application_1583843553969_0442/
INFO  : Kill Command = /opt/cloudera/parcels/CDH-5.16.2-1.cdh5.16.2.p0.8/lib/hadoop/bin/hadoop job  -kill job_1583843553969_0442
INFO  : Hadoop job information for Stage-1: number of mappers: 1; number of reducers: 1
INFO  : 2020-04-16 17:12:41,845 Stage-1 map = 0%,  reduce = 0%
INFO  : 2020-04-16 17:12:55,360 Stage-1 map = 100%,  reduce = 0%, Cumulative CPU 7.61 sec
INFO  : 2020-04-16 17:13:04,660 Stage-1 map = 100%,  reduce = 100%, Cumulative CPU 11.57 sec
INFO  : MapReduce Total cumulative CPU time: 11 seconds 570 msec
INFO  : Ended Job = job_1583843553969_0442
INFO  : MapReduce Jobs Launched:
INFO  : Stage-Stage-1: Map: 1  Reduce: 1   Cumulative CPU: 11.57 sec   HDFS Read: 30742532 HDFS Write: 244 SUCCESS
INFO  : Total MapReduce CPU Time Spent: 11 seconds 570 msec
INFO  : Completed executing command(queryId=hive_20200416171212_c3c08d24-31c7-43b0-a2f1-2e4331597ff5); Time taken: 32.121 seconds
INFO  : OK
```

</details>

Результат выгрузки:

| \_c0  | measure | \_c2       |
| ----- | ------- | ---------- |
| 29856 | 1       | 253654160  |
| 29694 | 10      | 177190288  |
| 28697 | 11      | 1044218114 |
| 27623 | 12      | 6197450    |
| 27657 | 2       | 38288393   |
| 27708 | 3       | 903864     |
| 30196 | 4       | 5457391275 |
| 28820 | 5       | 142330871  |
| 29757 | 6       | 64046035   |
| 27684 | 7       | 21139444   |
| 30219 | 8       | 2559691192 |
| 28822 | 9       | 8543756    |

**6. Сделать любой отчет по загруженным данным используя JOIN.**

```
select m.measure, bc.mes_count, bc.val_sum
from (
	select count(*) as `mes_count`, measure, sum(value) as `val_sum`
	from student3_7_les3.border_crossing bc
	group by measure
) bc
left join student3_7_les3.measure m
on bc.measure = m.id;
```

<details>
  <summary>Лог выполнения в HUE</summary>

```
INFO  : Compiling command(queryId=hive_20200416172121_ff6f2f65-b874-4408-ae04-42ca3dff98d7): select m.measure, bc.mes_count, bc.val_sum
from (
	select count(*) as `mes_count`, measure, sum(value) as `val_sum`
	from student3_7_les3.border_crossing bc
	group by measure
) bc
left join student3_7_les3.measure m
on bc.measure = m.id
INFO  : Semantic Analysis Completed
INFO  : Returning Hive schema: Schema(fieldSchemas:[FieldSchema(name:m.measure, type:string, comment:null), FieldSchema(name:bc.mes_count, type:bigint, comment:null), FieldSchema(name:bc.val_sum, type:double, comment:null)], properties:null)
INFO  : Completed compiling command(queryId=hive_20200416172121_ff6f2f65-b874-4408-ae04-42ca3dff98d7); Time taken: 1.357 seconds
INFO  : Executing command(queryId=hive_20200416172121_ff6f2f65-b874-4408-ae04-42ca3dff98d7): select m.measure, bc.mes_count, bc.val_sum
from (
	select count(*) as `mes_count`, measure, sum(value) as `val_sum`
	from student3_7_les3.border_crossing bc
	group by measure
) bc
left join student3_7_les3.measure m
on bc.measure = m.id
INFO  : Query ID = hive_20200416172121_ff6f2f65-b874-4408-ae04-42ca3dff98d7
INFO  : Total jobs = 2
INFO  : Launching Job 1 out of 2
INFO  : Starting task [Stage-1:MAPRED] in serial mode
INFO  : Number of reduce tasks not specified. Estimated from input data size: 1
INFO  : In order to change the average load for a reducer (in bytes):
INFO  :   set hive.exec.reducers.bytes.per.reducer=<number>
INFO  : In order to limit the maximum number of reducers:
INFO  :   set hive.exec.reducers.max=<number>
INFO  : In order to set a constant number of reducers:
INFO  :   set mapreduce.job.reduces=<number>
INFO  : number of splits:1
INFO  : Submitting tokens for job: job_1583843553969_0443
INFO  : The url to track the job: http://manager.novalocal:8088/proxy/application_1583843553969_0443/
INFO  : Starting Job = job_1583843553969_0443, Tracking URL = http://manager.novalocal:8088/proxy/application_1583843553969_0443/
INFO  : Kill Command = /opt/cloudera/parcels/CDH-5.16.2-1.cdh5.16.2.p0.8/lib/hadoop/bin/hadoop job  -kill job_1583843553969_0443
INFO  : Hadoop job information for Stage-1: number of mappers: 1; number of reducers: 1
INFO  : 2020-04-16 17:21:50,505 Stage-1 map = 0%,  reduce = 0%
INFO  : 2020-04-16 17:21:59,364 Stage-1 map = 100%,  reduce = 0%, Cumulative CPU 6.34 sec
INFO  : 2020-04-16 17:22:06,695 Stage-1 map = 100%,  reduce = 100%, Cumulative CPU 8.82 sec
INFO  : MapReduce Total cumulative CPU time: 8 seconds 820 msec
INFO  : Ended Job = job_1583843553969_0443
INFO  : Starting task [Stage-5:MAPREDLOCAL] in serial mode
20/04/16 17:22:17 WARN conf.HiveConf: HiveConf of name hive.entity.capture.input.URI does not exist
Execution log at: /tmp/hive/hive_20200416172121_ff6f2f65-b874-4408-ae04-42ca3dff98d7.log
INFO  : Execution completed successfully
INFO  : MapredLocal task succeeded
INFO  : Launching Job 2 out of 2
INFO  : Starting task [Stage-4:MAPRED] in serial mode
INFO  : Number of reduce tasks is set to 0 since there's no reduce operator
INFO  : number of splits:1
INFO  : Submitting tokens for job: job_1583843553969_0444
INFO  : The url to track the job: http://manager.novalocal:8088/proxy/application_1583843553969_0444/
INFO  : Starting Job = job_1583843553969_0444, Tracking URL = http://manager.novalocal:8088/proxy/application_1583843553969_0444/
INFO  : Kill Command = /opt/cloudera/parcels/CDH-5.16.2-1.cdh5.16.2.p0.8/lib/hadoop/bin/hadoop job  -kill job_1583843553969_0444
INFO  : Hadoop job information for Stage-4: number of mappers: 1; number of reducers: 0
INFO  : 2020-04-16 17:22:28,497 Stage-4 map = 0%,  reduce = 0%
INFO  : 2020-04-16 17:22:34,734 Stage-4 map = 100%,  reduce = 0%, Cumulative CPU 3.04 sec
INFO  : MapReduce Total cumulative CPU time: 3 seconds 40 msec
INFO  : Ended Job = job_1583843553969_0444
INFO  : MapReduce Jobs Launched:
INFO  : Stage-Stage-1: Map: 1  Reduce: 1   Cumulative CPU: 8.82 sec   HDFS Read: 30741582 HDFS Write: 459 SUCCESS
INFO  : Stage-Stage-4: Map: 1   Cumulative CPU: 3.04 sec   HDFS Read: 6435 HDFS Write: 415 SUCCESS
INFO  : Total MapReduce CPU Time Spent: 11 seconds 860 msec
INFO  : Completed executing command(queryId=hive_20200416172121_ff6f2f65-b874-4408-ae04-42ca3dff98d7); Time taken: 56.715 seconds
INFO  : OK
```

</details>

Запрос выполнился за 3 стейджа, а не за 1, как в случае с простой агрегацией.

Результат выгрузки:

| m.measure                   | bc.mes_count | bc.val_sum |
| --------------------------- | ------------ | ---------- |
| Trucks                      | 29856        | 253654160  |
| Truck Containers Full       | 29694        | 177190288  |
| Pedestrians                 | 28697        | 1044218114 |
| Train Passengers            | 27623        | 6197450    |
| Rail Containers Full        | 27657        | 38288393   |
| Trains                      | 27708        | 903864     |
| Personal Vehicle Passengers | 30196        | 5457391275 |
| Bus Passengers              | 28820        | 142330871  |
| Truck Containers Empty      | 29757        | 64046035   |
| Rail Containers Empty       | 27684        | 21139444   |
| Personal Vehicles           | 30219        | 2559691192 |
| Buses                       | 28822        | 8543756    |

**7. [Продвинутый вариант] Сделать все вышеперечисленное с использованием JSON SerDe. Подсказка: см в сторону команды «ADD JAR».**

Не сделано
