# YOLO_TO_KITTI

ChatGPT o1-miniを活用して、YOLO形式のデータセットラベル付きデータセットをKITTI形式に変換するPythonスクリプトを作成しました。

I created a Python script to convert the YOLO format dataset labeled dataset into KITTI format using ChatGPT o1-mini.

## 使い方

画像ファイルのディレクトリ"images"とYOLO形式のラベルファイルのディレクトリ"labels"が既に存在する場合、--data_dir に続いてデータセットのディレクトリパスを指定してください。
（絶対パス・相対パスどちらも使用できます）

変換後のKITTI形式のラベルファイルはデータセットのディレクトリ内に"kitti_labels"のディレクトリで自動的に作成されます。


If the image file directory "images" and the YOLO format label file directory "labels" already exist, specify the dataset directory path following --data_dir.

(You can use either absolute or relative paths)

The converted KITTI format label files will be automatically created in the "kitti_labels" directory within the dataset directory.

```python
python YOLO_TO_KITTI.py --data_dir "C:\Users\Username\datasets"
```

---

画像ファイル、YOLO形式のラベルファイル、KITTI形式のラベルファイルの保存先を個別に指定する場合は以下のようになります。

If you want to specify the save destinations for the image file, YOLO format label file, and KITTI format label file individually, it will look like this.

```python
python YOLO_TO_KITTI.py --yolo_labels "C:\Users\Username\datasets\yolo_labels" --images "C:\Users\Username\datasets\images" --kitti_labels "C:\Users\Username\datasets\kitti_labels"
```

