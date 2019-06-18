<div align=right><img src ="logo_nav.png"/></div>
<div align='right' style="font-size:30px;font-weight:bold">Bottle Documentation</div>
<div align='right' style="font-size:21px;font-weight:bold;font-style:italic">Release 0.13-dev</div>
<br/><br/><br/><br/><br/><br/><br/>
<div align='right' style="font-size:21px;font-weight:bold">Marcel Hellkamp</div>
<div align='right' style="font-size:18px;font-weight:bold">May 16, 2019</div>
<br/><br/><br/><br/><br/><br/><br/>

----
<div align='right' style="font-size:18px">Contents</div>

----
1. User’s Guide
    - [1.1 Tutorial](#1001)
    - [1.2 Configuration (DRAFT)](#1002)
    - [1.3 Request Routing](#1003)
    - [1.4 SimpleTemplate Engine](#1004)
    - [1.5 Deployment](#1005)
    - [1.6 API Reference](#1006)
    - [1.7 List of available Plugins](#1007)

2. Knowledge Base
    - [2.1 Tutorial: Todo-List Application](#2001)
    - [2.2 Primer to Asynchronous Applications](#2002)
    - [2.3 Recipes](#2003)
    - [2.4 Frequently Asked Questions](#2004)

3. Development and Contribution
    - [3.1 Release Notes and Changelog](#3001)
    - [3.2 Contributors](#3002)
    - [3.3 Developer Notes](#3003)
    - [3.4 Plugin Development Guide](#3004)
    - [3.5 Contact](#3005)

4. [License](#4001)

[Python Module Index](#5001)

[Index](#6001)
<br/><br/><br/><br/><br/><br/><br/>
Bottle 是一个基于 [Python](http://python.org/) 的快速，简单，轻量级的 [WSGI](http://www.wsgi.org/) 微型 Web 框架。它基于单个文件模块分发，并且没有除了 Python [标准库](http://docs.python.org/library/) 以外的依赖项。

+ __路由__：支持简洁的和动态的 URLs，并映射为请求的函数调用。
+ __模板__：快速和 pythonic [内置模板引擎](link)，并支持外部 [mako](http://www.makotemplates.org/)，[jinja2](http://jinja.pocoo.org/) 和 [cheetah](http://www.cheetahtemplate.org/) 模板。
+ __实用程序__：方便地访问表单数据，文件上载，cookies，headers 和其他与 HTTP 相关的元数据。
+ __服务器__：内置 HTTP 开发服务器，支持 [paste](http://pythonpaste.org/)，[fapws3](https://github.com/william-os4y/fapws3)，[bjoern](https://github.com/jonashaag/bjoern)，[gae](https://developers.google.com/appengine/)，[cherrypy](http://www.cherrypy.org/) 或任何其他支持 [WSGI](http://www.wsgi.org/) 的 HTTP 服务器。

### __示例：bottle 的 "Hello World"__

```python
from bottle import route, run, template

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

run(host='localhost', port=8080)
```

运行此脚本或将其粘贴到 Python 控制台，然后在浏览器中输入地址 http://localhost:8080/hello/world ，就行了。

### __下载和安装__

使用命令 pip install bottle 安装最新的稳定版本，或将 [bottle.py](https://github.com/bottlepy/bottle/raw/master/bottle.py) (unstable) 下载到项目目录中。除了 Python 标准库之外，没有其他 [硬依赖项@1](#0001) 。Bottle 支持 __Python 2.7 和 Python 3__。

从版本0.13开始：此版本删除了对 Python 2.5和2.6的支持。

<div id="0001">@1: 使用模板或服务器适配器类需要相应的模板或服务器模块。</div>


<div align='right' style="font-size:24px">第一章</div>

----
<div align='right' style="font-size:18px">用户指南</div>

----

如果您想学习如何使用 Bottle 框架进行 Web 开发，请从这里开始。如果您有任何疑问在这里没有回答，请访问一下 [邮件列表](mailto:bottlepy@googlegroups.com) 。

<div id="1001" style="font-size:21px;font-weight:bold">1.1 教程</div>

本教程将向您介绍 Bottle Web 框架的概念和功能，并介绍基本和高级主题同样地。您可以从头到尾阅读它，或稍后将其用作参考。自动生成的 [API 参考](internallink) 也可能对您有意义。它涵盖了更多细节，但解释不如本教程。解决方案最常见的问题可以在我们的 [食谱](internallink) 集合或 [常见问题](internallink) 页面中找到。如果你需要任何帮助，加入我们的 [邮件列表](mailto:bottlepy@googlegroups.com) 或访问我们的 [IRC频道](http://webchat.freenode.net/?channels=bottlepy) 。

### __1.1.1 安装__

Bottle 不依赖于任何外部库。您只需将 [bottle.py](bottle.py) 下载到项目目录中即可开始编码：

```shell
$ wget https://bottlepy.org/bottle.py
```

这将为您提供包含所有新功能的最新开发快照。如果你更喜欢稳定环境，你应该坚持稳定的发布版本。这些可在 [PyPI](http://pypi.python.org/pypi/bottle) 上获得，并可以通过 __pip__ 安装（推荐），__easy_install__ 或您自己的包管理器：

```shell
$ sudo pip install bottle # recommended
$ sudo easy_install bottle # alternative without pip
$ sudo apt-get install python-bottle # works for debian, ubuntu, ...
```

无论哪种方式，您都需要使用 Python 2.7 或更高版本（包括3.2+）来运行 Bottle 程序。如果您没有权限或者根本不想要在系统范围内安装软件包，首先创建一个 [virtualenv](http://pypi.python.org/pypi/virtualenv) ：

```shell
$ virtualenv develop # Create virtual environment
$ source develop/bin/activate # Change default python to virtual one
(develop)$ pip install -U bottle # Install bottle to virtual environment
```

或者，如果您的系统上未安装 virtualenv：

```shell
$ wget https://raw.github.com/pypa/virtualenv/master/virtualenv.py
$ python virtualenv.py develop # Create virtual environment
$ source develop/bin/activate # Change default python to virtual one
(develop)$ pip install -U bottle # Install bottle to virtual environment
```
### __1.1.2 快速入门："Hello World"__





<br/><br/><br/><br/><br/><br/><br/>
<div id="1003" style="font-size:21px;font-weight:bold">1.3 请求路由</div>

Bottle 使用一个强大的路由引擎为每个请求找到正确的回调函数。本教程向您展示了基础知识。
本文档详细介绍了高级技术和规则机制。 

### 1.3.1 语法规则

Router 区分两种基本类型的路由：静态路由（例如 /contact）和动态路由（例如 /hello/\<name>）。包含一个或多个通配符的路由被视为动态路由。所有其他的路由都是静态的。

在 0.10. 版本修改的。

最简单的通配符形式由尖括号括起来的名称组成（例如 \<name>）。这个名字对于给定的路由应该是唯一的，并是一个有效的 python 标识符（字母数字，以字母开头）。这是因为通配符稍后会用作请求回调函数的关键字参数。

每个通配符都匹配一个或多个字符，但在第一个斜杠（/）处停止。这等于正则表达式 [^/]+ 并确保只匹配一个路径段，并且使具有多个通配符的路由保持明确。

规则 /\<action>/\<item> 匹配如下：

|路径|结果|
|----|----|
|/save/123|{'action': 'save', 'item': '123'}|
|/save/123/|不匹配|
|/save/|不匹配|
|//123|不匹配|

是否可以使用反斜杠 \ 来转义冒号 : 等字符？这将阻止触发旧语法，如果你需要使用：例如：规则 /\<action>/item:\<id> 将触发旧语法，（见下文）但是 /action/item\\:\<id> 会按预期使用新语法。

您可以使用过滤器以多种方式更改确切行为。这将在下一节中介绍。

### 1.3.2 通配符过滤器

在 0.10. 版本新增的。

过滤器用于定义更具体的通配符，并且/或者 在被传递到回调函数之前，转换 URL 的匹配部分。被过滤的通配符声明为 \<name:filter> 或 \<name:filter:config> 。 语法可选的配置部分取决于使用的过滤器。

Bottle 实现了以下标准过滤器：

+ :int 匹配（带符号）数字并将值转换为整数。
+ :float 类似于 :int 但是用于精度型数字。
+ :path 以非贪婪的方式匹配包括斜杠字符在内的所有字符，并可用于匹配多个路径段。
+ :re[:exp] 允许您在配置字段中指定自定义正则表达式。匹配的值不是被修改的。

您可以将自己的过滤器添加到路由器。 您只需要一个返回三个元素的函数：正则表达式string，用于将URL片段转换为python值的callable和用于执行相反操作的callable。 过滤器使用配置字符串作为唯一参数调用函数，并可根据需要对其进行解析：

```python
app = Bottle()

def list_filter(config):
    ''' Matches a comma separated list of numbers. '''
    delimiter = config or ','
    regexp = r'\d+(%s\d)*' % re.escape(delimiter)

    def to_python(match):
        return map(int, match.split(delimiter))

    def to_url(numbers):
        return delimiter.join(map(str, numbers))

    return regexp, to_python, to_url

    app.router.add_filter('list', list_filter)

    @app.route('/follow/<ids:list>')
    def follow_users(ids):
        for id in ids:
            ...
```

### 1.3.3 旧语法

在 0.10. 版本修改的。

新的规则语法在 Bottle 0.10 中引入，以简化一些常见用例，但旧语法仍然有效，你可以找到很多仍在使用它的代码示例。以下示例可以很好的描述差异：

|Old Syntax|New Syntax|
|----|----|
|:name|\<name>|
|:name#regexp#|\<name:re:regexp>|
|:#regexp#|\<:re:regexp>|
|:##|\<:re>|

如果可以的话，在新项目中尽量避免使用旧语法。它目前尚未被弃用，但最终将被弃用。

### 1.3.4 显式路由配置

路由装饰器也可以直接调用为方法。这种方式为复杂的设置提供了灵活性，允许你直接控制何时以及如何完成路由配置。

下面是一个默认 Bottle 程序的显式路由配置的基本示例：

```python
def setup_routing():
    bottle.route('/', 'GET', index)
    bottle.route('/edit', ['GET', 'POST'], edit)
```

实际上，任何 Bottle 实例的路由都可以配置为相同的方式：

```python
def setup_routing(app):
    app.route('/new', ['GET', 'POST'], form_new)
    app.route('/edit', ['GET', 'POST'], form_edit)

app = Bottle()
setup_routing(app)
```

## 1.4 简单模板引擎

Bottle 附带一个快速，功能强大且易于学习的内置模板引擎，简称 SimpleTemplate 或 stpl。它是 view() 和 template() 帮助程序使用的默认引擎，但也可以用作独立的通用目的模板引擎。本文档解释了模板语法并显示了常见用例的示例。

