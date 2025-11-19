import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense
from tensorflow.keras.losses import MeanSquaredError
import numpy as np
import pandas as pd
from pathlib import Path

MODEL_FILE = Path("rnn_task_model.h5")
DATA_FILE = Path("tasks_data.csv")

class RNNModel:
    def __init__(self):
        self.model = None
        self.min_data_rows = 1000
        self.load_model()

    def load_model(self):
        if MODEL_FILE.exists():
            try:
                self.model = load_model(MODEL_FILE, compile=False)
                self.model.compile(optimizer="adam", loss=MeanSquaredError())
            except Exception as e:
                print(f"Failed to load model: {e}")
                self.model = None
        else:
            self.model = None

    def preprocess(self, df):
        X = df[["CPU","RAM"]].values
        y = df["total_score"].values
        return X, y

    def train_from_csv(self, epochs=5):
        if not DATA_FILE.exists():
            return
        df = pd.read_csv(DATA_FILE)
        if len(df) < self.min_data_rows:
            return
        X, y = self.preprocess(df)
        self.model = Sequential()
        self.model.add(Dense(32, input_dim=X.shape[1], activation="relu"))
        self.model.add(Dense(16, activation="relu"))
        self.model.add(Dense(1))
        self.model.compile(optimizer="adam", loss=MeanSquaredError())
        self.model.fit(X, y, epochs=epochs, verbose=0)
        self.model.save(MODEL_FILE)

    def predict(self, task):
        if self.model is None or not MODEL_FILE.exists():
            return np.random.uniform(10,80)

        X = np.array([[task["CPU"], task["RAM"]]])
        pred = self.model.predict(X, verbose=0)

        # Robust float extraction
        try:
            if isinstance(pred, np.ndarray):
                return float(pred.item()) if pred.size == 1 else float(pred[0,0])
            elif isinstance(pred, list):
                return float(pred[0][0])
            else:
                return float(pred)
        except Exception as e:
            print("Predict conversion error:", e)
            return np.random.uniform(10,80)
