"""植物診断ラボ・生徒用ひな形：個人情報の保存・外部DB接続なし。"""
from pathlib import Path
import io
import numpy as np
import streamlit as st
from PIL import Image, ImageOps, UnidentifiedImageError
from settings import DIAGNOSIS_MODELS
from advice import ADVICE, DEFAULT_ADVICE

ROOT = Path(__file__).resolve().parent
MAX_BYTES = 10 * 1024 * 1024
Image.MAX_IMAGE_PIXELS = 25_000_000
st.set_page_config(page_title="植物診断ラボ・生徒版", page_icon="🍅", layout="centered")
st.title("🍅 植物診断ラボ・生徒版")
st.write("写真をAIで分類し、アドバイスを表示します。自分のモデルと文章に改良してみよう！")
st.caption("写真はアプリからデータベースに送信・保存しません。診断は参考情報です。")

@st.cache_resource(show_spinner="モデルを読み込んでいます…")
def load_model(path: str, mtime: float):
    from tensorflow.keras.models import load_model as keras_load_model
    return keras_load_model(path, compile=False)

@st.cache_data
def read_labels(path: str, mtime: float) -> list[str]:
    result = []
    for line in Path(path).read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split(maxsplit=1)
        result.append(parts[1] if len(parts) == 2 and parts[0].isdigit() else line)
    return result

def get_prediction(key: str, tensor: np.ndarray):
    model_file = ROOT / "models" / key / "keras_model.h5"
    labels_file = ROOT / "models" / key / "labels.txt"
    if not model_file.is_file() or not labels_file.is_file():
        return None
    labels = read_labels(str(labels_file), labels_file.stat().st_mtime_ns)
    model = load_model(str(model_file), model_file.stat().st_mtime_ns)
    scores = np.asarray(model.predict(tensor, verbose=0)[0], dtype=float)
    if len(labels) != len(scores) or not np.isfinite(scores).all() or not labels:
        raise ValueError(f"{key} のモデルと labels.txt が対応していません。")
    index = int(np.argmax(scores))
    return labels[index], float(scores[index])

uploaded = st.file_uploader("ミニトマトの写真を選ぶ", type=["jpg", "jpeg", "png"])
if uploaded is not None:
    content = uploaded.getvalue()
    if len(content) > MAX_BYTES:
        st.error("写真は10 MB以下にしてください。")
        st.stop()
    try:
        with Image.open(io.BytesIO(content)) as photo:
            photo.load()
            picture = ImageOps.exif_transpose(photo).convert("RGB")
    except (UnidentifiedImageError, OSError, ValueError):
        st.error("写真を読み込めませんでした。別の画像を選んでください。")
        st.stop()
    st.image(picture, caption="選んだ写真", use_container_width=True)

    if st.button("🔍 AIで診断する", type="primary", use_container_width=True):
        resized = ImageOps.fit(picture, (224, 224), method=Image.Resampling.LANCZOS)
        normalized = np.asarray(resized, dtype=np.float32) / 127.5 - 1.0
        batch = np.expand_dims(normalized, axis=0)
        successful = 0
        for key, title in DIAGNOSIS_MODELS.items():
            try:
                result = get_prediction(key, batch)
            except Exception as error:
                st.error(f"{title}の診断に失敗しました：{error}")
                continue
            if result is None:
                st.info(f"{title}：モデル未配置（models/{key}/ にファイルを入れてください）")
                continue
            successful += 1
            label, score = result
            st.subheader(f"{title}：{label}")
            st.write("💡 " + ADVICE.get(key, {}).get(label, DEFAULT_ADVICE))
            with st.expander("AIが各分類に出した数値について"):
                st.write(f"選ばれた分類のスコア：{score:.1%}（正解率ではありません）")
        if successful == 0:
            st.warning("まだAIモデルがありません。README.md を見てモデルを追加してください。")
else:
    st.info("まず写真を選んでください。")

st.divider()
st.markdown("**生徒が改良できるところ**：① `settings.py` で診断項目を増やす　② `models/` のAIモデルを入れ替える　③ `advice.py` の文章を変更する")
