"""生徒が変更する場所①：診断項目と使用するAIモデル。"""
# models/ の下にフォルダを作り、keras_model.h5 と labels.txt を入れます。
# 新しい診断を追加するときは、この辞書に1行追加してください。
DIAGNOSIS_MODELS = {
    "whole": "株全体",
    "leaf": "葉",
    "fruit": "実",
    # "pest": "病害虫",  # 追加例：models/pest/ にモデルを置く
}
