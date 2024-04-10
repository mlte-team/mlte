# MLTE Mechanics 

This section provides insight into the mechanics required to use the `MLTE` Python package. If you're looking for a more comprehensive guide that covers the framework and how to implement it using the package, see the [Using MLTE](using_mlte.md) Guide.

## Install `MLTE`
You can install `MLTE` with

```bash
$ pip install mlte-python
```
or

```bash
$ conda install mlte-python
```

## Model Testing

MLTE has two types of model testing, internal model testing (IMT) and system dependent model testing (SDMT). The mechanics are similar for both, and this section goes through an example that will allow you to work through either type of testing. 

Testing a model using `MLTE` follows this process:

1. Initialize the `MLTE` context.
2. Define a specification.
3. Collect evidence.
4. Validate results.
5. Examine findings.

## Example Scenario

The scenario used here is a hypothetical where visitors to a botanical garden are identifying flowers to learn more about them. They are helped by a machine learning (ML) model that runs on a camera they loan from the botanical garden. The model was trained on the flower category dataset ([Nilsback 2008](https://www.robots.ox.ac.uk/~vgg/data/flowers/102/)). The complete files for this example can be found in the `MLTE` repository in the 
<a href="https://github.com/mlte-team/mlte/tree/master/demo/scenarios" target="_blank">demo folder</a>.

## 1. Initialize the `MLTE` Context

One core tenet of `MLTE` is that evaluation requires evidence in the form of artifacts. These are gathered throughout the testing process, and `MLTE` contains a global context that manages the currently active session so you can collect artifacts and store them all in the same place. Initializing your context tells `MLTE` how to store your artifacts.

```python
import os
from mlte.session import set_context, set_store

# Set up the path for where we are storing artifacts
store_path = os.path.join(os.getcwd(), "store")
os.makedirs(
    store_path, exist_ok=True
)

# Initialize the context
set_context("OxfordFlower", "0.0.1")
# Set the artifact storage path
set_store(f"local://{store_path}")
```

Note that running this code merely sets the context, it does *NOT* establish a model. To do so, we have to save our first artifact. When you save an artifact, `MLTE` draws on the context you set and then creates the model, which will allow you to then view your arifacts in the MLTE user interface (UI).

## 2. Define a Specification

In `MLTE`, requirements are defined by constructing a specification (`Spec`). A `Spec` contains the requirements the completed model must meet in order to be acceptable for use in the system into which it will be integrated. This is done with the structure of properties and conditions. Properties are characteristics of the trained model, the procedure used to train it (including training data), or its ability to perform inference. Conditions are a measurement and a threshold that correspond to a particular property - they are a concrete way to evaluate a property. 

### Conditions

For this scenario, our `Spec` includes the following properties and conditions:

- Fairness - Model Impartial to Photo Location
    - The model receives a picture taken in the garden and can correctly identify the correct flowers at least 90% of the time regardless of the location where the photo was taken. 
    - Test data needs to include pictures of the flowers from the different gardens, grouped by the garden that the image was taken at and representative of the garden population they are taken from. 
    - The total accuracy of the model across each garden population should be higher or equal to 0.9.
- Robustness - Model Robust to Noise (Image Blur)
    - If the model receives a picture taken in a garden that is a bit blurry, it should still be able to successfully identify the flower.
    - Test data needs to include blurred flower images (created using ImageMagick). 
    - Robustness to blur is measured using the Wilcoxon Rank-Sum test, with significance at p-value <=0.05.
- Robustness - Model Robust to Noise (Channel Loss)
    - The model should be able to successfully identify a picture of a flower from the garden even if the device has lost one of its RGB channels.
    - Test data needs to include images with a missing channel (created by removing each of the three channels using ImageMagic).
    - Robustness to channel loss is measured using the Wilcoxon Rank-Sum test, with significance at p-value <=0.05.
- Performance on Operational Platform
    - The model needs to run on the devices loaned out by the garden centers to visitors, which are small, inexpensive devices with limited CPU power, memory, and disk space (512 MB and 128 GB, respectively). 
    - Executing the model on the devices cannot exceed 30% of maximum CPU usage to ensure reasonable response time; CPU usage will be measure using ps.
    - Memory usage at inference time will not exceed available memory of 512 MB, measured using pmap.
    - Disk usage will not exceed available disk space of 128 GB, measured by adding the size of each file in the path for the model code.
- Interpretability - Understanding Model Results
    - The application that runs on the loaned camera should indicate the main features that were used to recognize the flower as part of the educational experience. 
    - The app will display the image highlighting the most informative features in flower identification, in addition to the flower name. 
    - The model needs to return evidence with each inference showing the pixels that were most informative in the classification decision (done using a heat map implementing the Integrated Gradients algorithm).

### Building the `Spec`

Now that we've defined the properties and conditions for this scenario, we can build the `Spec` in code. 

*NOTE:* to run this code, you'll need to download the supporting files from the <a href="https://github.com/mlte-team/mlte/tree/master/demo/scenarios" target="_blank">demo folder</a> in the `MLTE` repository as it uses functions from those files.

```python
from mlte.spec.spec import Spec

# Import the Properties for this scenario
from mlte.property.costs.storage_cost import StorageCost
from properties.fairness import Fairness
from properties.robustness import Robustness
from properties.interpretability import Interpretability
from properties.predicting_memory_cost import PredictingMemoryCost
from properties.predicting_compute_cost import PredictingComputeCost

# Import Value types for each condition
from mlte.measurement.storage import LocalObjectSize
from mlte.measurement.cpu import LocalProcessCPUUtilization
from mlte.measurement.memory import LocalProcessMemoryConsumption
from mlte.value.types.image import Image
from values.multiple_accuracy import MultipleAccuracy
from values.ranksums import RankSums
from values.multiple_ranksums import MultipleRanksums

# Define the Spec (Note that the Robustness Property contains conditions for both Robustness requirements)
spec = Spec(
    properties={
        Fairness(
            "Important check if model performs well accross different populations"
        ): {
            "accuracy across gardens": MultipleAccuracy.all_accuracies_more_or_equal_than(
                0.9
            )
        },
        Robustness("Robust against blur and noise"): {
            "ranksums blur2x8": RankSums.p_value_greater_or_equal_to(0.05 / 3),
            "ranksums blur5x8": RankSums.p_value_greater_or_equal_to(0.05 / 3),
            "ranksums blur0x8": RankSums.p_value_greater_or_equal_to(0.05 / 3),
            "multiple ranksums for clade2": MultipleRanksums.all_p_values_greater_or_equal_than(
                0.05
            ),
            "multiple ranksums between clade2 and 3": MultipleRanksums.all_p_values_greater_or_equal_than(
                0.05
            ),
        },
        StorageCost("Critical since model will be in an embedded device"): {
            "model size": LocalObjectSize.value().less_than(3000)
        },
        PredictingMemoryCost(
            "Useful to evaluate resources needed when predicting"
        ): {
            "predicting memory": LocalProcessMemoryConsumption.value().average_consumption_less_than(
                512000.0
            )
        },
        PredictingComputeCost(
            "Useful to evaluate resources needed when predicting"
        ): {
            "predicting cpu": LocalProcessCPUUtilization.value().max_utilization_less_than(
                30.0
            )
        },
        Interpretability("Important to understand what the model is doing"): {
            "image attributions": Image.ignore("Inspect the image.")
        },
    }
)
spec.save(parents=True, force=True)
```

### Run the `MLTE` UI

Once the context is initialized and you've created your first artifact, you can view them in the front end if you choose. To use the UI, you'll need to run both the front end and the back end using two shells.

To run the front end:

```bash
$ mlte ui
```

To run the back end: 

```bash
$ mlte store --backend-uri fs://store --allowed-origins http://localhost:8000
```

This allows the front end to be able to communicate with the store by allowing the requisite origin. The front end is hosted at `http://localhost:8000`.

Once you are running both the front and back ends in two shells, you can go to the hosted address to view the `MLTE` UI homepage. You should see the model you created on the lefthand side, and you should see the `Spec` we created above under the Specifications section of the artifacts.

## 3. Collect Evidence

After defining a `Spec`, `MLTE` mandates that you collect evidence to attest to the fact that the model realized the specified properties.

We define and instantiate `Measurements` to generate this evidence. Each individual piece of evidence is a `Value`. Once `Value`s are produced, persist them to the artifact store to maintain your set of evidence.

Preliminaries to set up for collecting evidence.

```python
from pathlib import Path

# Delineate the path at which datasets are stored
DATASETS_DIR = Path.cwd() / "data"

# Set where the model files are stored.
MODELS_DIR = Path.cwd() / "model"

# The path at which media is stored
MEDIA_DIR = Path.cwd() / "media"
os.makedirs(MEDIA_DIR, exist_ok=True)
```

Download the model that will be used (note that you'll need to get the requisite files from the <a href="https://github.com/mlte-team/mlte/tree/master/demo/scenarios" target="_blank">demo folder</a> in the `MLTE` repository).
 
```bash
!sh get_model.sh
```

Functions that facilitate the code for this scenario (corresponding files can be found in the <a href="https://github.com/mlte-team/mlte/tree/master/demo/scenarios" target="_blank">demo folder</a> in the `MLTE` repository), along with data preparation.

```python
import garden
import numpy as np

def load_data(data_folder: str):
    """Loads all garden data results and taxonomy categories."""
    df_results = garden.load_base_results(data_folder)
    df_results.head()

    # Load the taxonomic data and merge with results.
    df_info = garden.load_taxonomy(data_folder)
    df_results.rename(columns={"label": "Label"}, inplace=True)
    df_all = garden.merge_taxonomy_with_results(df_results, df_info)

    return df_info, df_all


def split_data(df_info, df_all):
    """Splits the data into 3 different populations to evaluate them."""
    df_gardenpop = df_info.copy()
    df_gardenpop["Population1"] = (
        np.around(
            np.random.dirichlet(np.ones(df_gardenpop.shape[0]), size=1)[0],
            decimals=3,
        )
        * 1000
    ).astype(int)
    df_gardenpop["Population2"] = (
        np.around(
            np.random.dirichlet(np.ones(df_gardenpop.shape[0]), size=1)[0],
            decimals=3,
        )
        * 1000
    ).astype(int)
    df_gardenpop["Population3"] = (
        np.around(
            np.random.dirichlet(np.ones(df_gardenpop.shape[0]), size=1)[0],
            decimals=3,
        )
        * 1000
    ).astype(int)
    df_gardenpop

    # Build populations from test data set that match the garden compositions
    from random import choices

    # Build 3 gardens with populations of 1000
    pop_names = ["Population1", "Population2", "Population3"]
    gardenpops = np.zeros((3, 1000), int)
    gardenmems = np.zeros((3, 1000), int)

    for j in range(1000):
        for i in range(len(df_gardenpop)):
            my_flower = df_gardenpop.iloc[i]["Common Name"]

            for g in range(3):
                n_choices = df_gardenpop.iloc[i][pop_names[g]]
                my_choices = df_all[df_all["Common Name"] == my_flower][
                    "model correct"
                ].to_list()
                my_selection = choices(my_choices, k=n_choices)

                gardenpops[g][j] += sum(my_selection)
                gardenmems[g][j] += len(my_selection)

    gardenpops

    return gardenpops, gardenmems


def calculate_model_performance_acc(gardenpops, gardenmems):
    """Get accucray of models across the garden populations."""
    gardenacc = np.zeros((3, 1000), float)
    for i in range(1000):
        for g in range(3):
            gardenacc[g][i] = gardenpops[g][i] / gardenmems[g][i]
    gardenacc

    model_performance_acc = []
    for g in range(3):
        avg = round(np.average(gardenacc[g][:]), 3)
        std = round(np.std(gardenacc[g][:]), 3)
        min = round(np.amin(gardenacc[g][:]), 3)
        max = round(np.amax(gardenacc[g][:]), 3)
        model_performance_acc.append(round(avg, 3))

        print("%1d %1.3f %1.3f %1.3f %1.3f" % (g, avg, std, min, max))

    return model_performance_acc

# Prepare the data. Here we use CSV files 
# containing the results of an already executed 
# run of the model (rather than running it again).
data = load_data(DATASETS_DIR)
split_data = split_data(data[0], data[1])
```

### Accuracy Measurements

To collect evidence of model accuracy, we wrap the output from `accuracy_score` with a custom `Result` type to handle the output of a third-party library that is not supported by a `MLTE` builtin.

```python
from values.multiple_accuracy import MultipleAccuracy
from mlte.measurement import ExternalMeasurement

# Evaluate accuracy in accordance with condition laid out in the Spec
accuracy_measurement = ExternalMeasurement(
    "accuracy across gardens", MultipleAccuracy, calculate_model_performance_acc
)
accuracy = accuracy_measurement.evaluate(split_data[0], split_data[1])

# Inspect value
print(accuracy)

# Save to artifact store
accuracy.save(force=True)
```

### Robustness Measurements

Again we set up some general functions to facilitate the robustness measurements as well as prepare the data needed.

```python
import pandas as pd

def calculate_base_accuracy(df_results: pd.DataFrame) -> pd.DataFrame:
    # Calculate the base model accuracy result for each data label
    df_pos = (
        df_results[df_results["model correct"] == True].groupby("label").count()
    )
    df_pos.drop(columns=["prediced_label"], inplace=True)
    df_neg = (
        df_results[df_results["model correct"] == False]
        .groupby("label")
        .count()
    )
    df_neg.drop(columns=["prediced_label"], inplace=True)
    df_neg.rename(columns={"model correct": "model incorrect"}, inplace=True)
    df_res = df_pos.merge(
        df_neg, right_on="label", left_on="label", how="outer"
    )
    df_res.fillna(0, inplace=True)
    df_res["model acc"] = df_res["model correct"] / (
        df_res["model correct"] + df_res["model incorrect"]
    )
    df_res["count"] = df_res["model correct"] + df_res["model incorrect"]
    df_res.drop(columns=["model correct", "model incorrect"], inplace=True)
    df_res.head()

    return df_res


def calculate_accuracy_per_set(
    data_folder: str, df_results: pd.DataFrame, df_res: pd.DataFrame
) -> pd.DataFrame:
    # Calculate the model accuracy by data label for each blurred data set
    base_filename = "FlowerModelv1_TestSetResults"
    ext_filename = ".csv"
    set_filename = ["_blur2x8", "_blur5x8", "_blur0x8", "_noR", "_noG", "_noB"]

    col_root = "model acc"

    for fs in set_filename:
        filename = os.path.join(data_folder, base_filename + fs + ext_filename)
        colname = col_root + fs

        df_temp = pd.read_csv(filename)
        df_temp.drop(columns=["Unnamed: 0"], inplace=True)

        df_pos = (
            df_temp[df_temp["model correct"] == True].groupby("label").count()
        )
        df_pos.drop(columns=["prediced_label"], inplace=True)
        df_neg = (
            df_results[df_results["model correct"] == False]
            .groupby("label")
            .count()
        )
        df_neg.drop(columns=["prediced_label"], inplace=True)
        df_neg.rename(
            columns={"model correct": "model incorrect"}, inplace=True
        )
        df_res2 = df_pos.merge(
            df_neg, right_on="label", left_on="label", how="outer"
        )
        df_res2.fillna(0, inplace=True)

        df_res2[colname] = df_res2["model correct"] / (
            df_res2["model correct"] + df_res2["model incorrect"]
        )
        df_res2.drop(columns=["model correct", "model incorrect"], inplace=True)

        df_res = df_res.merge(
            df_res2, right_on="label", left_on="label", how="outer"
        )

    df_res.head()
    return df_res


def print_model_accuracy(df_res: pd.DataFrame, key: str, name: str):
    model_acc = sum(df_res[key] * df_res["count"]) / sum(df_res["count"])
    print(name, model_acc)
```

```python
# Prepare all data. Same as above, we use CSV files that
# contain results of a previous execution of the model.
df_results = garden.load_base_results(DATASETS_DIR)
df_res = calculate_base_accuracy(df_results)
df_res = calculate_accuracy_per_set(DATASETS_DIR, df_results, df_res)
df_info = garden.load_taxonomy(DATASETS_DIR)
df_all = garden.merge_taxonomy_with_results(df_res, df_info, "label", "Label")

# Fill in missing model accuracy data
df_all["model acc_noR"].fillna(0, inplace=True)
df_all["model acc_noG"].fillna(0, inplace=True)
df_all["model acc_noB"].fillna(0, inplace=True)
```

Now we execute the measurements, starting with model accuracy across blurs.

```python
# View changes in model accuracy with blurring
print_model_accuracy(df_res, "model acc", "base model accuracy")
print_model_accuracy(
    df_res, "model acc_blur2x8", "model accuracy with 2x8 blur"
)
print_model_accuracy(
    df_res, "model acc_blur5x8", "model accuracy with 5x8 blur"
)
print_model_accuracy(
    df_res, "model acc_blur0x8", "model accuracy with 0x8 blur"
```

Now we measure the ranksums (p-value) for all blur cases, using scipy.stats.ranksums and the `ExternalMeasurement` wrapper from `MLTE`.

```python
import scipy.stats

from values.ranksums import RankSums
from mlte.measurement import ExternalMeasurement

my_blur = ["2x8", "5x8", "0x8"]
for i in range(len(my_blur)):
    # Define measurements
    ranksum_measurement = ExternalMeasurement(
        f"ranksums blur{my_blur[i]}", RankSums, scipy.stats.ranksums
    )

    # Evaluate
    ranksum: RankSums = ranksum_measurement.evaluate(
        df_res["model acc"], df_res[f"model acc_blur{my_blur[i]}"]
    )

    # Inspect values
    print(ranksum)

    # Save to artifact store
    ranksum.save(force=True)
```

Now we have to determing if the accuracy on blurry photos is equal across the flower population groups. To start, we will check the effects of blurring on one flower population (called Clade 2 - a clade is a natural group of organisms that share a common ancestor within an evolutionary tree).

```python
from typing import List
from values.multiple_ranksums import MultipleRanksums

# Using the initial result, blur columns to anaylze effect of blur
df_all["delta_2x8"] = df_all["model acc"] - df_all["model acc_blur2x8"]
df_all["delta_5x8"] = df_all["model acc"] - df_all["model acc_blur5x8"]
df_all["delta_0x8"] = df_all["model acc"] - df_all["model acc_blur0x8"]

pops = df_all["Clade2"].unique().tolist()
blurs = [
    "delta_2x8",
    "delta_5x8",
    "delta_0x8",
]

ranksums: List = []
for i in range(len(blurs)):
    for pop1 in pops:
        for pop2 in pops:
            ranksum_measurement = ExternalMeasurement(
                f"ranksums clade2 {pop1}-{pop2} blur{blurs[i]}",
                RankSums,
                scipy.stats.ranksums,
            )
            ranksum: RankSums = ranksum_measurement.evaluate(
                df_all[df_all["Clade2"] == pop1][blurs[i]],
                df_all[df_all["Clade2"] == pop2][blurs[i]],
            )
            print(f"blur {blurs[i]}: {ranksum}")
            ranksums.append({ranksum.identifier: ranksum.array})

multiple_ranksums_meas = ExternalMeasurement(
    f"multiple ranksums for clade2", MultipleRanksums, lambda x: x
)
multiple_ranksums: MultipleRanksums = multiple_ranksums_meas.evaluate(ranksums)
multiple_ranksums.num_pops = len(pops)
multiple_ranksums.save(force=True)
```

We continue to determe if the accuracy on blurry photos is equal across the flower population groups by looking at the next group, Clade 3, in comparison with Clade 2. 

```python
df_now = (
    df_all[["Clade2", "Clade 3"]]
    .copy()
    .groupby(["Clade2", "Clade 3"])
    .count()
    .reset_index()
)
ps1 = df_now["Clade2"].to_list()
ps2 = df_now["Clade 3"].to_list()
print(df_now)

ranksums: List = []
for k in range(len(blurs)):
    print("\n", blurs[k])
    for i in range(len(ps1)):
        p1c1 = ps1[i]
        p1c2 = ps2[i]
        for j in range(len(ps1)):
            p2c1 = ps1[j]
            p2c2 = ps2[j]
            if (
                len(
                    df_all[
                        (df_all["Clade2"] == p1c1) & (df_all["Clade 3"] == p2c2)
                    ][blurs[k]]
                )
                > 0
                | len(
                    df_all[
                        (df_all["Clade2"] == p2c1) & (df_all["Clade 3"] == p2c2)
                    ][blurs[k]]
                )
                > 0
            ):
                ranksum_measurement = ExternalMeasurement(
                    f"ranksums {p1c1}-{p2c2} - {p2c1}-{p2c2} blur{blurs[k]}",
                    RankSums,
                    scipy.stats.ranksums,
                )
                ranksum: RankSums = ranksum_measurement.evaluate(
                    df_all[
                        (df_all["Clade2"] == p1c1) & (df_all["Clade 3"] == p2c2)
                    ][blurs[k]],
                    df_all[
                        (df_all["Clade2"] == p2c1) & (df_all["Clade 3"] == p2c2)
                    ][blurs[k]],
                )
                ranksums.append({ranksum.identifier: ranksum.array})

multiple_ranksums_meas = ExternalMeasurement(
    f"multiple ranksums between clade2 and 3", MultipleRanksums, lambda x: x
)
multiple_ranksums: MultipleRanksums = multiple_ranksums_meas.evaluate(ranksums)
multiple_ranksums.num_pops = len(ps1)
multiple_ranksums.save(force=True)
```

### Performance Measurements

Next we collect stored, CPU, and memory usage data. Doing so requires running the model as this property is associated with that process.

*NOTE 1: The version of tensorflow used here requires Python 3.9 or higher.*

*NOTE 2: Files can be found in the <a href="https://github.com/mlte-team/mlte/tree/master/demo/scenarios" target="_blank">demo folder</a> of the `MLTE` repository.*

Set up the external script that will load and run the model for inference/prediction.

```python
script = Path.cwd() / "model_predict.py"
args = [
    "--images",
    DATASETS_DIR,
    "--model",
    MODELS_DIR / "model_f3_a.json",
    "--weights",
    MODELS_DIR / "model_f_a.h5",
]
```

Import and execute storage measurements.

```python
from mlte.measurement.storage import LocalObjectSize
from mlte.value.types.integer import Integer

store_measurement = LocalObjectSize("model size")
size: Integer = store_measurement.evaluate(MODELS_DIR)
print(size)
size.save(force=True)
```

Import and execute CPU measurements.

```python
from mlte.measurement import ProcessMeasurement
from mlte.measurement.cpu import LocalProcessCPUUtilization, CPUStatistics

cpu_measurement = LocalProcessCPUUtilization("predicting cpu")
cpu_stats: CPUStatistics = cpu_measurement.evaluate(
    ProcessMeasurement.start_script(script, args)
)
print(cpu_stats)
cpu_stats.save(force=True)
```

Import and execute memory measurements.

```python
from mlte.measurement.memory import (
    LocalProcessMemoryConsumption,
    MemoryStatistics,
)

mem_measurement = LocalProcessMemoryConsumption("predicting memory")
mem_stats: MemoryStatistics = mem_measurement.evaluate(
    ProcessMeasurement.start_script(script, args)
)
print(mem_stats)
mem_stats.save(force=True)
```

### Interpretability Measurements

Now we can gather data about the interpretability of the model; to start, we set up the model and weights files.

```python
model_filename = (
    MODELS_DIR / "model_f3_a.json"
)  # The json file of the model to load
weights_filename = MODELS_DIR / "model_f_a.h5"  # The weights file for the model
```

Load the model, and then load and display the image.

```python
from model_analysis import *

loaded_model = load_model(model_filename, weights_filename)

# Flower image to use (public domain, from: https://commons.wikimedia.org/wiki/File:Beautiful_white_flower_in_garden.jpg)
flower_img = "flower3.jpg" 
flower_idx = (
    42  # Classifier index of associated flower (see OxfordFlower102Labels.csv)
)

im = read_image(os.path.join(DATASETS_DIR, flower_img))

plt.imshow(im)
plt.axis("off")
plt.show()
```

Predict.

```python
predictions = run_model(im, loaded_model)

baseline, alphas = generate_baseline_and_alphas()
interpolated_images = interpolate_images(
    baseline=baseline, image=im, alphas=alphas
)
```

Display the image.

```python
fig = plt.figure(figsize=(20, 20))

i = 0
for alpha, image in zip(alphas[0::10], interpolated_images[0::10]):
    i += 1
    plt.subplot(1, len(alphas[0::10]), i)
    plt.title(f"alpha: {alpha:.1f}")
    plt.imshow(image)
    plt.axis("off")

plt.tight_layout()
```

Calculate and display image attributions.

```python
path_gradients = compute_gradients(
    loaded_model=loaded_model,
    images=interpolated_images,
    target_class_idx=flower_idx,
)
print(path_gradients.shape)

ig = integral_approximation(gradients=path_gradients)
print(ig.shape)
ig_attributions = integrated_gradients(
    baseline=baseline,
    image=im,
    target_class_idx=flower_idx,
    loaded_model=loaded_model,
    m_steps=240,
)
print(ig_attributions.shape)

fig = plot_img_attributions(
    image=im,
    baseline=baseline,
    target_class_idx=flower_idx,
    loaded_model=loaded_model,
    m_steps=240,
    cmap=plt.cm.inferno,
    overlay_alpha=0.4,
)

plt.savefig(MEDIA_DIR / "attributions.png")
```

Finally, save the image attributions to the artifact store.

```python
from mlte.measurement import ExternalMeasurement
from mlte.value.types.image import Image

# Save to MLTE store.
img_collector = ExternalMeasurement("image attributions", Image)
img = img_collector.ingest(MEDIA_DIR / "attributions.png")
img.save(force=True)
```

## 4. Validate Results

After collecting evidence, `MLTE` requires that you confirm that your evidence proves that the model meets the conditions stipulated in the `Spec`. `MLTE` does so by validating the metrics reflected by the evidence collected with a `SpecValidator`. This will then generate a  `ValidatedSpec` which contains the results of whether or not your evidence meets your specified thresholds.

*NOTE: if you are doing this in a new session (separate from the past steps as is done in the <a href="https://github.com/mlte-team/mlte/tree/master/demo/scenarios" target="_blank">demo folder</a>), you will need to re-initialize the `MLTE` context.*

```python
from mlte.spec.spec import Spec
from mlte.validation.spec_validator import SpecValidator
from mlte.value.artifact import Value

# Load the specification
spec = Spec.load()

# Add all values to the validator
spec_validator = SpecValidator(spec)
spec_validator.add_values(Value.load_all())

# Validate requirements and get validated details.
validated_spec = spec_validator.validate()
validated_spec.save(force=True)

# Display validation results
validated_spec.print_results()
```

Once they are displayed, we can examine the validation results. One highlight is the significant difference between the model detecting images with no blur and images with a blur of 0x8. We see a drop in model accuracy with this maximum increased blur (0x8), but the model accuracy does not fall substantially for lesser levels of blur.

## 5. Generate a Report

After validating results, `MLTE` allows you to generate a report so you can communicate your evaluation findings. The report can be generated as seen below, or you can use the front end to do so.

```python
from mlte.model.shared import (
    ProblemType,
    GoalDescriptor,
    MetricDescriptor,
    ModelProductionDescriptor,
    ModelInterfaceDescriptor,
    ModelInputDescriptor,
    ModelOutputDescriptor,
    ModelResourcesDescriptor,
    RiskDescriptor,
    DataDescriptor,
    DataClassification,
    FieldDescriptor,
    LabelDescriptor,
)
from mlte.report.artifact import (
    Report,
    SummaryDescriptor,
    PerformanceDesciptor,
    IntendedUseDescriptor,
    CommentDescriptor,
    QuantitiveAnalysisDescriptor,
)

report = Report(
    summary=SummaryDescriptor(
        problem_type=ProblemType.CLASSIFICATION, task="Flower classification"
    ),
    performance=PerformanceDesciptor(
        goals=[
            GoalDescriptor(
                description="The model should perform well.",
                metrics=[
                    MetricDescriptor(
                        description="accuracy",
                        baseline="Better than random chance.",
                    )
                ],
            )
        ]
    ),
    intended_use=IntendedUseDescriptor(
        usage_context="A handheld flower identification device.",
        production_requirements=ModelProductionDescriptor(
            deployment_platform="local server",
            capability_deployment_mechanism="API",
            interface=ModelInterfaceDescriptor(
                input=ModelInputDescriptor(description="Vector[150]"),
                output=ModelOutputDescriptor(description="Vector[3]"),
            ),
            resources=ModelResourcesDescriptor(
                cpu="1", gpu="0", memory="6MiB", storage="2KiB"
            ),
        ),
    ),
    risks=RiskDescriptor(
        fp="The wrong type of flower is identified.",
        fn="The flower is not identified.",
        other="N/A",
    ),
    data=[
        DataDescriptor(
            description="Flower dataset.",
            classification=DataClassification.UNCLASSIFIED,
            access="None",
            labeling_method="by hand",
            fields=[
                FieldDescriptor(
                    name="Sepal length",
                    description="The length of the sepal.",
                    type="float",
                    expected_values="N/A",
                    missing_values="N/A",
                    special_values="N/A",
                )
            ],
            labels=[
                LabelDescriptor(description="Dahlia", percentage=30.0),
                LabelDescriptor(description="Sunflower", percentage=30.0),
                LabelDescriptor(description="Azalea", percentage=40.0),
            ],
            policies="N/A",
            rights="N/A",
            source="https://www.robots.ox.ac.uk/~vgg/data/flowers/102/",
        )
    ],
    comments=[
        CommentDescriptor(
            content="This model should not be used for nefarious purposes."
        )
    ],
    quantitative_analysis=QuantitiveAnalysisDescriptor(
        content="Insert graph here."
    ),
    validated_spec_id=validated_spec.identifier,
)

report.save(force=True, parents=True)
```

------
All files that correspond to this example can be found in the <a href="https://github.com/mlte-team/mlte/tree/master/demo/scenarios" target="_blank">demo folder</a> of the `MLTE` repository.

If you're looking for a more comprehensive guide that covers the framework and how to implement it using the package, see the [Using MLTE](using_mlte.md) Guide.