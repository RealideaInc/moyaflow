# moyaflow

roboflowのオマージュです

## moyaflow.py

- VoTTで作成したJSONファイルとその画像データをyolov5のフォーマットに変換します。

- 必要な引数:

  - INPUT_JSON ：           JSONファイルが入っているディレクトリのパス。
  - INPUT_IMAGE ：          画像ファイルが入っているディレクトリのパス。

- オプション引数:

  - -h, --help    ：        ヘルプ。
  - -s SIZE, --size SIZE：  出力画像ファイルの一辺の長さを決めます（画像ファイルは正方形）。
  
 - pythonファイルの最初のグローバル引数を変更することで、`train`、`test`、`valid`の割合を変更できます。
    
    - train + test + valid = 10にしてください。
  
## point_checker.py

- moyaflow.pyで出来た画像ファイルとlabel.txtが正しく対応しているかを確認するプログラムです。

- 引数とかは特に作ってないので、pythonファイルの中身を適当に変更して使ってください


  
  
