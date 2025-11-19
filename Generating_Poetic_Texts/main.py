import os
import numpy as np
import streamlit as st
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Activation
from tensorflow.keras.optimizers import RMSprop

MODEL_PATH = "textgenerator.h5"


# ----------------------------------
# 1) Utility: Sampling Function
# ----------------------------------
def sample(preds, temperature=1.0):
    preds = np.asarray(preds).astype("float64")
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    return np.random.choice(len(preds), p=preds)


# ----------------------------------
# 2) Load or Train Model
# ----------------------------------
@st.cache_resource
def load_or_train_model():
    if os.path.exists(MODEL_PATH):
        st.info("📌 Saved model found. Loading model...")
        model = load_model(MODEL_PATH)

        link = "https://storage.googleapis.com/download.tensorflow.org/data/shakespeare.txt"
        filepath = tf.keras.utils.get_file("shakespeare.txt", link)
        text = open(filepath, 'rb').read().decode('utf-8')

        characters = sorted(set(text))
        char_to_index = {c: i for i, c in enumerate(characters)}
        index_to_char = {i: c for i, c in enumerate(characters)}

        return model, char_to_index, index_to_char, characters, text

    else:
        st.warning("⚠️ No saved model found. Training a new model... This may take 3–5 minutes.")

        link = "https://storage.googleapis.com/download.tensorflow.org/data/shakespeare.txt"
        filepath = tf.keras.utils.get_file("shakespeare.txt", link)
        text = open(filepath, 'rb').read().decode('utf-8')

        characters = sorted(set(text))
        char_to_index = {c: i for i, c in enumerate(characters)}
        index_to_char = {i: c for i, c in enumerate(characters)}

        SEQ_LENGTH = 40
        STEP_SIZE = 1

        sentences = []
        next_chars = []

        for i in range(0, len(text) - SEQ_LENGTH, STEP_SIZE):
            sentences.append(text[i:i + SEQ_LENGTH])
            next_chars.append(text[i + SEQ_LENGTH])

        x = np.zeros((len(sentences), SEQ_LENGTH, len(characters)), dtype=bool)
        y = np.zeros((len(sentences), len(characters)), dtype=bool)

        for i, sentence in enumerate(sentences):
            for t, char in enumerate(sentence):
                x[i, t, char_to_index[char]] = True
            y[i, char_to_index[next_chars[i]]] = True

        # Build model
        model = Sequential()
        model.add(LSTM(128, input_shape=(SEQ_LENGTH, len(characters))))
        model.add(Dense(len(characters)))
        model.add(Activation('softmax'))

        model.compile(loss="categorical_crossentropy",
                      optimizer=RMSprop(learning_rate=0.01))

        model.fit(x, y, batch_size=256, epochs=4)

        model.save("textgenerator.h5", include_optimizer=False)
        st.success("✅ Model trained and saved successfully.")

        return model, char_to_index, index_to_char, characters, text


# ----------------------------------
# 3) Text Generation Function
# ----------------------------------
def generate_text(model, seed, length, temperature, char_to_index, index_to_char, SEQ_LENGTH=40):
    generated = seed

    for _ in range(length):
        x_pred = np.zeros((1, SEQ_LENGTH, len(char_to_index)))
        seed_cut = seed[-SEQ_LENGTH:]

        for t, char in enumerate(seed_cut):
            if char in char_to_index:
                x_pred[0, t, char_to_index[char]] = 1

        preds = model.predict(x_pred, verbose=0)[0]
        next_index = sample(preds, temperature)
        next_char = index_to_char[next_index]

        generated += next_char
        seed += next_char

    return generated


# ----------------------------------
# 4) Streamlit UI
# ----------------------------------
st.title("📝 LSTM Shakespeare Text Generator")
st.write("If a model exists, it will be loaded. Otherwise, a new one will be trained automatically.")

# Load or train model
model, char_to_index, index_to_char, characters, text = load_or_train_model()

# User inputs
seed_text = st.text_input("Enter a seed sentence:", "To be, or not to be, that is the ")
length = st.slider("Number of characters to generate", 50, 500, 200)

# Temperature presets
temp_option = st.selectbox("Choose a temperature preset:", ["Conservative", "Balanced", "Creative"])
temperature_dict = {"Conservative": 0.3, "Balanced": 0.6, "Creative": 1.0}
temperature = temperature_dict[temp_option]

st.write(f"⚡ Temperature set to {temperature} ({temp_option})")

if st.button("Generate Text"):
    output = generate_text(model, seed_text, length, temperature, char_to_index, index_to_char)
    st.subheader("🔮 Generated Text:")
    st.write(output)
