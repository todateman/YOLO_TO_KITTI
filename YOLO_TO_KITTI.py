# python YOLO_TO_KITTI.py --yolo_labels "C:\Users\Username\datasets\yolo_labels" --images "C:\Users\Username\datasets\images" --kitti_labels "C:\Users\Username\datasets\kitti_labels"
# python YOLO_TO_KITTI.py --data_dir "C:\Users\Username\datasets"

import os
from PIL import Image

# YOLOクラスIDからKITTIクラス名へのマッピング
CLASS_MAPPING = {
    '0': 'bike',
    '1': 'bus',
    '2': 'car',
    '3': 'truck'
}

# デフォルト値
TRUNCATED = 0
OCCLUDED = 0
ALPHA = 0
# 3D情報やその他のフィールドは空白またはデフォルト値に設定
HEIGHT = 0
WIDTH = 0
LENGTH = 0
POSE = 0
TRUNCATION_LEVEL = 0
# バウンディングボックスの3D座標やその他の情報は省略

def yolo_to_kitti(yolo_label, img_width, img_height):
    """
    YOLOラベルをKITTI形式に変換する
    """
    class_id, x_center, y_center, width, height = yolo_label
    class_name = CLASS_MAPPING.get(class_id, 'DontCare')

    # YOLOの座標は正規化されているため、ピクセル単位に変換
    x_center = float(x_center) * img_width
    y_center = float(y_center) * img_height
    width = float(width) * img_width
    height = float(height) * img_height

    # KITTIのバウンディングボックスは左上と右下の座標
    bbox_left = x_center - (width / 2)
    bbox_top = y_center - (height / 2)
    bbox_right = x_center + (width / 2)
    bbox_bottom = y_center + (height / 2)

    # フォーマットに合わせて文字列を作成
    kitti_label = f"{class_name} {TRUNCATED} {OCCLUDED} {ALPHA} " \
                 f"{int(bbox_left)} {int(bbox_top)} {int(bbox_right)} {int(bbox_bottom)} " \
                 f"{HEIGHT} {WIDTH} {LENGTH} {POSE}\n"

    return kitti_label

def get_image_extension(image_dir, base_filename):
    """
    画像ディレクトリ内で指定されたベースファイル名に一致する画像ファイルの拡張子を取得する
    """
    for ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
        if os.path.exists(os.path.join(image_dir, base_filename + ext)):
            return ext
    return None

def convert_yolo_to_kitti(yolo_labels_dir, images_dir, kitti_labels_dir):
    """
    YOLO形式のラベルディレクトリをKITTI形式に変換する
    """
    # パスを絶対パスに変換
    yolo_labels_dir = os.path.abspath(yolo_labels_dir)
    images_dir = os.path.abspath(images_dir)
    kitti_labels_dir = os.path.abspath(kitti_labels_dir)

    # ディレクトリの存在を確認
    if not os.path.isdir(yolo_labels_dir):
        print(f"YOLOラベルディレクトリが存在しません: {yolo_labels_dir}")
        return
    if not os.path.isdir(images_dir):
        print(f"画像ディレクトリが存在しません: {images_dir}")
        return
    if not os.path.exists(kitti_labels_dir):
        os.makedirs(kitti_labels_dir)

    # ラベルファイルをループ
    for label_file in os.listdir(yolo_labels_dir):
        if not label_file.endswith('.txt'):
            continue

        yolo_path = os.path.join(yolo_labels_dir, label_file)
        base_filename = os.path.splitext(label_file)[0]
        
        # 画像の拡張子を自動検出
        image_ext = get_image_extension(images_dir, base_filename)
        if image_ext is None:
            print(f"画像ファイルが見つかりません: {base_filename}.* in {images_dir}")
            continue

        image_filename = base_filename + image_ext
        image_path = os.path.join(images_dir, image_filename)

        # 画像のサイズを取得
        try:
            with Image.open(image_path) as img:
                img_width, img_height = img.size
        except Exception as e:
            print(f"画像ファイルを開けません: {image_path}. エラー: {e}")
            continue

        kitti_labels = []

        # YOLOラベルファイルを読み込み
        try:
            with open(yolo_path, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) != 5:
                        print(f"無効なラベル行: {line.strip()} in {yolo_path}")
                        continue
                    kitti_label = yolo_to_kitti(parts, img_width, img_height)
                    kitti_labels.append(kitti_label)
        except Exception as e:
            print(f"ラベルファイルを読み込めません: {yolo_path}. エラー: {e}")
            continue

        # KITTIラベルファイルを書き込み
        kitti_path = os.path.join(kitti_labels_dir, label_file)
        try:
            with open(kitti_path, 'w') as f:
                f.writelines(kitti_labels)
            print(f"変換完了: {label_file} -> {kitti_path}")
        except Exception as e:
            print(f"KITTIラベルファイルを書き込めません: {kitti_path}. エラー: {e}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Convert YOLO labels to KITTI format.")
    group = parser.add_mutually_exclusive_group(required=True)
    
    # 個別のディレクトリ指定オプション
    group.add_argument('--yolo_labels', type=str, help='YOLO形式のラベルディレクトリへのパス（絶対パスまたは相対パス）')
    group.add_argument('--data_dir', type=str, help='データセットのベースディレクトリへのパス（絶対パスまたは相対パス）')

    # 個別のディレクトリ指定オプションを使用する場合の追加引数
    parser.add_argument('--images', type=str, help='画像ディレクトリへのパス（--data_dir使用時は不要）')
    parser.add_argument('--kitti_labels', type=str, help='KITTI形式のラベルを保存するディレクトリへのパス（--data_dir使用時は不要）')

    args = parser.parse_args()

    if args.data_dir:
        # --data_dirが指定された場合のディレクトリ設定
        data_dir = os.path.abspath(args.data_dir)
        yolo_labels_dir = os.path.join(data_dir, 'labels')
        images_dir = os.path.join(data_dir, 'images')
        kitti_labels_dir = os.path.join(data_dir, 'kitti_labels')
        convert_yolo_to_kitti(yolo_labels_dir, images_dir, kitti_labels_dir)
    else:
        # 個別のディレクトリ指定オプションが指定された場合
        if not args.yolo_labels or not args.images or not args.kitti_labels:
            print("個別のディレクトリ指定を使用する場合、--yolo_labels、--images、--kitti_labelsの全てを指定してください。")
            exit(1)
        convert_yolo_to_kitti(args.yolo_labels, args.images, args.kitti_labels)
