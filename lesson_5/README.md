## Урок 5. Потоковая обработка данных. Flume.

Для части по потоковой обработке (Flume)

**1. Посмотреть что не так в конфигурации NetCat Flume agent которого я сделал. Описать и аргументировать.**

```
# Naming the components on the current agent
NetcatAgent.sources = Netcat
NetcatAgent.channels = MemChannel
NetcatAgent.sinks = LoggerSink

# insert timestamp
NetcatAgent.sources.Netcat.interceptors = ts_interceptor
NetcatAgent.sources.Netcat.interceptors.ts_interceptor.type = timestamp

# Describing/Configuring the source
NetcatAgent.sources.Netcat.type = netcat
NetcatAgent.sources.Netcat.bind = 89.208.220.216
NetcatAgent.sources.Netcat.port = 7401

# Describing/Configuring the sink
NetcatAgent.sinks.LoggerSink.type = hdfs
NetcatAgent.sinks.LoggerSink.hdfs.path= /NetCat/snap_day=%Y%m%d/
# NetcatAgent.sinks.LoggerSink.hdfs.path= /NetCat/
NetcatAgent.sinks.LoggerSink.hdfs.filePrefix=flume_data
NetcatAgent.sinks.LoggerSink.hdfs.fileType=SequenceFile
NetcatAgent.sinks.LoggerSink.hdfs.codeC=gzip

# Describing/Configuring the channel
NetcatAgent.channels.MemChannel.type = memory
NetcatAgent.channels.MemChannel.capacity = 10000
NetcatAgent.channels.MemChannel.transactionCapacity = 10

# Bind the source and sink to the channel
NetcatAgent.sources.Netcat.channels = MemChannel
NetcatAgent.sinks.LoggerSink.channel = MemChannel
```

Выглядит так, что всё работает. Но судя по логам, буфер часто переполняется:

```
process failed
org.apache.flume.ChannelException: Take list for MemoryTransaction, capacity 10 full, consider committing more frequently, increasing capacity, or increasing thread count
```

ETL-процесс формирует батч из 10 событий (каждое максимум 512 байт) и может записывать его в HDFS раз в 3 секунды. То есть пропускная способнсть процесса 1,67 КБайт в секунду. Если сообщения поступают чаще, чем 10 раз в 3 секунды, то они будут потеряны (???). При этом в лог пишется ошибка со статусом CRITICAL.

`NetcatAgent.sinks.LoggerSink.hdfs.fileType=SequenceFile` - значение по-умолчанию, указывать не обязательно.

**2. Создать любой Flume поток используя Flume сервис соотвествующего номера.**

Тип источника источник – exeс
Тип канала – file
Тип слива – hdfs

Для сервиса Flume-7 зададим конфиг:

```
# Naming the components on the current agent
LoggerAgent.sources = ExecSource
LoggerAgent.channels = FileChannel
LoggerAgent.sinks = HdfsSink

# Describing/Configuring the source
LoggerAgent.sources.ExecSource.type = exec
LoggerAgent.sources.ExecSource.command = tail -F /var/log/hadoop-httpfs/hadoop-cmf-hdfs-HTTPFS-node2.novalocal.log.out
LoggerAgent.sources.ExecSource.interceptors = TimestampInterceptor
LoggerAgent.sources.ExecSource.interceptors.TimestampInterceptor.type = timestamp

# Describing/Configuring the HDFS sink
LoggerAgent.sinks.HdfsSink.type = hdfs
LoggerAgent.sinks.HdfsSink.hdfs.path = /flume/flume-7/exec-file-hdfs-v4/%y-%m-%d/
LoggerAgent.sinks.HdfsSink.hdfs.filePrefix = events

# Describing/Configuring the channel
LoggerAgent.channels.FileChannel.type = file
LoggerAgent.channels.FileChannel.checkpointDir = /tmp/flume-7/checkpoint
LoggerAgent.channels.FileChannel.dataDirs = /tmp/flume-7/data

# Bind the source and sink to the channel
LoggerAgent.sources.ExecSource.channels = FileChannel
LoggerAgent.sinks.HdfsSink.channel = FileChannel
```

Источник читиает файл логов инстанса HttpFS сервиса HDFS. Этот инстанс запущен на том же узле что и наш Flume-7 (node2.novalocal).

Посмотрим, как создались файлы:

```
[student3_7@manager ~]$ hdfs dfs -ls -R /flume/flume-7/exec-file-hdfs-v4/
drwxr-xr-x   - flume flume          0 2020-04-19 19:21 /flume/flume-7/exec-file-hdfs-v4/20-04-19
-rw-r--r--   3 flume flume       1088 2020-04-19 19:21 /flume/flume-7/exec-file-hdfs-v4/20-04-19/events.1587324059157
```

Посмотрим содержимое файла

