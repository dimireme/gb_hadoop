## Урок 2.YARN. Парадигма Map Reduce.

**0. [Исследовательское задание] Сколько узлов можно потерять в кластере из 10 узлов без потери данных? Из 100 узлов?**

Не сделано

**1-5. Опробовать запуски map-reduce задач для кластера используя hadoop-mapreduce-examples.jar. Выполнить три любых задачи включенных в этот JAR. Найти свои задачи в интерфейсе Cloudera Manager. Опробовать навигацию по интерфейсу YARN. Сделать документ со скриншотами того, что вы видели.**

Найдём место расположения файла jar-файла с тестовыми примерами.

```
[student3_7@manager ~]$ find /opt -name "hadoop-mapreduce-examples.jar"
/opt/cloudera/parcels/CDH-5.16.2-1.cdh5.16.2.p0.8/lib/hadoop-mapreduce/hadoop-mapreduce-examples.jar
[student3_7@manager ~]$ export YARN_EXAMPLES=/opt/cloudera/parcels/CDH-5.16.2-1.cdh5.16.2.p0.8/lib/hadoop-mapreduce
```

Запустим первый пример для расчёта числа Пи.

```
[student3_7@manager ~]$ yarn jar $YARN_EXAMPLES/hadoop-mapreduce-examples.jar pi 16 1000000
```

<details>
  <summary>Результат вывода в консоль</summary>

```
Number of Maps  = 16
Samples per Map = 1000000
Wrote input for Map #0
Wrote input for Map #1
Wrote input for Map #2
Wrote input for Map #3
Wrote input for Map #4
Wrote input for Map #5
Wrote input for Map #6
Wrote input for Map #7
Wrote input for Map #8
Wrote input for Map #9
Wrote input for Map #10
Wrote input for Map #11
Wrote input for Map #12
Wrote input for Map #13
Wrote input for Map #14
Wrote input for Map #15
Starting Job
20/03/30 09:52:54 INFO client.RMProxy: Connecting to ResourceManager at manager.novalocal/89.208.221.132:8032
20/03/30 09:52:54 INFO input.FileInputFormat: Total input paths to process : 16
20/03/30 09:52:54 INFO mapreduce.JobSubmitter: number of splits:16
20/03/30 09:52:55 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1583843553969_0184
20/03/30 09:52:55 INFO impl.YarnClientImpl: Submitted application application_1583843553969_0184
20/03/30 09:52:55 INFO mapreduce.Job: The url to track the job: http://manager.novalocal:8088/proxy/application_1583843553969_0184/
20/03/30 09:52:55 INFO mapreduce.Job: Running job: job_1583843553969_0184
20/03/30 09:53:02 INFO mapreduce.Job: Job job_1583843553969_0184 running in uber mode : false
20/03/30 09:53:02 INFO mapreduce.Job:  map 0% reduce 0%
20/03/30 09:53:07 INFO mapreduce.Job:  map 13% reduce 0%
20/03/30 09:53:10 INFO mapreduce.Job:  map 19% reduce 0%
20/03/30 09:53:11 INFO mapreduce.Job:  map 25% reduce 0%
20/03/30 09:53:14 INFO mapreduce.Job:  map 31% reduce 0%
20/03/30 09:53:15 INFO mapreduce.Job:  map 38% reduce 0%
20/03/30 09:53:18 INFO mapreduce.Job:  map 44% reduce 0%
20/03/30 09:53:19 INFO mapreduce.Job:  map 50% reduce 0%
20/03/30 09:53:22 INFO mapreduce.Job:  map 56% reduce 0%
20/03/30 09:53:23 INFO mapreduce.Job:  map 63% reduce 0%
20/03/30 09:53:26 INFO mapreduce.Job:  map 69% reduce 0%
20/03/30 09:53:27 INFO mapreduce.Job:  map 75% reduce 0%
20/03/30 09:53:30 INFO mapreduce.Job:  map 81% reduce 0%
20/03/30 09:53:31 INFO mapreduce.Job:  map 88% reduce 0%
20/03/30 09:53:35 INFO mapreduce.Job:  map 94% reduce 0%
20/03/30 09:53:39 INFO mapreduce.Job:  map 100% reduce 0%
20/03/30 09:53:41 INFO mapreduce.Job:  map 100% reduce 100%
20/03/30 09:53:42 INFO mapreduce.Job: Job job_1583843553969_0184 completed successfully
20/03/30 09:53:42 INFO mapreduce.Job: Counters: 49
        File System Counters
                FILE: Number of bytes read=174
                FILE: Number of bytes written=2547624
                FILE: Number of read operations=0
                FILE: Number of large read operations=0
                FILE: Number of write operations=0
                HDFS: Number of bytes read=4454
                HDFS: Number of bytes written=215
                HDFS: Number of read operations=67
                HDFS: Number of large read operations=0
                HDFS: Number of write operations=3
        Job Counters
                Launched map tasks=16
                Launched reduce tasks=1
                Data-local map tasks=16
                Total time spent by all maps in occupied slots (ms)=44140
                Total time spent by all reduces in occupied slots (ms)=7720
                Total time spent by all map tasks (ms)=44140
                Total time spent by all reduce tasks (ms)=7720
                Total vcore-milliseconds taken by all map tasks=44140
                Total vcore-milliseconds taken by all reduce tasks=7720
                Total megabyte-milliseconds taken by all map tasks=45199360
                Total megabyte-milliseconds taken by all reduce tasks=7905280
        Map-Reduce Framework
                Map input records=16
                Map output records=32
                Map output bytes=288
                Map output materialized bytes=576
                Input split bytes=2566
                Combine input records=0
                Combine output records=0
                Reduce input groups=2
                Reduce shuffle bytes=576
                Reduce input records=32
                Reduce output records=0
                Spilled Records=64
                Shuffled Maps =16
                Failed Shuffles=0
                Merged Map outputs=16
                GC time elapsed (ms)=1016
                CPU time spent (ms)=14040
                Physical memory (bytes) snapshot=7639375872
                Virtual memory (bytes) snapshot=47492177920
                Total committed heap usage (bytes)=7527727104
        Shuffle Errors
                BAD_ID=0
                CONNECTION=0
                IO_ERROR=0
                WRONG_LENGTH=0
                WRONG_MAP=0
                WRONG_REDUCE=0
        File Input Format Counters
                Bytes Read=1888
        File Output Format Counters
                Bytes Written=97
Job Finished in 48.178 seconds
Estimated value of Pi is 3.14159125000000000000
```

