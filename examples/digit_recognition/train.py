"""
Training script for ResNet152 image classifier.

Usage:
    train.py <PATH> --epochs <N_EPOCHS>

Arguments:
    - PATH The path to which the trained model is saved
    - N_EPOCHS The number of epochs for which model is trained
"""

import sys
import argparse
import tensorflow as tf
from typing import Tuple
from tensorflow.keras import datasets, layers, losses, Model

# Script exit codes
EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# The default number of training epochs
DEFAULT_N_EPOCHS = 1


def parse_arguments() -> Tuple[str, int]:
    """
    Parse commandline arguments.
    :return (path, n_epochs)
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path", type=str, help="The path to which the model is saved."
    )
    parser.add_argument(
        "--epochs",
        "-e",
        type=int,
        default=DEFAULT_N_EPOCHS,
        help=f"Default number of training epochs (default: {DEFAULT_N_EPOCHS})",
    )
    args = parser.parse_args()
    return args.path, args.epochs


def prepare_data() -> Tuple:
    """Load the MNIST image dataset."""
    (X_train, y_train), (X_test, y_test) = datasets.mnist.load_data()

    X_train = tf.pad(X_train, [[0, 0], [2, 2], [2, 2]]) / 255
    X_test = tf.pad(X_test, [[0, 0], [2, 2], [2, 2]]) / 255
    X_train = tf.expand_dims(X_train, axis=3, name=None)
    X_test = tf.expand_dims(X_test, axis=3, name=None)
    X_train = tf.repeat(X_train, 3, axis=3)
    X_test = tf.repeat(X_test, 3, axis=3)

    X_val = X_train[-2000:, :, :, :]
    y_val = y_train[-2000:]

    X_train = X_train[:-2000, :, :, :]
    y_train = y_train[:-2000]

    return (X_train, y_train), (X_test, y_test), (X_val, y_val)


def prepare_model():
    """Load a pretrained model and prepare for fine-tuning."""
    # Load the base model, ResNet152
    model = tf.keras.applications.ResNet152(
        weights="imagenet", include_top=False, input_shape=(32, 32, 3)
    )
    for layer in model.layers:
        layer.trainable = False

    # Add the trainable layers
    x = layers.Flatten()(model.output)
    x = layers.Dense(1000, activation="relu")(x)
    predictions = layers.Dense(10, activation="softmax")(x)

    # Build and compile the complete model
    head_model = Model(inputs=model.input, outputs=predictions)
    head_model.compile(
        optimizer="adam",
        loss=losses.sparse_categorical_crossentropy,
        metrics=["accuracy"],
    )
    return head_model


def train(path: str, epochs: int):
    """
    Train and save ResNet152 image classifier.
    :param path The path to which the model is saved
    :param epochs The number of training epochs
    """
    # Load the dataset
    (X_train, y_train), (_, _), (X_val, y_val) = prepare_data()

    # Instantiate the model
    model = prepare_model()

    # Fit the model
    _ = model.fit(
        X_train,
        y_train,
        batch_size=64,
        epochs=epochs,
        validation_data=(X_val, y_val),
    )

    # Save the model
    model.save(path)


def main() -> int:
    path, epochs = parse_arguments()
    try:
        train(path, epochs)
    except Exception:
        return EXIT_FAILURE
    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
