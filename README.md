# UECda-pyclient
Basic UECda Client written in Python.

## Description
UECda-PyClientはコンピュータ大貧民大会であるUECdaのためのPythonクライアントです。
Pythonで書かれたことで、短くわかりやすいコードになりました。
また、TensorFlowやChainer、Theano等の機械学習ライブラリの使用にも適しています。

## Requirement
* Python2.7
* Python3.5 (HIGHLY RECOMMENDED)

## Usage
client.py が実行ファイルです。
この実行ファイルは次のような形式で実行できます。

```
$ python client.py

The following arguments are optional:
-a    server address [127.0.0.1]
-p    port [42485]
-n    user name < 15 characters [default]
-h    help
```


たとえば、サーバが同じコンピュータの42485ポートで待ち受けているときに、
クライアント名を default とする場合、次のように実行します。

```
$ python client.py -a 127.0.0.1 -p 42485 -n default
```

これは次の様に省略した場合と同じ設定となります。

```
$ python client.py
```

また、下記のように任意のものだけ指定することもできます。
この例はクライアント名を client01 と指定しています。

```
$ python client.py -n client01
```

クライアントを5つ同時に起動する場合、

```
$ python client.py &
```

のように最後に&(アンパサント)をつけると、クライアントがバックグラウンドで実行されるので、5つ続けて同時に起動できます


## Install

```
$ pip install -r requirements.txt
```

## Licence

[MIT](https://github.com/Hironsan/uecda-pyclient/blob/master/LICENSE)

## Author

[Hironsan](https://github.com/Hironsan)