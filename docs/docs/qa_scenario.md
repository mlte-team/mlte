# Translating Quality Attribute Scenarios into MLTE

The elicitation of QA Scenarios (QAS) to clearly define model quality requirements should guide the negotiation that takes place in System Dependent Model Testing (SDMT). After model quality requirements are documented, the steps to translate these scenarios into MLTE specifications are described below.

NOTE: This is a high-level overview. For a detailed example visit the `demo/scenario`  folder in the repository.

In the steps below, we will be focusing mostly on one of the QAS defined in the demo, which is the one for Fairness.

## Step 1 - Setup

Demo code: `requirements.ipynb`

Initialize the MLTE context to ensure the library is ready to work with the current model and defined artifact store. We will be working with a model called Oxford Flower, used to identify flower types from pictures.

```python
import os
from mlte.session import set_context, set_store

store_path = os.path.join(os.getcwd(), "store")
# Ensure we are creating the folder if it is not there.
os.makedirs(store_path, exist_ok=True) 

set_context("ns", "OxfordFlower", "0.0.1")
set_store(f"local://{store_path}")
```

## Step 2 - Specification

Define a Specification based on the defined scenario. The Specification will consist of several Properties, each associated to at least one Quality Attribute, and one or more Conditions for each property. To illustrate the process, we will focus on the Fairness property for the Oxford Flower model we are using.

### 2.1 Properties
Identify which Properties in MLTE (in the `mlte.properties` package) match the Quality Attribute of your scenarios (see section 2.3 for how they are added to the Specification).

If there are Quality Attributes that do not match any of the existing Properties, you will need to create a new Property. This is the case for one of our scenarios, the Fairness one. To add a new property, you will need to:
1. Create a new class that derives from `Property`  (from `mlte.properties.base`).
1. Create a constructor for your new class that only needs to receive one argument, `rationale`, call the constructor of the base class (`super().__init()`), and pass the following parameters as arguments: 
    1. `instance` : it has to be self 
    1. `description` : a textual description or definition of the new `Property`
    1. `rationale` : the rationale that was received as a param just needs to be passed along
1. Store this `Property` in a Python file in a location of your choosing, that can be imported to the file where you are defining the Specification.

```python
from mlte.property.base import Property

class Fairness(Property):
	def __init__(self, rationale: str):
		"""Initialize a Fairness instance."""
		super().__init__(
			instance=self,
			description="""
				Fairness refers to the absence of biases in data and model 
                inaccuracies that lead to models that treat individuals
				or groups unfavorably on the basis of inherent or acquired 
                characteristics (such as race, gender, disabilities,
				or others). For ML models, this means ensuring similar 
                model performance across specified subpopulations, groups,
				or data.
				""",
			rationale=rationale,
		)
```

### 2.2 Conditions
For each Property, identify the Conditions you want to validate for the associated scenario. This will likely come from the Response Measure / Measurement part of your QAS.

For each Condition you will need to use or select a validation method from a `Value` object. Existing Value types can be used (see package `mlte.value.types`), and validation methods from those Values can be used to create the Conditions (see section 2.3 for how they are called). However, if you need a more complex validation, or a more complex Value, you will need to create a new Value that derives from either `mlte.value.base`, or from one of the standard Value types mentioned above.

* For Conditions that are very simple, and just need to check a scalar value against a threshold, selecting a `Value` type from the types package, and calling a validation method from it will be enough, so no additional classes are needed.
* For Conditions that require more complex Values, a new Value has to be created that derives from `mlte.value.base.ValueBase`, that has an ``__init__``  method, a ``__str__``  method, a ``serialize()``  method and a ``deserialize()``  method. Besides these, you will need to add the actual validation method that creates the Condition you need. For an example of this case, see the `demo/scenairo/values/array_value.py` file for the `Array` value.
* For Conditions that are more complex than default types but do not need to store more data than one of the standard `Value` types, a new Value has to be created that derives from whatever existing Value type you need, and only a validation method has to be added. We will be doing this for our sample Fairness scenario. For this, we will create a value called `MultipleAccuracy` that will derive from the `Array` value mentioned above, and that will add one validation method to check for Fairness. More specifically, we will be storing the accuracy results for multiple groups in the array in our Value, and we want to validate that all those accuracies are above a certain threshold. Note that the threshold itself is not defined here, so this validation method can be reused as needed. 

```python
from values.array_value import Array
from mlte.spec.condition import Condition
from mlte.validation.result import Failure, Success

class MultipleAccuracy(Array):
    """An array with multiple accuracies."""

    @classmethod
    def all_accuracies_more_or_equal_than(cls, threshold: float) -> Condition:
        """Checks if the accuracy for multiple populations is fair by checking 
        if all of them are over the given threshold."""
        condition: Condition = Condition(
            "all_accuracies_more_than",
            [threshold],
            lambda value: Success(
                f"All accuracies are equal to or over threshold {threshold}"
            )
            if sum(g >= threshold for g in value.array) == len(value.array)
            else Failure(
                f"One or more accuracies are below threshold {threshold}: {value.array}"
            ),
        )
        return condition
```

