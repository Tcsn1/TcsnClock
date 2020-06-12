# TcsnClock

#### 介绍
一个用来闹钟、事件备忘、提醒生日的程序。

#### 快速入门

###### 1. 点击exe运行

打开`/bin`目录，点击`TcsnClock.exe`，会跳出一个黑漆漆的窗口。

如果是第一次使用，会在当前目录下生成一个`/data`目录，里面有重要的配置文件：`config.xml`。

###### 2. python运行

```shell
python /tcsnclock/main.py
```

#### 如何设置？

##### 1. 通过配置xml文件来设置

> 配置文件支持热加载、热刷新！！

打开`/bin/config.xml`

相信聪明的您一定看得懂里面的注释和配置信息。

###### 设置闹钟

在`<alarmclocks>`标签中有很多`<alarmclock>`标签。

```xml
<alarmclocks>
    <alarmclock time="8:30" week="[1,2,3,4,5]">上班</alarmclock>
    <alarmclock time="23:00">睡觉</alarmclock>
</alarmclocks>
```

`<alarmclock>`标签有以下属性：

* time属性：闹钟时间。

* week属性：设置星期。例如[1,3,5]就代表周一、周三、周五闹钟才会响起。如果不设置，默认每天都会响起。

* 标签中间的文本则是描述信息，可以自己随便写。

###### 设置事件提醒

在`<reminders>`标签中有很多`<reminder>`标签。

```xml
<reminders>
    <reminder time="2019.11.14 19:19:19">1个小时后看电影</reminder>
    <reminder time="1977.7.7 7:7:7">七夕节给女朋友买礼物</reminder>
</reminders>
```

`<reminder>`标签有以下属性：

* time属性：触发事件提醒的日期和时间。

* 中间的文本是文本描述。

###### 设置生日提醒

在`<birthdays>`标签中有很多`<birthday>`标签。

```xml
<birthdays remindTime="12:00:00" preRemind="2">
    <birthday date="11.11">小黑的生日</birthday>
    <birthday date="2000.10.10">小花的生日</birthday>
</birthdays>
```

`<birthdays>`标签有以下属性：

* preRemind属性：设置为2后，将会在生日2天前额外提醒一次。
* remindTime属性：生日将会在一天中的这个时刻进行提醒。

`<birthday>`标签有以下属性：

* date属性：生日的日期
* 中间的文本是文本描述。