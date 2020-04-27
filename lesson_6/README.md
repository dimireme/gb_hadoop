## Урок 5. Потоковая обработка данных. Flume.

**1. Создать Flume поток используя Flume сервис соотвествующего номера.**

Тип источника источник – exeс
Тип канала – memory
Тип слива – hbase

Сперва в hbase создадим таблицу `Student3_7` с одним семейством колонок `Message`.

```
[student3_7@manager ~]$ hbase shell
```

```
hbase(main):004:0> create 'Student3_7', 'Message'
0 row(s) in 3.0720 seconds

=> Hbase::Table - Student3_7
hbase(main):005:0> describe 'Student3_7'
Table Student3_7 is ENABLED
Student3_7
COLUMN FAMILIES DESCRIPTION
{NAME => 'Message', BLOOMFILTER => 'ROW', VERSIONS => '1', IN_MEMORY => 'false', KEEP_DELETED_CELLS => 'FALSE', DATA_BLOCK_ENCODING => 'NONE', TTL => 'FOREVER', COMPRESSION => 'NONE', MIN_VERSIONS => '0', BLOCKCACHE => 'true', BLOCKSIZE => '65536', REPLICATION_SCOPE => '0'}
1 row(s) in 0.0390 seconds
```

Для сервиса Flume-7 зададим конфиг:

```
# Naming the components on the current agent
LoggerAgent.sources = ExecSource
LoggerAgent.channels = MemChannel
LoggerAgent.sinks = HbaseSink

# Describing/Configuring the source
LoggerAgent.sources.ExecSource.type = exec
LoggerAgent.sources.ExecSource.command = tail -F /tmp/student3_7_hbase_source
LoggerAgent.sources.ExecSource.interceptors = TimestampInterceptor
LoggerAgent.sources.ExecSource.interceptors.TimestampInterceptor.type = timestamp

# Describing/Configuring the HDFS sink
LoggerAgent.sinks.HbaseSink.type 	= hbase
LoggerAgent.sinks.HbaseSink.table = Student3_7
LoggerAgent.sinks.HbaseSink.columnFamily = Message

# Describing/Configuring the channel
LoggerAgent.channels.MemChannel.type = memory
LoggerAgent.channels.MemChannel.capacity = 1000
LoggerAgent.channels.MemChannel.transactionCapacity = 1000

# Bind the source and sink to the channel
LoggerAgent.sources.ExecSource.channels = MemChannel
LoggerAgent.sinks.HbaseSink.channel = MemChannel
```

Агент Flume7 читает данные из файла `/tmp/student3_7_hbase_source` и записывает в таблицу `Student3_7`. Долбавим записей в файл-источник.

```
[student3_7@node2 ~]$ echo 'first message' >> /tmp/student3_7_hbase_source
[student3_7@node2 ~]$ echo 'second message' >> /tmp/student3_7_hbase_source
[student3_7@node2 ~]$ echo 'third message' >> /tmp/student3_7_hbase_source
[student3_7@node2 ~]$ echo 'third 4 message' >> /tmp/student3_7_hbase_source
[student3_7@node2 ~]$ echo 'third 5 message' >> /tmp/student3_7_hbase_source
[student3_7@node2 ~]$ cat /tmp/student3_7_hbase_source
first message
second message
third message
third 4 message
third 5 message
```

Посмотрим содержимое нашей таблицы

```
hbase(main):009:0> scan 'Student3_7'
ROW                                             COLUMN+CELL
 default0c1c21cb-f918-4775-8c6b-f680f07cc3cb    column=Message:pCol, timestamp=1587979602590, value=first message
 default0ecfee8d-b2ae-4f61-a8d0-d7cac33a793e    column=Message:pCol, timestamp=1587979876628, value=third 5 message
 default1da55f6e-4f7b-4822-b812-66c8305629df    column=Message:pCol, timestamp=1587979871850, value=third 4 message
 default9e4f8ab4-0682-4e48-a3c4-149b6c28ef50    column=Message:pCol, timestamp=1587979707660, value=second message
 defaultdf3fe310-f8a1-4cae-b572-edf5b3e13bc1    column=Message:pCol, timestamp=1587979740680, value=third message
 incRow                                         column=Message:iCol, timestamp=1587979876635, value=\x00\x00\x00\x00\x00\x00\x00\x05
6 row(s) in 0.0750 seconds
```

// TODO: добавить пример чтения из ячейки

В конце удалим нашу таблицу. Сперва её нужно задизейблить, только потом можно будет её удалить.

```
hbase(main):003:0> disable 'Student3_7'
0 row(s) in 4.5880 seconds

hbase(main):004:0> drop 'Student3_7'
0 row(s) in 2.3790 seconds

hbase(main):005:0> list
TABLE
Project_S2_3
Stud3_2
Student3_10
Users
UsersTable
carbon_hbase
exec_date
flume_cronlog
shlyapka_hbase
student2_5
student2_6_logs
syslog
12 row(s) in 0.0130 seconds

=> ["Project_S2_3", "Stud3_2", "Student3_10", "Users", "UsersTable", "carbon_hbase", "exec_date", "flume_cronlog", "shlyapka_hbase", "student2_5", "student2_6_logs", "syslog"]
```

Таблицы `Student3_7` нет в списке, она успешно удалена.
