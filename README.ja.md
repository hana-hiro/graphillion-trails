# graphillion-trails

(C)2014-2015 Hiroyuki HANADA <hana-hiro@live.jp>

当プログラムは、著者が研究プロジェクト「ERATO湊離散構造処理系プロジェクト」
（科学技術振興機構）の在籍中に作成したものです。
https://www-erato.ist.hokudai.ac.jp/
http://www.jst.go.jp/erato/research_area/ongoing/mrk_PJ.html

# 1. 概要

このプログラムは、グラフ中の経路列挙を取り扱うライブラリ「Graphillion」を用いて、
グラフ中のtrail（辺素な路）あるいはEulerian trail（すべての辺を一度ずつ用いる路）を
列挙するものです。

例えば、以下のグラフにおいて、BからCへ至る異なるtrailは9つあります。
(BC, BAC, BDC, BACBDC, BACDBC, BDCABC, BCABDC, BDCBAC, BCDBAC)
またそのうち、後ろの6つがEulerian trailです。

    A----B
    | __/|
    |/   |
    C----D

# 2. 技術的な解説

これまで、trailではなくsimple path（点素な路）を列挙することについては多数の検討があり、
特にzero-suppressed binary decision diagram (ZDD)を用いた方法は、多くの現実の問題に
対して有効に機能することが知られています（最悪時間計算量では従来と変わらず最悪で指数時間）。

著者はこのsimple path列挙手法を、trailの列挙のために用いることを検討し、
これが行える条件を数学的に示すとともに実装しました。
具体的には、元のグラフの各辺に一対一対応する点を持つグラフ「line graph」を用いています。
http://link.springer.com/chapter/10.1007/978-3-319-15612-5_15 （国際会議原稿）
http://www-alg.ist.hokudai.ac.jp/~thomas/TCSTR/tcstr_14_79/tcstr_14_79.pdf （上記のテクニカルレポート版）
（上記の記事ではEulerian trailに限定して議論していますが、一般のtrailでも方法は同じです）

なお本プログラムでは、simple pathを列挙するためのソフトウェアとして、上記の手法を
Pythonから使えるようにしたライブラリ「Graphillion」を用いています。
[Graphillion配布サイト]
https://github.com/takemaru/graphillion
[技術解説（英語）]
http://www-alg.ist.hokudai.ac.jp/~thomas/TCSTR/tcstr_13_65/tcstr_13_65.pdf

# 3. 準備

PythonとGraphillion（上記参照）をインストールしてください。

# 4. 動かす

まず、グラフを表すファイルを用意します。（サンプルも含まれています。）
グラフを表すファイルは、各行が辺を表し、各行をスペースで区切ったそれぞれが頂点を表すものとします。
（一つの行にスペースがちょうど一つ存在している必要があります。）
グラフを表すファイルは、拡張子を.graphとすることを推奨します。

例えば、

    A----B
    | __/|
    |/   |
    C----D

このグラフを表すには、ファイルの内容は

    A B
    A C
    B C
    B D
    C D

とします。

例えば、上記の内容のファイルがsample/box.graphにあるときに

    python graphtrail.py -E B,C sample/box.graph

と入力すると、

    Number of trails: 9
    Computation time (sec): 0.003668
    Number of pairs of edges as constraints: 24
    Trails:
    B, C, A, B, D, C
    B, C, D, B, A, C
    B, D, C, A, B, C
    B, D, C, B, A, C
    B, A, C, B, D, C
    B, A, C, D, B, C
    B, A, C
    B, C
    B, D, C

のように出力されます。冒頭に示した通り、相異なるtrailが9個あると計算されました。
なお、「-E A,D」の部分で、「Aを起点、Dを終点とするtrailを列挙する」となります。

-E を -U に変えると、オイラー路（すべての辺をちょうど1度ずつ使うtrail）を列挙します。

    python graphtrail.py -U B,C sample/box.graph

と入力すると、

    Number of trails: 6
    Computation time (sec): 0.003417
    Number of pairs of edges as constraints: 24
    Trails:
    B, C, A, B, D, C
    B, C, D, B, A, C
    B, D, C, A, B, C
    B, D, C, B, A, C
    B, A, C, B, D, C
    B, A, C, D, B, C

のように出力されます。

なお上記の処理においては、以下の拡張子によりファイルが自動生成されます。

ファイル名.graph   - 元のグラフ
ファイル名.sgraph  - 元のグラフを単純グラフにしたもの
ファイル名.lsgraph - 単純グラフをline graphにしたもの
ファイル名.lsgraph.json
- Line graphにする前の元のグラフの頂点から、それを含むline graph上の頂点
  （＝元のグラフ上の辺）の一覧を得る連想配列

# 5. コマンドラインオプション

python graphtrail.py -h で見られます。

# 6. ライセンス

MIT Licenseで公開しております。正文（英語）はLICENSE.txtにあります。

# 7. お問い合わせ

Hiroyuki HANADA <hana-hiro@live.jp> （日本語か英語でお願いします）

