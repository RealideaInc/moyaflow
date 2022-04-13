# moyaflow

roboflowのビッグバネイトです。

## moyaflow.py

- VoTTで作成したJSONファイルとその画像データをyolov5のフォーマットに変換します。

- 必要な引数:

  - INPUT_JSON ：           JSONファイルが入っているディレクトリのパス。
  - INPUT_IMAGE ：          画像ファイルが入っているディレクトリのパス。

- オプション引数:

  - -h, --help    ：        ヘルプ。
  - -s SIZE, --size SIZE：  出力画像ファイルの一辺の長さを決めます（画像ファイルは正方形）。
  - -d DataArgment, --DaraArgment：　水増しデータを作るオプションです。現在使えるフィルタはsalt, papper, smoothの三種類です。使いたいフィルタを-dの後に入れるとその分画像データが水増しされます。例えば、saltとsmoothを使いたければ"-d salt smooth"とします（これらは省略して"-d sa sm"としても動きます）。
  
 - pythonファイルの最初のグローバル引数を変更することで、`train`、`test`、`valid`の割合を変更できます。
    
    - train + test + valid = 10にしてください。
 - 出力フォルダの階層は以下のようになっています
 ```
 - trees
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
- もし、出力フォルダを変えたければ`BASE_OUTPUT_PATH`を変更してください（初期では実行したフォルダにtreesが作成されます）
- ## point_checker.py

- moyaflow.pyで出来た画像ファイルとlabel.txtが正しく対応しているかを確認するプログラムです。

- 引数とかは特に作ってないので、pythonファイルの中身を適当に変更して使ってください


  
  
