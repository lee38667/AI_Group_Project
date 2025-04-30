import cv2
import numpy as np
import os
import sys
import tensorflow as tf
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import EarlyStopping

EPOCHS = 50  # Let EarlyStopping decide the best epoch
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():
    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python traffic.py data_directory")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Early stopping callback
    early_stop = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)

    # Train the model with validation split and early stopping
    history = model.fit(
        x_train, y_train,
        epochs=EPOCHS,
        validation_split=0.2,
        callbacks=[early_stop]
    )

    # Evaluate neural network performance
    model.evaluate(x_test, y_test, verbose=2)

    # Plot training history
    plot_training_history(history)

    # Save model with versioning
    save_model_with_version(model)


def load_data(data_dir):
    images = []
    labels = []

    for label in range(NUM_CATEGORIES):
        label_dir = os.path.join(data_dir, str(label))
        if not os.path.isdir(label_dir):
            continue

        for filename in os.listdir(label_dir):
            filepath = os.path.join(label_dir, filename)
            image = cv2.imread(filepath)

            if image is None:
                continue

            image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))
            images.append(image)
            labels.append(label)

    return images, labels


def get_model():
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),

        tf.keras.layers.Flatten(),

        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.5),

        tf.keras.layers.Dense(NUM_CATEGORIES, activation='softmax')
    ])

    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return model


def plot_training_history(history):
    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']
    loss = history.history['loss']
    val_loss = history.history['val_loss']
    epochs_range = range(len(acc))

    plt.figure(figsize=(12, 5))

    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training vs. Validation Accuracy')

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training vs. Validation Loss')

    plt.tight_layout()
    plt.show()


def save_model_with_version(model, folder="."):
    """
    Save model to file as modelV#.h5, where # is the next available version number.
    """
    version = 1
    while os.path.exists(os.path.join(folder, f"modelV{version}.h5")):
        version += 1

    filename = os.path.join(folder, f"modelV{version}.h5")
    model.save(filename)
    print(f"Model saved to {filename}.")


if __name__ == "__main__":
    main()
