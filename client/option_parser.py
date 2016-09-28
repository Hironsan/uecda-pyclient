# -*- coding:utf-8 -*-
from optparse import OptionParser


class OptParser(object):
    """
    コマンドライン引数の解析をするクラス
    """
    def __init__(self):
        usage = u'%prog [Args] [Options]\nDetailed options -h or --help'  # コマンドエラー時に表示する文字列
        version = 0.1
        self.parser = OptionParser(usage=usage, version=version)
        self.add_option('-p', '--port', typ='int', dest='port', hlp='Set server port number')
        self.add_option('-n', '--name', typ='str', dest='name', hlp='Set client name')
        self.add_option('-a', '--address', typ='str', dest='addr', hlp='Set server address')
        self.set_default()
        self.options, args = self.parser.parse_args()

    def add_option(self, opt1, opt2, typ, dest, hlp, action='store'):
        """
        オプションを追加する
        """
        self.parser.add_option(
            opt1, opt2,       # オプション
            action = action,  # 行う処理
            type   = typ,     # 型指定
            dest   = dest,    # 保存先変数名
            help   = hlp      # --help時に表示する文
        )

    def set_default(self, port=42485, name='default', addr='127.0.0.1'):
        """
        各オプションのデフォルト値をセットする
        """
        self.parser.set_defaults(
            port = port,
            name = name,
            addr = addr
        )

    def get_options(self):
        return self.options.addr, self.options.name, self.options.port