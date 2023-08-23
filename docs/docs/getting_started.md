# Getting Started

Or, how to set up the MLTE infrastructure.

## Introduction

MLTE is a framework (a process to follow) and an infrastructure (a Python package) for machine learning model and system evaluation. This section focuses on setting up the infrastructure, which is an integral part of following the MLTE [framework](mlte_framework.md).

## Installation

If you already have Python installed you can install *MLTE* with

```bash
$ pip install mlte-python
```
or

```bash
$ conda install mlte-python
```
If you are new to Python and haven't installed it, we recommend starting with [Python for Beginners](https://www.python.org/about/gettingstarted/).

## Subpackages

MLTE contains the following subpackages:

- **Properties**: Properties are any attribute of the trained model, the procedure used to train it (including training data), or its ability to perform inference. A property is ‘abstract’ in the sense that there may be many ways in which it might be assessed. Developers will consider priorities, tradeoffs, and weaknesses of their model in the context of the system and prioritize properties for testing.  

- **Measurement**: Measurements are functions that assess phenomena related to the property of interest. For example, the total local process memory consumption is a *measurement* that measures the *property* of Training Memory Cost. 

- **Spec**: Specifications (Specs) are collections of properties and their associated measurements. Specs help organize the *MLTE* properties so that models can be easily re-evaluted. They are created by selecting the characteristics the model must exhibit to be considered acceptable. 

- **Report**: A *MLTE* report encapsulates all of the knowledge gained about the model and the system as a consequence of the evaluation process. The report renders as a web page and is opened automatically in an available window of the default browser. 


## Import

*MLTE* can be imported like any Python pacakge using the standard conventions.

```python
from mlte.properties ... #importing from properties subpackage
from mlte.measurement ... #importing from measurement subpackage
from mlte.spec ... #importing from spec subpackage
from mlte.report ... #importing from report subpackage
```

## Next Steps

Once you're set up, head over to the next how-to guide to start working through the MLTE process [content coming soon!].