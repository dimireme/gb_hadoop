## Урок 7. Notebooks. Hue, Jupyter, Zeppelin.

**1. На основе импортированных в Hbase данных создать любой график в Jupyter или Zeppelin.**

Создадим таблицу `Student3_7` с семейством колонок `Message`.

```
hbase(main):018:0> create 'Student3_7', 'Message'
0 row(s) in 8.5430 seconds
```

Колонку `Message:Text` заполним роизвольным текстом, используя конструкцию вида

```
put 'Student3_7', 'Message{i}', 'Message:Text', '{text}'
```

где `i` - индекс от 1 до 5, `text` - произвольный текст.

```
hbase(main):027:0> scan 'Student3_7'
```

<details>
<summary>
  результат
</summary>

```
ROW                                          COLUMN+CELL
 Message1                                    column=Message:Text, timestamp=1588447183426, value=Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod temp
                                             or incididunt ut labore et dolore magna aliqua. Lobortis scelerisque fermentum dui faucibus in ornare quam viverra orci. Vitae c
                                             ongue eu consequat ac felis donec et odio. Et leo duis ut diam. Egestas maecenas pharetra convallis posuere. Congue eu consequat
                                              ac felis donec. Id velit ut tortor pretium viverra suspendisse potenti. Sed risus pretium quam vulputate dignissim suspendisse
                                             in. Odio morbi quis commodo odio aenean sed. Vel orci porta non pulvinar neque. Tellus integer feugiat scelerisque varius morbi
                                             enim. Morbi tristique senectus et netus et. Ante metus dictum at tempor commodo ullamcorper a lacus vestibulum. Tristique sollic
                                             itudin nibh sit amet commodo nulla facilisi. Ut enim blandit volutpat maecenas volutpat blandit aliquam. Est ultricies integer q
                                             uis auctor elit sed vulputate mi sit. Ut diam quam nulla porttitor massa. Adipiscing bibendum est ultricies integer quis auctor
                                             elit. At auctor urna nunc id cursus.
 Message2                                    column=Message:Text, timestamp=1588447204975, value=Eget felis eget nunc lobortis mattis. Interdum posuere lorem ipsum dolor. Te
                                             llus integer feugiat scelerisque varius. Nisi vitae suscipit tellus mauris a diam. Metus aliquam eleifend mi in nulla posuere so
                                             llicitudin. Adipiscing diam donec adipiscing tristique risus. Cursus mattis molestie a iaculis. Semper quis lectus nulla at. Ali
                                             quam eleifend mi in nulla. Ultrices neque ornare aenean euismod elementum nisi quis. At in tellus integer feugiat scelerisque. P
                                             roin fermentum leo vel orci porta non pulvinar neque laoreet. Lectus magna fringilla urna porttitor rhoncus dolor purus non. Viv
                                             erra vitae congue eu consequat ac felis.
 Message3                                    column=Message:Text, timestamp=1588447241886, value=Tristique magna sit amet purus gravida quis. Sed euismod nisi porta lorem mo
                                             llis aliquam. Est ultricies integer quis auctor. Ornare massa eget egestas purus viverra accumsan in nisl. Vestibulum sed arcu n
                                             on odio. Libero enim sed faucibus turpis in eu. Sed tempus urna et pharetra pharetra massa massa. Lacus sed viverra tellus in ha
                                             c. Lacus luctus accumsan tortor posuere ac ut consequat semper. Sapien pellentesque habitant morbi tristique senectus. Sit amet
                                             est placerat in egestas. Ornare quam viverra orci sagittis eu volutpat. Tellus integer feugiat scelerisque varius morbi enim nun
                                             c faucibus a. Pellentesque habitant morbi tristique senectus et netus. Consequat semper viverra nam libero justo laoreet sit.
 Message4                                    column=Message:Text, timestamp=1588447267710, value=Malesuada bibendum arcu vitae elementum curabitur vitae nunc sed velit. Semp
                                             er risus in hendrerit gravida rutrum quisque non tellus. Ornare aenean euismod elementum nisi quis eleifend quam. Iaculis eu non
                                              diam phasellus vestibulum lorem. Sollicitudin tempor id eu nisl nunc mi ipsum. Morbi tempus iaculis urna id volutpat lacus laor
                                             eet. Diam maecenas ultricies mi eget mauris pharetra. Faucibus purus in massa tempor nec feugiat nisl. Leo in vitae turpis massa
                                              sed elementum tempus. Purus in massa tempor nec feugiat nisl pretium. Quis hendrerit dolor magna eget est lorem. Cras tincidunt
                                              lobortis feugiat vivamus at augue eget arcu. Nam libero justo laoreet sit amet cursus sit. Tempor orci dapibus ultrices in iacu
                                             lis nunc sed augue lacus. Elementum integer enim neque volutpat ac tincidunt vitae semper.
 Message5                                    column=Message:Text, timestamp=1588447289653, value=Et molestie ac feugiat sed lectus. Nec feugiat nisl pretium fusce id velit u
                                             t tortor pretium. Bibendum arcu vitae elementum curabitur vitae. Turpis tincidunt id aliquet risus feugiat in. Vulputate digniss
                                             im suspendisse in est ante in nibh. Nisl nisi scelerisque eu ultrices. Aliquet bibendum enim facilisis gravida neque convallis a
                                             . Scelerisque in dictum non consectetur. Mi bibendum neque egestas congue. Augue mauris augue neque gravida in fermentum et. In
                                             tellus integer feugiat scelerisque varius. Lectus proin nibh nisl condimentum id venenatis. Adipiscing elit pellentesque habitan
                                             t morbi. Ut sem nulla pharetra diam sit amet nisl suscipit adipiscing. Fermentum et sollicitudin ac orci phasellus egestas. Volu
                                             tpat blandit aliquam etiam erat velit. Et sollicitudin ac orci phasellus egestas tellus rutrum tellus pellentesque. Habitasse pl
                                             atea dictumst vestibulum rhoncus est.
5 row(s) in 0.0270 seconds
```

</details>

**2. Если есть проблемы с доступом из ноутбука в HBASE то можно использовать любой другой источник данных. Hive, Postgres -- все что найдете в материалах курса :)**

```

```
