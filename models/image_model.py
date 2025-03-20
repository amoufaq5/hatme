# models/image_model.py
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.preprocessing import image

class ImageDiagnosisModel:
    def __init__(self):
        self.model = self.build_model()
        # In production, load trained weights:
        # self.model.load_weights('path_to_trained_weights.h5')

    def build_model(self):
        model = Sequential([
            Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
            MaxPooling2D((2, 2)),
            Conv2D(64, (3, 3), activation='relu'),
            MaxPooling2D((2, 2)),
            Flatten(),
            Dense(128, activation='relu'),
            Dense(2, activation='softmax')  # Binary classification example
        ])
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
        return model

    def predict(self, image_path):
        # Preprocess the image for prediction.
        img = image.load_img(image_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0) / 255.0
        predictions = self.model.predict(img_array)
        predicted_class = int(np.argmax(predictions, axis=1)[0])
        return "Normal findings." if predicted_class == 0 else "Abnormal findings detected. Further evaluation required."
