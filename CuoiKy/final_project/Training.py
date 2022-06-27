from os import listdir
from keras_facenet import FaceNet
from tensorflow import keras
import os
import numpy as np
import cv2
from os.path import isdir
from PIL import Image
import pickle
from glob import glob
import shutil
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import joblib
from keras import models

facenet_model = models.load_model("facenet_keras.h5")

processed_folder = "image_train"


def get_embedding(model, face_pixels):
    face_pixels = face_pixels.astype("float32")
    face_pixels = cv2.resize(face_pixels, (160, 160))
    # standardize pixel values across channels (global)
    mean, std = face_pixels.mean(), face_pixels.std()
    face_pixels = (face_pixels - mean) / std
    # transform face into one sample
    samples = np.expand_dims(face_pixels, axis=0)
    # make prediction to get embedding
    yhat = model.predict(samples)
    return yhat[0]


def load_faces(train_folder=processed_folder):
    if os.path.exists("faces_data.npz"):
        data = np.load("faces_data.npz")
        X_train, y_train = data["arr_0"], data["arr_1"]
        return X_train, y_train
    else:
        X_train = []
        y_train = []

        # enumerate folders, on per class
        for folder in listdir(train_folder):
            # Lặp qua các file trong từng thư mục chứa các em
            for file in listdir(train_folder + "/" + folder):  # +"/"+ folder
                # Read file
                image = Image.open(
                    train_folder + "/" + folder + "/" + file
                )  # +"/"+ folder
                # convert to RGB, if needed
                image = image.convert("RGB")
                # convert to array
                pixels = np.asarray(image)

                # Thêm vào X
                X_train.append(pixels)
                y_train.append(folder)

        X_train = np.array(X_train)
        y_train = np.array(y_train)

        # Check dữ liệu
        print(X_train.shape)
        print(y_train.shape)
        print(y_train[0:5])

        # Convert du lieu y_train
        output_enc = LabelEncoder()
        output_enc.fit(y_train)
        y_train = output_enc.transform(y_train)
        pkl_filename = "output_enc.pkl"
        with open(pkl_filename, "wb") as file:
            pickle.dump(output_enc, file)

        print(y_train[0:5])

        # Convert du lieu X_train sang embeding
        X_train_emb = []
        for x in X_train:
            X_train_emb.append(get_embedding(facenet_model, x))

        X_train_emb = np.array(X_train_emb)

        print("Load faces done!")
        # Save
        np.savez_compressed("faces_data.npz", X_train_emb, y_train)
        return X_train_emb, y_train


# Main program
X_train, y_train = load_faces()

# Train SVM với kernel tuyến tính
model = SVC(kernel="linear", probability=True)
model.fit(X_train, y_train)

# Save model
pkl_filename = "faces_svm.pkl"
with open(pkl_filename, "wb") as file:
    pickle.dump(model, file)

print("Saved model")