</details>

Создалось приложение `application_1583843553969_0184`. В интерфейсе Cloudera Manager наблюдаем выполнение задачи:

<details>
  <summary>Скриншоты интерфейса Cloudera Manager</summary>

![png](images/yarn_example_pi_1.png)

![png](images/yarn_example_pi_2.png)

</details>

Второй пример с подсчётом слов внутри файла

```
[student3_7@manager ~]$ yarn jar $YARN_EXAMPLES/hadoop-mapreduce-examples.jar wordcount /acldir/etc/nfsmount.conf /tmp/output2
```

<details>
  <summary>Результат вывода в консоль</summary>

```
20/03/30 16:37:23 INFO client.RMProxy: Connecting to ResourceManager at manager.novalocal/89.208.221.132:8032
20/03/30 16:37:24 INFO input.FileInputFormat: Total input paths to process : 1
20/03/30 16:37:24 INFO mapreduce.JobSubmitter: number of splits:1
20/03/30 16:37:25 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1583843553969_0205
20/03/30 16:37:25 INFO impl.YarnClientImpl: Submitted application application_1583843553969_0205
20/03/30 16:37:25 INFO mapreduce.Job: The url to track the job: http://manager.novalocal:8088/proxy/application_1583843553969_0205/
20/03/30 16:37:25 INFO mapreduce.Job: Running job: job_1583843553969_0205
20/03/30 16:37:30 INFO mapreduce.Job: Job job_1583843553969_0205 running in uber mode : false
20/03/30 16:37:30 INFO mapreduce.Job:  map 0% reduce 0%
20/03/30 16:37:37 INFO mapreduce.Job:  map 100% reduce 0%
20/03/30 16:37:45 INFO mapreduce.Job:  map 100% reduce 33%
20/03/30 16:37:49 INFO mapreduce.Job:  map 100% reduce 50%
20/03/30 16:37:52 INFO mapreduce.Job:  map 100% reduce 67%
20/03/30 16:37:53 INFO mapreduce.Job:  map 100% reduce 83%
20/03/30 16:37:57 INFO mapreduce.Job:  map 100% reduce 100%
20/03/30 16:37:58 INFO mapreduce.Job: Job job_1583843553969_0205 completed successfully
20/03/30 16:37:58 INFO mapreduce.Job: Counters: 49
      File System Counters
              FILE: Number of bytes read=2854
              FILE: Number of bytes written=1051785
              FILE: Number of read operations=0
              FILE: Number of large read operations=0
              FILE: Number of write operations=0
              HDFS: Number of bytes read=3509
              HDFS: Number of bytes written=2277
              HDFS: Number of read operations=21
              HDFS: Number of large read operations=0
              HDFS: Number of write operations=12
      Job Counters
              Launched map tasks=1
              Launched reduce tasks=6
              Data-local map tasks=1
              Total time spent by all maps in occupied slots (ms)=4740
              Total time spent by all reduces in occupied slots (ms)=24974
              Total time spent by all map tasks (ms)=4740
              Total time spent by all reduce tasks (ms)=24974
              Total vcore-milliseconds taken by all map tasks=4740
              Total vcore-milliseconds taken by all reduce tasks=24974
              Total megabyte-milliseconds taken by all map tasks=4853760
              Total megabyte-milliseconds taken by all reduce tasks=25573376
      Map-Reduce Framework
              Map input records=135
              Map output records=593
              Map output bytes=5723
              Map output materialized bytes=2830
              Input split bytes=119
              Combine input records=593
              Combine output records=227
              Reduce input groups=227
              Reduce shuffle bytes=2830
              Reduce input records=227
              Reduce output records=227
              Spilled Records=454
              Shuffled Maps =6
              Failed Shuffles=0
              Merged Map outputs=6
              GC time elapsed (ms)=444
              CPU time spent (ms)=9370
              Physical memory (bytes) snapshot=1779253248
              Virtual memory (bytes) snapshot=19632926720
              Total committed heap usage (bytes)=1572339712
      Shuffle Errors
              BAD_ID=0
              CONNECTION=0
              IO_ERROR=0
              WRONG_LENGTH=0
              WRONG_MAP=0
              WRONG_REDUCE=0
      File Input Format Counters
              Bytes Read=3390
      File Output Format Counters
              Bytes Written=2277
```

