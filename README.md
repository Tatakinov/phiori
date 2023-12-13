# これは何？

[phiori](https://github.com/phiori/phiori)
を令和の世に復活させる試み。

# Caution

**fork元とはセーブデータの互換性がありません。**

fork元のphioriを更新する目的で導入するのは非推奨です。

# 使い方

phiori.dllは同dllがあるフォルダの\*.pyを読み込むようになっています。
したがってファイル構成は

```
ghost/master
    |- config.txt
    |- descript.txt
    |- dlls
        |- LICENSE.txt
        |- _asyncio.pyd
        |- _bz2.pyd
        |- ...
    |- example.py
    |- phiori
        |- __init__.py
        |- builtins
        |- collections.py
        |- ...
    |- phiori.dll
    |- python312.dll
    |- python312.zip
    |- resource.txt
    |- words.dic
```

のようになると思われます。

[Python Release for Windows](https://www.python.org/downloads/windows/)
の最新版のWindows embeddable package (32-bit)
を解凍してpython312.dllとpython312.zipをghost/master以下に配置して
残りをdllsにリネームすると良いと思います。

# ビルド

[Python Release for Windows](https://www.python.org/downloads/windows/)
からWindows installer (32-bit)をダウンロードしてインストールする。

pythonのinclude, libsそれぞれにパスを通して

```
cd phiori.dll
clang -o phiori.dll -shared *.c -lpython312
```

もしくはパスを通さずに直接

```
cd phiori.dll
clang -I path/to/python/include -L path/to/python/libs -o phiori.dll -shared *.c -lpython312
```

とする。

# ライセンス

phiori.dllはLGPL3、example.pyおよびphioriモジュールはMIT Licenseです。

