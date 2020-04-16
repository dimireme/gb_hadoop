## Урок 3. SQL движки PIG, HIVE, Impala.

**1. Скачать любой датасет из списка ниже.**

https://www.kaggle.com/shuyangli94/food-com-recipes-and-user-interactions
https://www.kaggle.com/datasnaek/youtube-new
https://www.kaggle.com/akhilv11/border-crossing-entry-data
https://www.kaggle.com/tristan581/17k-apple-app-store-strategy-games
https://www.kaggle.com/gustavomodelli/forest-fires-in-brazil

Выберем датасет `border-crossing-entry-data`, который содержит данные о въезжающих в США транспортных средствах на границах с Мексикой и Канадой за период 01.01.1996-01.03.2019. В датасете 8 столбцов (`Port Name`, `State`, `Port Code`, `Border`, `Date`, `Measure`, `Value`, `Location`) и 347 тыс. наблюдений.

**2. Загрузить этот датасет в HDFS в свою домашнюю папку.**

Загрузим датасет используя интерфейс HUE. Проверим наличие файла.

```
[student3_7@manager ~]$ hdfs dfs -ls /user/student3_7/
Found 4 items
drwx------   - student3_7 student3_7          0 2020-03-31 21:00 /user/student3_7/.Trash
drwx------   - student3_7 student3_7          0 2020-03-30 21:58 /user/student3_7/.staging
-rw-r--r--   3 student3_7 student3_7   37054236 2020-04-15 20:14 /user/student3_7/Border_Crossing_Entry_Data.csv
drwxr-xr-x   - student3_7 student3_7          0 2020-03-30 16:00 /user/student3_7/QuasiMonteCarlo_1585584041275_1299144201
```

```
[student3_7@manager ~]$ hdfs dfs -cat /user/student3_7/Border_Crossing_Entry_Data.csv | less
```

Файл `Border_Crossing_Entry_Data.csv` успешно загружен. Таблицу будем создавать с укказанием директории файла, поэтому нужно чтобы в папке с датасетом не было других файлов:

```
[student3_7@manager ~]$ hdfs dfs -mkdir /user/student3_7/datasets
[student3_7@manager ~]$ hdfs dfs -mv /user/student3_7/Border_Crossing_Entry_Data.csv /user/student3_7/datasets/border_crossing.csv
```

Данные теперь хранятся в папке `/user/student3_7/datasets/`.

**3. Создать собственную базу данных в HIVE. Жлательно чтобы имя базы содержало номер вашего пользователя.**

```
create database student3_7_les3;
```

**4. Создать EXTERNAL таблицы внутри базы данных с использованием всех загруженных файлов. Один файл – одна таблица.**

```
create external table student3_7_les3.border_crossing
(
    port_name string,
    state string,
    port_code int,
    border string,
    `date` date,
    measure string,
    value int,
    `location` string
)
ROW FORMAT SERDE
    'org.apache.hadoop.hive.serde2.OpenCSVSerde'
LOCATION
    '/user/student3_7/datasets/'
TBLPROPERTIES
(
  'serialization.null.format' = '',
  'skip.header.line.count' = '1'
);
```

Посмотрим как была создана таблица:

```
show create table student3_7_les3.border_crossing;
```

Проверим, есть ли даные в таблице:

```
select * from student3_7_les3.border_crossing;
```

Почему-то все столбцы таблицы имеют тип `string`.

**5. Сделать любой отчет по загруженным данным используя груповые и агрегатные функции.**

```
select count(*), measure
from student3_7_les3.border_crossing
group by measure;
```

**6. Сделать любой отчет по загруженным данным используя JOIN.**

**7. [Продвинутый вариант] Сделать все вышеперечисленное с использованием JSON SerDe. Подсказка: см в сторону команды «ADD JAR».**
