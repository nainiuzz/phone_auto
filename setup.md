#UI自动化测试环境安装

##服务器搭建环境

windows系统

##安装步骤

###一、安装node.js

1.[官网下载地址](https://nodejs.org/en/download/)

2.双击进行安装，可以选择路径，如默认位置C盘（C:\Program Files\nodejs\），自动添加到了PATH环境变量，DOS窗口输入npm回车，看是否添加环境变量成功

3.测试：CMD中输入node -v，能看到版本号

###二、Java环境配置

1.[安装jdk](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)

2.设置系统环境变量

      a.系统变量→新建 JAVA_HOME 变量,变量值填写jdk的安装目录
    （如C:\Program Files\Java\jdk1.7.0_80)

      b.系统变量→新建 CLASSPATH 变量,变量值填写
     (.;%JAVA_HOME%\lib\dt.jar;%JAVA_HOME%\lib\tools.jar)

      c.系统变量→寻找 Path 变量→编辑
     (%JAVA_HOME%\bin;%JAVA_HOME%\jre\bin;)
     注意：原来Path的变量值末尾有没有;号，先输入;号再输入上面的代码

3.安装Android SDK（测试中用到Android SDK的一些工具）

4.设置安卓环境变量

      a.系统变量→寻找 Path 变量→编辑，变量值填写
        （%ANDROID_HOME%\tools;%ANDROID_HOME%\platform-tools）

      b.系统变量→新建 ANDROID_HOME 变量,变量值填写sdk的安装目录
           (如是：D:\Program Files\eclipse\sdk)

5.测试:CMD中输入java -version,能看到版本号

###三、安装Appium

1.[最新appium安装说明](http://www.automationtestinghub.com/download-and-install-appium-1-6/)

2.[下载appium的桌面监听](https://github.com/appium/appium-desktop/releases)

3.安装uiautomator2

       a.安装npm镜像

              cmd中执行：

             npm install -g cnpm --registry=https://registry.npm.taobao.org

      b.安装uiautomator2

            cmd中执行：

       cnpm install appium-uiautomator2-driver

4.安装appium-doctor检查appium环境设置是否成功

     cmd中执行：cnpm install -g appium-doctor

###四、安装python

1.[python下载](https://www.python.org/downloads/windows/)

2.安装：选择路径进行安装，默认为C盘

3.配置系统环境变量，找到系统环境变量Path，添加python的路径（一般会默认添加路径）
   （如是C:\Python36\Scripts\;C:\Python36\;）

4.安装检查:DOS窗口输入python回车，检查是否安装成功

###五、安装pycharm

1.[pycharm下载](https://www.jetbrains.com/pycharm/download/#section=windows)

2.打开pycharm，git导入[项目工程](http://git.internal.taqu.cn/common/ui_auto_test)

3.检查项目工程库是否安装完整

###六、安装夜神模拟器

1.[模拟器安装说明](https://www.jianshu.com/p/50eb9a88f4e2)

2.下载[夜神模拟器](https://www.yeshen.com/)

3.配置系统环境变量：在Path中添加D:\yeShen\Nox\bin

4、新增一个模拟器

5、如需要Android5以上，请打开多开模拟器，并新增，选择Android5.1.1版本模拟器。然后cmd输入netstat -ano |findstr 620查找对应端口

###七、启动环境

1.打开模拟器

2.cmd 输入nox_adb.exe connect 127.0.0.1:62001（或者nox_adb.exe connect 127.0.0.1:62025）

3.cmd 输入appium 或者 打开appium可执行程序

3.用pycharm打开项目工程，找到触发文件（\\ui_auto_test\test\test_model.py）,点击run。或者在终端下进入，输入D:\ui_auto_test\src>py.test ../test/test_model.py