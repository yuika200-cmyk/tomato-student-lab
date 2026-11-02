# 🍅 植物診断ラボ・生徒用ひな形

## このひな形の目的
自分たちで撮影・分類したミニトマトの写真をTeachable Machineで学習させ、AIモデルとアドバイスを改良します。一般公開版とは別アプリです。個人のログインやSupabaseは使いません。

## ① モデルを準備する
Teachable Machineで「画像プロジェクト」を作り、クラス（例：良好、葉が黄色い）ごとに写真を入れて学習します。
「モデルをエクスポート」→ **TensorFlow → Keras** 形式を選び、ファイルをダウンロードします。
`keras_model.h5` と `labels.txt` を次のように置きます。

```
models/
  whole/keras_model.h5
  whole/labels.txt
  leaf/keras_model.h5
  leaf/labels.txt
  fruit/keras_model.h5
  fruit/labels.txt
```

※同梱ZIPには重いAIモデルそのものは含めていません。空のままでもアプリは起動します。

## ② 生徒が変更するファイル
- `settings.py`：診断する分野を追加・変更する。新しい分野 `pest` を使うなら `models/pest/` にモデルファイルを置く。
- `advice.py`：判定ラベルごとのアドバイス文を書く（ラベル名は`labels.txt`と一致させる）。
- `app.py`：基本の診断画面。最初は変更しなくてもよい。

## ③ ローカルで起動する
Python 3.11 を使ってください（TensorFlow 2.15.1との互換性のため）。

```
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

※ Windowsでは `py -3.11 -m pip ...` や仮想環境を使うことをおすすめします。

## ④ 元のアプリと比較する
同じ評価用写真を使い、元のモデルと改良モデルの正解数を比較してください。**学習に使った写真は評価に使わない**こと。スコアは正解率ではありません。

## ⑤ 学校での注意
- 人の顔・名札・位置情報などが写る写真は使わない。
- 学習・共有目的で使う写真は撮影者や学校のルールに従い、許可を取る。
- 一般公開版のSupabaseの秘密鍵・ユーザー情報をコピーしない。
- 各班の公開アプリは必要に応じて教師が確認する。
