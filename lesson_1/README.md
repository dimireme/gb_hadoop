## Урок 1. Сравнение RDBMS и NoSQL. Экосистема Hadoop. Файловая система HDFS

**1. Опробовать консольные утилиты для работы с кластером**

**1.1 Создать/скопировать/удалить папку**

Создание `hdfs dfs -mkdir /student3_7`.

Копирование `hdfs dfs -cp /student3_7 /student3_7_copy`.

Удаление `hdfs dfs -rm -R /student3_7_copy`.

Без флага `-R` удаляется только файл. После каждой команды проверял результат командой `hdfs dfs -ls /`.

**1.2 Положить в HDFS любой файл**

`hdfs dfs -copyFromLocal /home/student3_7/.bashrc /student3_7/`

Первый аргумент - что копируем, второй - куда копируем. Проверяется командой `hdfs dfs -ls /student3_7`. Результат:

```
Found 1 items
-rw-r--r--   3 student3_7 supergroup        231 2020-03-18 23:55 /student3_7/.bashrc
```

**1.3 Скопировать/удалить этот файл**

`hdfs dfs -get /student3_7/.bashrc /tmp` или `hdfs dfs -copyToLocal /student3_7/.bashrc /tmp`.

Порядок аргументов такой же. Сперва откуда, потом куда. Проверяем командой `ls -la /tmp`. Сразу удалим этот файл с рабочей станции: `rm /tmp/.bashrc`.

Скопируем файл: `hdfs dfs -cp /student3_7/.bashrc /student3_7/.bashrc_copy`. Удалим дубликат: `hdfs dfs -rm /student3_7/.bashrc_copy`.

**1.4 Просмотреть размер любой папки**

Сперва узнаем сколько весит файл .bashrc на рабочей станции, чтобы убедиться в правильности команды на сервере:

```
[student3_7@manager /]$ du -h /home/student3_7/.bashrc
4,0K    /home/student3_7/.bashrc
```

На сервере: `hdfs dfs -du /student3_7/`. Результат:

```
231  693  /student3_7/.bashrc
```

То есть на сервере этот файл весит 231 байт??? Эта же цифра выводится в команде `hdfs dfs -ls /student3_7/`, но не показывается суммарный объём занимаемой памяти.

**1.5 Посмотреть как файл хранится на файловой системе (см. команду fsck)**

Команда `hdfs fsck /student3_7/`. Результат:

```
Total size:    231 B
Total dirs:    1
Total files:   1
Total symlinks:                0
Total blocks (validated):      1 (avg. block size 231 B)
Minimally replicated blocks:   1 (100.0 %)
Over-replicated blocks:        0 (0.0 %)
Under-replicated blocks:       0 (0.0 %)
Mis-replicated blocks:         0 (0.0 %)
Default replication factor:    3
Average block replication:     3.0
Corrupt blocks:                0
Missing replicas:              0 (0.0 %)
Number of data-nodes:          3
Number of racks:               1
```

**1.6 Установить нестандартный фактор репликации (см. команду setrep)**

```
[student3_7@manager /]$ hdfs dfs -setrep 2 /student3_7/
Replication 2 set: /student3_7/.bashrc
```

Сделаем копию файла ещё раз: `hdfs dfs -cp /student3_7/.bashrc /student3_7/.bashrc_copy`. Проверим содержимое папки:

```
[student3_7@manager /]$ hdfs dfs -du -h /student3_7/
231  462  /student3_7/.bashrc
231  693  /student3_7/.bashrc_copy
```

То есть нестандартный фактор репликации применился к существующим файлам. Но к новым файлам в этой папке применяется дефолтный фактор репликации.

Перед уходом удалим всё лишнее:

```
hdfs dfs -rm /student3_7/.bashrc_copy
hdfs dfs -rm /student3_7/.bashrc
```

**2. Опробовать rest-доступ для работы с кластером, используя утилиту CURL.**

Команда `curl -X GET 'http://node2.novalocal:14000/webhdfs/v1/acldir?user.name=student3_7&op=LISTSTATUS'`.

Результат:

```json
{
  "FileStatuses": {
    "FileStatus": [
      {
        "pathSuffix": "etc",
        "type": "DIRECTORY",
        "length": 0,
        "owner": "centos",
        "group": "supergroup",
        "permission": "755",
        "accessTime": 0,
        "modificationTime": 1574696487181,
        "blockSize": 0,
        "replication": 0
      }
    ]
  }
}
```

**3. [Для любителей администрирования] Опробовать NFS доступ. Предварительно связаться со мной чтобы я открыл нужные порты.**

**4. [Для любителей программирования] Достучаться до файловой системы используя python и библиотеку libhdfs3**

Возникли проблемы с установкой библиотеки `libhdfs3`, но всё-таки успел поставить и выполнить следующий код:

```
from hdfs3 import HDFileSystem
hdfs=HDFileSystem(host='manager.novalocal',port=8020)


hdfs.ls('/user/instructor')
```
