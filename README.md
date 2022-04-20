# moyaflow

roboflowのビッグバネイトです。

## moyaflow.py

- VoTTで作成したJSONファイルとその画像データをyolov5のフォーマットに変換します。

- 必要な引数:

  - **INPUT_JSON** ：           JSONファイルが入っているディレクトリのパス。
  - **INPUT_IMAGE** ：          画像ファイルが入っているディレクトリのパス。

- オプション引数:

  - **-h, --help**    ：        ヘルプ。
  - **-s SIZE, --size SIZE**：  出力画像ファイルの一辺の長さを決めます（画像ファイルは正方形）。
  - **-p PATH, --path PATH:**: 出力されるデータのパスを指定できます。
  - **-r TRAIN,TEST,VALID, --rate TRAIN,TEST,VALID**: データファイルの割合を指定できます。**足して10**になるように、**コンマ区切り**で指定してください。コンマとコンマの間にスペースは**入れないでください**。デフォルトは\[train, test, valid\] = [7, 2, 1]です。
  - **-d DataArgment, --DaraArgment**：　水増しデータを作るオプションです。現在使えるフィルタはsalt, pepper, smooth, fliplrの4種類です。使いたいフィルタを-dの後に入れるとその分画像データが水増しされます。例えば、saltとsmoothを使いたければ"-d salt smooth"とします（これらは省略して"-d sa sm"としても動きます）。
    - **salt** : 塩ノイズと呼ばれるノイズをかけます。[wiki-ごま塩ノイズ](https://ja.wikipedia.org/wiki/%E3%81%94%E3%81%BE%E5%A1%A9%E3%83%8E%E3%82%A4%E3%82%BA)
    - **pepper** : ペッパーノイズと呼ばれるノイズをかけます。塩ノイズが黒くなっただけです。好きな方にしてください。
    - **smooth** : 平滑化フィルタ処理をします。画像をぼかすことができます。
    - **fliplr** : 左右が反転した画像を作ります。

 - 出力フォルダの階層は以下のようになっています
 ```
 - trees(変更可能)
  ├── data.yaml
  ├── test
  │   ├── images
  │   └── labels
  ├── train
  │   ├── images
  │   └── labels
  └── valid
      ├── images
      └── labels
```

- ## point_checker.py

- moyaflow.pyで出来た画像ファイルとlabel.txtが正しく対応しているかを確認するプログラムです。

- 引数とかは特に作ってないので、pythonファイルの中身を適当に変更して使ってください
