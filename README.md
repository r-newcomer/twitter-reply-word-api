# 環境構築
## Pythonのインストール
pyenvによるバージョン管理をする。

```
# pyenvのインストール
brew install pyenv

# pyenvのパスを通す (zsh)
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zsrc

# zshrcの保存を適用する
source ~/.zshrc

# pyenvでpythonのインストール (今回は3.9.9をインストールする)
pyenv install 3.9.9

# pyenvでバージョンを指定する (他のバージョンをインストールすれば、切り替えも可能)
pyenv local 3.9.9
pyenv global 3.9.9

# pythonのバージョンを確認する (Python 3.9.9が出力されればOK)
python --version

# もし、バージョンが変更されていなかった場合、デフォルトのpythonを参照している可能性があるのでpyenvを優先するようにviで修正する
vi /etc/paths

# 変更前
/usr/local/bin
/usr/bin
/bin

# 変更後
/usr/local/bin
/usr/bin
/bin
/usr/local/sbin
/usr/sbin
/sbin
```

## パッケージのインストール (ここら辺nodeみたいにいい感じにできないかな、、多分できる)
```
pip install uvicorn fastapi emoji requests requests_oauthlib mecab ipykernel
```

## WordCloud用にMatplotlibの日本語化
以下のリンクを参考にして行う。
`sudo apt install fontconfig`などは`sudo apt`を`brew`に置き換えて実装する
Ex.) `brew install fontconfig`
https://self-development.info/ipaexgothic%e3%81%ab%e3%82%88%e3%82%8bmatplotlib%e3%81%ae%e6%97%a5%e6%9c%ac%e8%aa%9e%e5%8c%96%e3%80%90python%e3%80%91/


## APIサーバーの起動
appディレクトリに移動して下記を実行する
`uvicorn main:app --reload `
