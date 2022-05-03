# Quick Start

## Installation

If you already have Python installed you can install *MLTE* with

```bash
$ pip install mlte-python
```
or

```bash
$ conda install mlte-python
```

If you don’t have Python yet, you might want to consider using Anaconda. It’s the easiest way to get started. The good thing about getting this distribution is the fact that you don’t need to worry too much about separately installing any of the major packages that you’ll be using for your data analyses, like pandas, Scikit-Learn, etc.

## Subpackages
MLTE contains the following subpackages:
- Properties: Properties are the characteristics or traits of a ML model or system. Developers will consider priorities, tradeoffs, and weaknesses of their model in the context of the system and prioritize properties for testing. The categories that organize properties are listed in [SDMT](https://github.com/mlte-team/a2it/blob/master/framework/1_SDMT.md). Properties in MLTE are an abstract element that are measured by measurements and validated by validators which are bound to properties. 
- Measurement: Measurements are the isntances that assesses a property. For example, the total local process memory consumptions is a *measurement* that measures the *property* of Training Memory Cost. 
- Suites: Suites are collections of properties and their associated measurements and bound validators. Suits help contain and organize the *MLTE* properties so that models can be easily re-evaluted. It also aids in the generation of the *MLTE* report. 
- Report: Report contains a number of subclasses that are returned and displayed in the automatically generated *MLTE* report. The report renders as a web page and is opened automatically in an available window of the default browser. 

## Import
*MLTE* can be imported like any Python pacakge using the standard conventions. For a detailed example and use case of *MLTE* see the [examples](https://mlte.readthedocs.io/en/latest/examples.html) page.

```python
from mlte.properties ... #importing from properties subpackage
from mlte.measurement ... #importing from measurement subpackage
from mlte.suites ... #importing from suites subpackage
from mlte.report ... #importing from report subpackage
```
