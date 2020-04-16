## Урок 4. Заливка данных в Hadoop. Форматы хранения файлов.

---Первая часть задания -- форматы данных ---

Есть большая таблица по имени

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

Её размер вот такой:

hdfs dfs -du -h -s /test_datasets/citation
97.2 G 291.5 G /test_datasets/citation

Что вам нужно сделать

1. Создать таблицы в форматах PARQUET/ORC/AVRO c компрессией и без оной. (Выберите один вариант, например ORC с компрессией)
2. Заполнить данными из большой таблицы hive_db.citation_data
3. Посмотреть на получившийся размер данных
4. Сделать выводы о эффективности хранения и компресии.

---Вторая часть задания -- SQOOP ---
Простое задание довольно :)

1. Создать отдельную БД в HIve
2. Посмотреть при помощи SQOOP содержимое БД в POsgresql
3. Импортировать в нее три любые таблицы из базы pg_db в Postgresql используя SQOOP. Для каждой таблице используйте отдельный формат хранения -- ORC/Parquet/AVRO Рекомендую захватить таблицу sales_large -- там порядка 10 миллионов записей, она будет достаточно репрезентативна для проверки компрессии.
4. Найдите папки на файловой системе куда были сохранены данные. Посмотрите их размер.
5. Сделайте несколько произвольных запросов к этим таблицам.
6. [Продвинутое задание] Сделать тоже самое с любой другой таблицей в любой другой БД вне кластера. Это задание автматически покрывает предыдущие пять пунктов -- если сделаете, то пункты 1-5 не обязательны :)

Пример запуска SQOOP
Импорт:
sqoop import --connect jdbc:postgresql://node3.novalocal/pg_db --username exporter -P --table character --hive-import --hive-database default --hive-table character
Посмотреть в схему:
sqoop import --connect jdbc:postgresql://node3.novalocal/pg_db --username exporter -P --table character --hive-import --hive-database default --hive-table character