### 2.3 Spec Creation

Once you have selected all Properties and Conditions that will be needed, a `Spec` can be created putting all of them together, as can be seen below.

```python
spec = Spec(properties={
    Fairness("Important check if model performs well accross different populations"): 
                {"accuracy across gardens": 
                            MultipleAccuracy.all_accuracies_more_or_equal_than(0.9)},
    Robustness("Robust against blur and noise"): 
                {"ranksums blur2x8": RankSums.p_value_greater_or_equal_to(0.05/3),
                 "ranksums blur5x8": RankSums.p_value_greater_or_equal_to(0.05/3),
                 "ranksums blur0x8": RankSums.p_value_greater_or_equal_to(0.05/3),
                 "multiple ranksums for clade2": 
                        MultipleRanksums.all_p_values_greater_or_equal_than(0.05),
                 "multiple ranksums between clade2 and 3": 
                        MultipleRanksums.all_p_values_greater_or_equal_than(0.05),
                },
    StorageCost("Critical since model will be in an embedded device"): 
                    {"model size": LocalObjectSize.value().less_than(3000)},                
    PredictingMemoryCost("Useful to evaluate resources needed when predicting"): 
                    {"predicting memory": 
                    LocalProcessMemoryConsumption.value().average_consumption_less_than(512000.0)},
    PredictingComputeCost("Useful to evaluate resources needed when predicting"): 
                    {"predicting cpu": 
                    LocalProcessCPUUtilization.value().max_utilization_less_than(30.0)},
    Interpretability("Important to understand what the model is doing"): 
                    {"image attributions": Image.ignore("Inspect the image.")},
    })
```

Note that for the `Fairness` property, we are:
* Passing a rationale string as an argument, to register why it is important in our specific model.
* Indicating we want to use the validation method `all_accuracies_more_or_equal_than` from the `MultipleAccuracy` Value we created.
* Passing the threshold value we want the accuracies to be greater than (in this case, 0.9)
* Defining an identifier for the Condition (in this case, "accuracy across gardens"). Note that this identifier will need to be used when gathering measurements for this Property, to automatically validate it later.

## Step 3 - Gathering Measurement Evidence
The next step is to gather data from measurements for each of the `Condition`s defined in the `Spec`. See `demo/scenario/evidence.ipynb` for a self-guided explanation on how to do this.

In particular, for Fairness, after loading helper code to process the data and load model results, the following code is used to store measurements related to accuracy (the method `calculate_model_performance_acc`  is defined earlier in the demo notebook, as well as `split_data`). Note that the identifier "accuracy across gardens" is used when creating the Measurement, to later link it to the `Condition` in the `Spec`.

```python
from values.multiple_accuracy import MultipleAccuracy
from mlte.measurement import ExternalMeasurement

# Evaluate accuracy, identifier has to be the same one defined in the Spec.
accuracy_measurement = ExternalMeasurement("accuracy across gardens", 
                    MultipleAccuracy, calculate_model_performance_acc)
accuracy = accuracy_measurement.evaluate(split_data[0], split_data[1])

# Inspect value
print(accuracy)

# Save to artifact store
accuracy.save(force=True)
```

## Step 4 - Validation
The final step is to validate your results, and optionally generate a report. Validation will generate a `ValidatedSpec` indicating the results of validating the `Condition`s for each Quality Attribute. See `demo/scenario/report.ipynb` for the full example, but below is the validation code:

```python
# Load the specification
spec = Spec.load()

# Add all values to the validator.
spec_validator = SpecValidator(spec)
spec_validator.add_value(MultipleAccuracy.load("accuracy across gardens.value"))
spec_validator.add_value(RankSums.load("ranksums blur2x8.value"))
spec_validator.add_value(RankSums.load("ranksums blur5x8.value"))
spec_validator.add_value(RankSums.load("ranksums blur0x8.value"))
spec_validator.add_value(MultipleRanksums.load("multiple ranksums for clade2.value"))
spec_validator.add_value(MultipleRanksums.load("multiple ranksums between clade2 and 3.value"))
spec_validator.add_value(Integer.load("model size.value"))
spec_validator.add_value(CPUStatistics.load("predicting cpu.value"))
spec_validator.add_value(MemoryStatistics.load("predicting memory.value"))
spec_validator.add_value(Image.load("image attributions.value"))

# Validate requirements and get validated details.
validated_spec = spec_validator.validate()
validated_spec.save(force=True)

# We want to see the validation results in the Notebook, regardless of them being saved.
validated_spec.print_results()
```

Note that, among other values, we are loading the result of our "accuracy across gardens" value by using that id and adding the ".value" suffix, as well as other measurement results for other Properties. The validation is then done automatically between all these measurement results and the `Spec`.

## More Information

If this guide makes you want to learn more about `MLTE`, check out our <a href="https://arxiv.org/abs/2303.01998" target="_blank">paper</a>!