```
[student3_7@manager ~]$ hdfs dfs -cat /flume/flume-7/exec-file-hdfs-v4/20-04-19/events.1587324059157
SEQ!org.apache.hadoop.io.LongWritable"org.apache.hadoop.io.BytesWritable�����I
                                                                              zX�#"9�Eq���_G
2020-04-19 18:29:55,085 INFO httpfsaudit: [/user/student3_7] filter [-]q���_1
2020-04-19 18:29:55,098 INFO httpfsaudit: [/user]q���_<
2020-04-19 18:29:55,116 INFO httpfsaudit: [/user/student3_7]q���_*
2020-04-19 18:29:55,129 INFO httpfsaudit: q���_<
2020-04-19 18:29:55,138 INFO httpfsaudit: [/user/student3_7q���_
2020-04-19 18:29:55,149 WARN org.apache.hadoop.security.UserGroupInformation: PriviledgedActionException as:student3_7 (auth:PROXY) via httpfs (auth:SIMPLE) cause:java.io.FileNotFoundException: File does not exist: /user/student3_7/.Trash/Current/user/student3_7q���_*
2020-04-19 18:29:55,158 INFO httpfsaudit: q���_<
2020-04-19 18:29:55,167 INFO httpfsaudit: [/user/student3_7]q���_C
2020-04-19 18:29:55,177 INFO httpfsaudit: [/user/student3_7/.Trash]q���_<
2020-04-19 18:29:55,190 INFO httpfsaudit: [/user/student3_7]���������I
                                                                                                                                              zX�#"9�E[
```

**3. [Продвинутый вариант] Сделать то-же самое используя несколько сливов в разные места, например в HDFS и в Hive одновременно.**

Задаём два канала на два слива с одним источником. По умолчанию параметр `LoggerAgent.sources.ExecSource.selector.type == replicating`. В этом случае событие будет отправлено на все указанные каналы. При значении `multiplexing`, событие будет отправлено только в подходящие каналы. Условие выбора канала задаётся дополнительными параметрами.

```
# Naming the components on the current agent
LoggerAgent.sources = ExecSource
LoggerAgent.channels = FileChannelForHdfs FileChannelForHive
LoggerAgent.sinks = HdfsSink HiveSink

# SOURCES

# Describing/Configuring the source
LoggerAgent.sources.ExecSource.type = exec
LoggerAgent.sources.ExecSource.command = tail -F /var/log/hadoop-httpfs/hadoop-cmf-hdfs-HTTPFS-node2.novalocal.log.out
LoggerAgent.sources.ExecSource.interceptors = TimestampInterceptor
LoggerAgent.sources.ExecSource.interceptors.TimestampInterceptor.type = timestamp

# SINKS

# Describing/Configuring the HDFS sink
LoggerAgent.sinks.HdfsSink.type = hdfs
LoggerAgent.sinks.HdfsSink.hdfs.path = /flume/flume-7/exec-file-hdfs-v10/%y-%m-%d/
LoggerAgent.sinks.HdfsSink.hdfs.filePrefix = events

# Describing/Configuring the Hive sink
LoggerAgent.sinks.HiveSink.type = hive
LoggerAgent.sinks.HiveSink.hive.metastore = thrift://89.208.221.132:9083
LoggerAgent.sinks.HiveSink.hive.database = student3_7_les4
LoggerAgent.sinks.HiveSink.hive.table = flume_logger_agent
LoggerAgent.sinks.HiveSink.hive.partition = %y-%m-%d
LoggerAgent.sinks.HiveSink.serializer = DELIMITED
LoggerAgent.sinks.HiveSink.serializer.delimiter = "\t"
LoggerAgent.sinks.HiveSink.serializer.fieldnames = text

# CHANNELS

# Describing/Configuring the channel for hdfs sink
LoggerAgent.channels.FileChannelForHdfs.type = file
LoggerAgent.channels.FileChannelForHdfs.checkpointDir = /tmp/flume-7/checkpoint-hdfs
LoggerAgent.channels.FileChannelForHdfs.dataDirs = /tmp/flume-7/data-hdfs

# Describing/Configuring the channel for hive sink
LoggerAgent.channels.FileChannelForHive.type = file
LoggerAgent.channels.FileChannelForHive.checkpointDir = /tmp/flume-7/checkpoint-hive
LoggerAgent.channels.FileChannelForHive.dataDirs = /tmp/flume-7/data-hive

# BINDING

# Binding source and sinks to channels
LoggerAgent.sources.ExecSource.channels = FileChannelForHdfs FileChannelForHive
LoggerAgent.sinks.HdfsSink.channel = FileChannelForHdfs
LoggerAgent.sinks.HiveSink.channel = FileChannelForHive
```

Таблица в hive:

