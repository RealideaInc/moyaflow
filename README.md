# MOYAFLOW

[VoTT](https://github.com/microsoft/VoTT)でアノテーションして作成したJSONファイルとその画像データをyolov5のフォーマットに変換するPythonスクリプトです。画像データの水増しもできます。

![moyaflowimage3](https://user-images.githubusercontent.com/69300459/165578664-99d080e1-66f7-4464-bcd7-74845f67d21f.png)

# Usage

```bash
$ git clone https://github.com/RealideaInc/moyaflow.git
```

```bash
$ cd moyaflow
```

```bash
$ python moyaflow.py /Your/VoTTJson/Dir/Path /Your/Image/Dir/Path  
```

# DEMO

1. [GitHub - microsoft/VoTT: Visual Object Tagging Tool: An electron app for building end to end Object Detection Models from Images and Videos.](https://github.com/microsoft/VoTT)や[【物体検出】アノテーションツールVoTTの使い方](https://sleepless-se.net/2019/06/21/how-to-use-vott/)などを参考にVoTTでアノテーションを行う。
   この時**VoTTJson**として出力する。

2. `moyaflow.py`を`clone`またはダウンロードして、`moyaflow.py`が存在するディレクトリで以下のコマンドを入力
   
   ```bash
   $ python moyaflow /Json/Dir/Path /Image/Dir/Path Feature 
   ```

3. カレントディレクトリに`/yolov5_anotation_data`ができています。これがyolov5フォーマットの学習データです。

# Features

[How To Convert VoTT JSON to YOLOv5 PyTorch TXT](https://roboflow.com/convert/vott-json-to-yolov5-pytorch-txt)と同じ機能です。こちらには枚数制限がありますが`moyaflow`には枚数制限はありません。

# Requirement

* `python 3.0`系

# ## moyaflow.py

- 必要な引数:
  
  - **JSON_PATH** ：           JSONファイルが入っているディレクトリのパス。
  - **IMAGE_PATH** ：          画像ファイルが入っているディレクトリのパス。

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
    olov5_anotation_data(変更可能)
    ├── data.yaml
    ├── test
    │ ├── images
    │ └── labels
    ├── train
    │ ├── images
    │ └── labels
    └── valid
     ├── images
     └── labels
    ```

## point_checker.py

- moyaflow.pyで出来た画像ファイルとlabel.txtが正しく対応しているかを確認するデバッグ用プログラムです。

- 引数とかは特に作ってないので、pythonファイルの中身を適当に変更して使ってください
