# Getting Started

## Installation

If you already have Python installed you can install *MLTE* with

```bash
$ pip install mlte-python
```
or

```bash
$ conda install mlte-python
```

If you don’t have Python yet, you might want to consider using Anaconda[LINK]. It’s the easiest way to get started. The good thing about getting this distribution is the fact that you don’t need to worry too much about separately installing any of the major packages that you’ll be using for your data analyses, like pandas, Scikit-Learn, etc.

## Subpackages
MLTE contains the following subpackages:
- **Properties**: Properties are any attribute of the trained model, the procedure used to train it (including training data), or its ability to perform inference. A property is ‘abstract’ in the sense that there may be many ways in which it might be assessed. Developers will consider priorities, tradeoffs, and weaknesses of their model in the context of the system and prioritize properties for testing. The categories and their corresponding properties are listed in the [framework](https://github.com/mlte-team/mlte-framework). 
- **Measurement**: Measurements are functions that assess phenomena related to the property of interest. For example, the total local process memory consumption is a *measurement* that measures the *property* of Training Memory Cost. 
- **Spec**: Specifications (Specs) are collections of properties and their associated measurements and bound validators. Specs help contain and organize the *MLTE* properties so that models can be easily re-evaluted. They are created by selecting the characteristics the model must exhibit to be considered acceptable. They also aid in the generation of a *MLTE* report. 
- **Report**: A *MLTE* report encapsulates all of the knowledge gained about the model and the system as a consequence of the evaluation process. The report renders as a web page and is opened automatically in an available window of the default browser. 

## Import
*MLTE* can be imported like any Python pacakge using the standard conventions. For a detailed example and use case of *MLTE* see the [user guide](user_guide.rst).

```python
from mlte.properties ... #importing from properties subpackage
from mlte.measurement ... #importing from measurement subpackage
from mlte.spec ... #importing from spec subpackage
from mlte.report ... #importing from report subpackage
```