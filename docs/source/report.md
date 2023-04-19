# Generating a Report

## Define/Persist a Binding
In MLTE, a Binding associates individual results with the properties to which they attest. This ensures that all stakeholders gain a concrete understanding of how the model performs with respect to the specific requirements that were defined at the beginning of the evaluation process. See below for an example of defining and persisting a binding.

```Python
from mlte.binding import Binding

binding = Binding(
    {
        "TaskEfficacy": [
            "accuracy",
            "confusion matrix",
            "class distribution"
        ],
        "StorageCost": [
            "model size"
        ],
        "TrainingComputeCost": [
            "training cpu"
        ],
        "TrainingMemoryCost": [
            "training memory"
        ]
    }
)

# Persist the binding
binding.save()
```

## Load a Specification
In MLTE, loading a specification is simple but requires the proper context to be set up. 

```Python
# Set up the MLTE context
import mlte

store_path = os.path.join(os.getcwd(), "store")

mlte.set_model("IrisClassifier", "0.0.1")
mlte.set_artifact_store_uri(f"local://{store_path}")

# Import necessary modules
from mlte.spec import Spec, BoundSpec

# Load the specification
spec = Spec.load()
```

## Validate a Result
Once a Binding has been defined, users can load previously generated results and then validate them by invoking type-specific Validator methods. This also requires the context to be set as it is in the above example.

```Python
from mlte.measurement.result import Integer

model_size: Integer = Integer.load("model size")
model_size = model_size.less_than(3000)

# Results support introspection
print(model_size)
```

## Bind Validated Results to a Specification
Once validated, users can bind their validated Results to a specification using their corresponding Properties. 

```Python
# Bind results to properties, according to Binding
from mlte.spec import Spec, BoundSpec
from mlte.measurement.result import Real, Integer
from mlte.measurement.memory import MemoryStatistics

bound_spec: BoundSpec = spec.bind(binding, [
    model_size,
    cpu_utilization,
    memory_consumption,
    accuracy,
    confusion_matrix,
    class_distribution
])

# BoundSpec also supports persistence
bound_spec.save()
```

## Write a Report
The final step of MLTE is the generation of a report to communicate the results of model evaluation. A report encapsulates all of the knowledge gained about the model and the system as a consequence of the evaluation process. Report production ensures that teams have a method through which they can both examine and display the results of their work. See below for an example of writing a report.

```Python
import time
from mlte.report import Report, Dataset, User, UseCase, Limitation

def unix_timestamp() -> str:
    return f"{int(time.time())}"

def build_report() -> Report:
    report = Report()
    report.metadata.project_name = "IrisClassificationProject"
    report.metadata.authors = ["Kyle Dotterrer", "Kate Maffey"]
    report.metadata.source_url = "https://github.com/mlte-team"
    report.metadata.artifact_url = "https://github.com/mlte-team"
    report.metadata.timestamp = unix_timestamp()

    report.model_details.name = "IrisClassifier"
    report.model_details.overview = "A model that distinguishes among three (3) types of irises."
    report.model_details.documentation = "This is a simple model that can distinguish between the setosa, versicolour, and virginica species of Iris based on physical characteristics."

    report.model_specification.domain = "Classification"
    report.model_specification.architecture = "Decision Tree"
    report.model_specification.input = "Vector[4]"
    report.model_specification.output = "Binary"
    report.model_specification.data = [
        Dataset("Dataset0", "https://github.com/mlte-team", "This is one training dataset."),
        Dataset("Dataset1", "https://github.com/mlte-team", "This is the other one we used."),
    ]

    report.considerations.users = [
        User("Botanist", "A professional botanist."),
        User("Explorer", "A weekend-warrior outdoor explorer."),
    ]
    report.considerations.use_cases = [
        UseCase("Personal Edification", "Quench your curiosity: what species of iris IS that? Wonder no longer.")
    ]
    report.considerations.limitations = [
        Limitation(
            "Low Training Data Volume",
            """
            This model was trained on a low volume of training data.
            """,
        ),
    ]
    return report
```

## Persist/View a Report
Persisting and viewing reports are simple; once the report is saved, it can be opened in any browser and will be rendered like a webpage. See example below.

```Python
from mlte.report import render

# Build the base report
report = build_report()
# Attach the bound specification
report.spec = bound_spec

# Save the report as an HTML document
report.to_html(REPORTS_DIR / "report.html", local=True)
```