</details>

Создалось приложение `application_1583843553969_0205`.

<details>
  <summary>Скриншоты интерфейса Cloudera Manager</summary>

![png](images/yarn_example_wordcount_1.png)

![png](images/yarn_example_wordcount_2.png)

</details>

Результат можно посмотреть командой

```
[student3_7@manager ~]$ hdfs dfs -cat /tmp/output2/*
```

Из результатов видно, что в тексте чфще всего встречается символ `#` - 134 раза.

То же самое можно сделать командой

```
[student3_7@manager ~]$ hadoop jar /wordcount.java/WordCount.jar /acldir/etc/nfsmount.conf /tmp/output2
```

В конце удалим созданный файл

```
[student3_7@manager ~]$ hdfs dfs -rm -R /tmp/output2
```

Третий пример - с подсчетом средней длины слова в тексте

```
[student3_7@manager ~]$ yarn jar $YARN_EXAMPLES/hadoop-mapreduce-examples.jar wordmean /acldir/etc/nfsmount.conf /tmp/output2
```

<details>
  <summary>Результат вывода в консоль</summary>

```
20/03/30 18:37:52 INFO client.RMProxy: Connecting to ResourceManager at manager.novalocal/89.208.221.132:8032
20/03/30 18:37:52 INFO input.FileInputFormat: Total input paths to process : 1
20/03/30 18:37:53 INFO mapreduce.JobSubmitter: number of splits:1
20/03/30 18:37:53 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1583843553969_0209
20/03/30 18:37:54 INFO impl.YarnClientImpl: Submitted application application_1583843553969_0209
20/03/30 18:37:54 INFO mapreduce.Job: The url to track the job: http://manager.novalocal:8088/proxy/application_1583843553969_0209/
20/03/30 18:37:54 INFO mapreduce.Job: Running job: job_1583843553969_0209
20/03/30 18:38:01 INFO mapreduce.Job: Job job_1583843553969_0209 running in uber mode : false
20/03/30 18:38:01 INFO mapreduce.Job:  map 0% reduce 0%
20/03/30 18:38:06 INFO mapreduce.Job:  map 100% reduce 0%
20/03/30 18:38:12 INFO mapreduce.Job:  map 100% reduce 33%
20/03/30 18:38:16 INFO mapreduce.Job:  map 100% reduce 50%
20/03/30 18:38:17 INFO mapreduce.Job:  map 100% reduce 67%
20/03/30 18:38:19 INFO mapreduce.Job:  map 100% reduce 83%
20/03/30 18:38:24 INFO mapreduce.Job:  map 100% reduce 100%
20/03/30 18:38:31 INFO mapreduce.Job: Job job_1583843553969_0209 completed successfully
20/03/30 18:38:31 INFO mapreduce.Job: Counters: 49
        File System Counters
                FILE: Number of bytes read=153
                FILE: Number of bytes written=1046383
                FILE: Number of read operations=0
                FILE: Number of large read operations=0
                FILE: Number of write operations=0
                HDFS: Number of bytes read=3509
                HDFS: Number of bytes written=22
                HDFS: Number of read operations=21
                HDFS: Number of large read operations=0
                HDFS: Number of write operations=12
        Job Counters
                Launched map tasks=1
                Launched reduce tasks=6
                Data-local map tasks=1
                Total time spent by all maps in occupied slots (ms)=3650
                Total time spent by all reduces in occupied slots (ms)=23644
                Total time spent by all map tasks (ms)=3650
                Total time spent by all reduce tasks (ms)=23644
                Total vcore-milliseconds taken by all map tasks=3650
                Total vcore-milliseconds taken by all reduce tasks=23644
                Total megabyte-milliseconds taken by all map tasks=3737600
                Total megabyte-milliseconds taken by all reduce tasks=24211456
        Map-Reduce Framework
                Map input records=135
                Map output records=1186
                Map output bytes=17197
                Map output materialized bytes=129
                Input split bytes=119
                Combine input records=1186
                Combine output records=2
                Reduce input groups=2
                Reduce shuffle bytes=129
                Reduce input records=2
                Reduce output records=2
                Spilled Records=4
                Shuffled Maps =6
                Failed Shuffles=0
                Merged Map outputs=6
                GC time elapsed (ms)=782
                CPU time spent (ms)=7740
                Physical memory (bytes) snapshot=1724329984
                Virtual memory (bytes) snapshot=19623833600
                Total committed heap usage (bytes)=1602748416
        Shuffle Errors
                BAD_ID=0
                CONNECTION=0
                IO_ERROR=0
                WRONG_LENGTH=0
                WRONG_MAP=0
                WRONG_REDUCE=0
        File Input Format Counters
                Bytes Read=3390
        File Output Format Counters
                Bytes Written=22
The mean is: NaN
```

