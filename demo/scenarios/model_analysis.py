import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import model_from_json


def load_model(model_filename: str, weights_filename: str):
    # Load model
    json_file = open(model_filename, "r")
    loaded_model_json = json_file.read()
    loaded_model = model_from_json(loaded_model_json)
    json_file.close()

    # Load weights into new model
    loaded_model.load_weights(weights_filename)

    return loaded_model


def run_model(im, loaded_model):
    im_batch = tf.expand_dims(im, 0)
    predictions = loaded_model(im_batch)
    return predictions


def read_image(filename):
    image = tf.io.read_file(filename)
    image = tf.io.decode_jpeg(image, channels=3)
    image = tf.image.convert_image_dtype(image, tf.float32)
    image = tf.image.resize_with_pad(image, target_height=224, target_width=224)
    return image


def generate_baseline_and_alphas():
    baseline = tf.zeros(shape=(224, 224, 3))
    m_steps = 50
    alphas = tf.linspace(
        start=0.0, stop=1.0, num=m_steps + 1
    )  # Generate m_steps intervals for integral_approximation() below.
    return baseline, alphas


def interpolate_images(baseline, image, alphas):
    alphas_x = alphas[:, tf.newaxis, tf.newaxis, tf.newaxis]
    baseline_x = tf.expand_dims(baseline, axis=0)
    input_x = tf.expand_dims(image, axis=0)
    delta = input_x - baseline_x
    images = baseline_x + alphas_x * delta
    return images


def integral_approximation(gradients):
    # riemann_trapezoidal
    grads = (gradients[:-1] + gradients[1:]) / tf.constant(2.0)
    int_gradients = tf.math.reduce_mean(grads, axis=0)
    return int_gradients


def compute_gradients(loaded_model, images, target_class_idx):
    with tf.GradientTape() as tape:
        tape.watch(images)
        probs = loaded_model(images)[:, target_class_idx]
        """
    If your model does not have a softmax output layer,
    comment out the above line and un-comment the following 2 lines
    """
        # logits = loaded_model(images)
        # probs = tf.nn.softmax(logits, axis=-1)[:, target_class_idx]

    return tape.gradient(probs, images)


@tf.function
def one_batch(baseline, image, alpha_batch, target_class_idx, loaded_model):
    # Generate interpolated inputs between baseline and input.
    interpolated_path_input_batch = interpolate_images(
        baseline=baseline, image=image, alphas=alpha_batch
    )

    # Compute gradients between model outputs and interpolated inputs.
    gradient_batch = compute_gradients(
        loaded_model=loaded_model,
        images=interpolated_path_input_batch,
        target_class_idx=target_class_idx,
    )
    return gradient_batch


def integrated_gradients(
    baseline, image, target_class_idx, loaded_model, m_steps=50, batch_size=32
):
    # Generate alphas.
    alphas = tf.linspace(start=0.0, stop=1.0, num=m_steps + 1)

    # Collect gradients.
    gradient_batches = []

    # Iterate alphas range and batch computation for speed, memory efficiency, and scaling to larger m_steps.
    for alpha in tf.range(0, len(alphas), batch_size):
        from_ = alpha
        to = tf.minimum(from_ + batch_size, len(alphas))
        alpha_batch = alphas[from_:to]

        gradient_batch = one_batch(
            baseline, image, alpha_batch, target_class_idx, loaded_model
        )
        gradient_batches.append(gradient_batch)

    # Concatenate path gradients together row-wise into single tensor.
    total_gradients = tf.concat(gradient_batches, axis=0)

    # Integral approximation through averaging gradients.
    avg_gradients = integral_approximation(gradients=total_gradients)

    # Scale integrated gradients with respect to input.
    gradients = (image - baseline) * avg_gradients
    return gradients


def plot_img_attributions(
    baseline,
    image,
    target_class_idx,
    loaded_model,
    m_steps=50,
    cmap=None,
    overlay_alpha=0.4,
):
    attributions = integrated_gradients(
        baseline=baseline,
        image=image,
        target_class_idx=target_class_idx,
        loaded_model=loaded_model,
        m_steps=m_steps,
    )

    # Sum of the attributions across color channels for visualization.
    # The attribution mask shape is a grayscale image with height and width
    # equal to the original image.
    attribution_mask = tf.reduce_sum(tf.math.abs(attributions), axis=-1)

    fig, axs = plt.subplots(nrows=2, ncols=2, squeeze=False, figsize=(8, 8))

    axs[0, 0].set_title("Baseline image")
    axs[0, 0].imshow(baseline)
    axs[0, 0].axis("off")

    axs[0, 1].set_title("Original image")
    axs[0, 1].imshow(image)
    axs[0, 1].axis("off")

    axs[1, 0].set_title("Attribution mask")
    axs[1, 0].imshow(attribution_mask, cmap=cmap)
    axs[1, 0].axis("off")

    axs[1, 1].set_title("Overlay")
    axs[1, 1].imshow(attribution_mask, cmap=cmap)
    axs[1, 1].imshow(image, alpha=overlay_alpha)
    axs[1, 1].axis("off")

    plt.tight_layout()
    return fig