```
create table student3_7_les4.flume_logger_agent (
    text string
)
partitioned by (`date` string)
clustered by (text) into 5 buckets
stored as orc;
```

Данные логов будут писаться в одну строку, без разделителей.

Для успешного старта агента так же нужно было указать параметры для `Flume Service Environment`:

```
HCAT_HOME=/opt/cloudera/parcels/CDH-5.16.2-1.cdh5.16.2.p0.8/lib/hive-hcatalog
HIVE_HOME=/opt/cloudera/parcels/CDH-5.16.2-1.cdh5.16.2.p0.8/lib/hive
```

Посмотрим на результат:

```
select * from student3_7_les4.flume_logger_agent limit 8;
```

| flume_logger_agent.text                                                                                                              | flume_logger_agent.date |
| ------------------------------------------------------------------------------------------------------------------------------------ | ----------------------- |
| 2020-04-20 19:18:02,271 INFO httpfsaudit: [/user/flume/student3_10/log/20-04-20/hdfs-st3_10-.1587377562789.gz]                       | 20-04-20                |
| 2020-04-20 19:18:02,530 INFO httpfsaudit: [/user/flume/student3_10/log/20-04-20/hdfs-st3_10-.1587377562789.gz]                       | 20-04-20                |
| 2020-04-20 19:18:02,544 INFO httpfsaudit: [/user/flume/student3_10/log/20-04-20/hdfs-st3_10-.1587377562789.gz]                       | 20-04-20                |
| 2020-04-20 19:18:02,558 INFO httpfsaudit: [/user/flume/student3_10/log/20-04-20/hdfs-st3_10-.1587377562789.gz]                       | 20-04-20                |
| 2020-04-20 19:18:02,569 INFO httpfsaudit: [/user/flume/student3_10/log/20-04-20/hdfs-st3_10-.1587377562789.gz]                       | 20-04-20                |
| 2020-04-20 19:18:02,581 INFO httpfsaudit: [/user/flume/student3_10/log/20-04-20/hdfs-st3_10-.1587377562789.gz]                       | 20-04-20                |
| 2020-04-20 19:18:02,592 INFO httpfsaudit: [/user/flume/student3_10/log/20-04-20/hdfs-st3_10-.1587377562789.gz] offset [0] len [4096] | 20-04-20                |
| 2020-04-20 19:18:02,605 INFO httpfsaudit: [/user/flume/student3_10/log/20-04-20/hdfs-st3_10-.1587377562789.gz]                       | 20-04-20                |

```
[student3_7@manager ~]$ hdfs dfs -ls -R /flume/flume-7/exec-file-hdfs-v10
drwxr-xr-x   - flume flume          0 2020-04-20 22:59 /flume/flume-7/exec-file-hdfs-v10/20-04-20
-rw-r--r--   3 flume flume       1337 2020-04-20 22:59 /flume/flume-7/exec-file-hdfs-v10/20-04-20/events.1587423544595
```

```
[student3_7@manager ~]$ hdfs dfs -cat /flume/flume-7/exec-file-hdfs-v10/20-04-20/events.1587423544595
SEQ!org.apache.hadoop.io.LongWritable"org.apache.hadoop.io.BytesWritable
2020-04-20 19:18:02,271 INFO httpfsaudit: [/user/flume/student3_10/log/20-04-20/hdfs-st3_10-.1587377562789.gz]
2020-04-20 19:18:02,530 INFO httpfsaudit: [/user/flume/student3_10/log/20-04-20/hdfs-st3_10-.1587377562789.gz]
2020-04-20 19:18:02,544 INFO httpfsaudit: [/user/flume/student3_10/log/20-04-20/hdfs-st3_10-.1587377562789.gz]
2020-04-20 19:18:02,558 INFO httpfsaudit: [/user/flume/student3_10/log/20-04-20/hdfs-st3_10-.1587377562789.gz]
2020-04-20 19:18:02,569 INFO httpfsaudit: [/user/flume/student3_10/log/20-04-20/hdfs-st3_10-.1587377562789.gz]
2020-04-20 19:18:02,581 INFO httpfsaudit: [/user/flume/student3_10/log/20-04-20/hdfs-st3_10-.1587377562789.gz]
2020-04-20 19:18:02,592 INFO httpfsaudit: [/user/flume/student3_10/log/20-04-20/hdfs-st3_10-.1587377562789.gz] offset [0] len [4096]
2020-04-20 19:18:02,605 INFO httpfsaudit: [/user/flume/student3_10/log/20-04-20/hdfs-st3_10-.1587377562789.gz]
```

Тут немного почистил вывод в консоль от спец-символов. В Hive-таблице и в HDFS одинаковые данные.

**4. [Продвинутый вариант] Повторить стандартный пример с выборкой сообщений из Twitter. Перед этим связаться со мной :)**

Не сделано.