</details>

В консоли написано что средняя длина слова не определена, но в выходном файле есть следующие данные:

```
[student3_7@manager ~]$ hdfs dfs -cat /tmp/output2/*
count   593
length  2758
```

На эту задачу скрины не делал.

**6. [Факультативное, для тех кто знает JAVA] Собрать программу для MR на Java и запустить ее. Wordcount будет вполне достаточен.**

Создадим новую папку и скопируем в неё программу на java.

```
[student3_7@manager /]$ mkdir /students/student3_7
[student3_7@manager /]$ cp -R /wordcount.java /students/student3_7/
[student3_7@manager /]$ cd /students/student3_7/wordcount.java/
```

Компилируем программу.

```
[student3_7@manager wordcount.java]$ ./compile.sh
removed ‘WordCount.class’
removed ‘WordCount.jar’
Note: WordCount.java uses or overrides a deprecated API.
Note: Recompile with -Xlint:deprecation for details.
added manifest
adding: WordCount.class(in = 1814) (out= 912)(deflated 49%)
adding: WordCount$Map.class(in = 1657) (out= 692)(deflated 58%)
adding: WordCount$Reduce.class(in = 1627) (out= 686)(deflated 57%)
```

Запускаем jar-файл на исполнение.

```
[student3_7@manager wordcount.java]$ hadoop jar WordCount.jar /acldir/etc/nfsmount.conf /tmp/output2
```

Результат такой же, как и при предыдущем выполнении этой программы, только id этого приложения `application_1583843553969_0210`.

**7. [Задание на 5++] Повторить вот этот пример https://www.michael-noll.com/tutorials/writing-an-hadoop-mapreduce-program-in-python/**
