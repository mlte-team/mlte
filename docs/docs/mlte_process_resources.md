# MLTE Process Resources

MLTE was created based on existing techniques and cutting-edge research for machine learning. This section gives some explanations of why the team made the choices we did for the MLTE framework and infrastructure.


## Baseline and Performance Metric Selection

### Information on Baseline Selection

* Some datasets and methods already have an accepted baseline that can be used (for instance, [PASCAL VOC](http://host.robots.ox.ac.uk/pascal/VOC/pubs/everingham10.pdf) is an object category recognition and detection benchmark).
* Classify everything as the majority (as described by Chapter 7.2 of [Hvitfeldt & Silge 2021](https://smltar.com/mlclassification.html#classnull)).
* If the model implements a task that is currently performed manually, conduct a test in which humans perform the task and use the human performance as the baseline.
  
### Information on Performance Metric Selection

The choice of metric depends on the exact nature of the system being created; following are some examples to consider from commonly used disciplines of ML.  

* Classification:
    * Receiver Operating Characteristics ([ROC](https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html?highlight=roc)) curves and the Area Under the Curve ([AUC](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html#sklearn.metrics.roc_auc_score)): Evaluation metrics for standard classification tasks. 
    * Precision Recall Curves and Area Under the Precision Recall Curve ([AUPRC](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.PrecisionRecallDisplay.html#sklearn.metrics.PrecisionRecallDisplay)): Used when there are class imbalances.
* Object Detection:
    * Average Precision ([AP](https://scikit-learn.org/stable/auto_examples/model_selection/plot_precision_recall.html?highlight=precision%20recall)) is the weighted mean of precisions achieved at each recall threshold.
    * [mAP50](https://arxiv.org/abs/2112.02814): Used when detecting multiple classes. The precision accumulated over different levels of recall under the intersection over union (IOU) threshold of 0.50. 
    * [mAP](https://arxiv.org/abs/2112.02814): Extension of mAP50 that is averaged over ten IOU thresholds.


## Resources on Machine Learning Pipelines and Processes

### ML Training Best Practices

* Ensuring that representative training and test data is available or provided for the problem at hand, and handling the data appropriately based on any associated permissions or authorities that are required.
* Splitting the data correctly for training, validation, and testing.
* Appropriately selecting a model type and then fine-tuning it. 
  
### [Ch 2 End-to-End Machine Learning](https://learning.oreilly.com/library/view/hands-on-machine-learning/9781098125967/ch02.html) from [Hands-On Machine Learning](https://learning.oreilly.com/library/view/hands-on-machine-learning/9781098125967/) by [Aurélien Géron](https://github.com/ageron)

1. Look at the big picture.
2. Get the data.
3. Explore and visualize the data to gain insights.
4. Prepare the data for Machine Learning algorithms.
5. Select a model and train it.
6. Fine-tune your model.
7. Present your solution.
8. Launch, monitor, and maintain your system.

### [A Course in Machine Learning](http://ciml.info) by [Hal Daumé III](http://hal3.name/)

- Feature engineering, tuning hyperparameters, debugging techniques: [Ch 5 Practical Issues](http://ciml.info/dl/v0_99/ciml-v0_99-ch05.pdf)
- Neural networks: [Ch 10 Neural Networks](http://ciml.info/dl/v0_99/ciml-v0_99-ch10.pdf)
- Gradient descent, feature hashing: [Ch 14 Efficient Learning](http://ciml.info/dl/v0_99/ciml-v0_99-ch14.pdf)

### [Introduction to Machine Learning with Python](https://www.oreilly.com/library/view/introduction-to-machine/9781449369880/) by [Andreas C. Müller](https://amueller.github.io) and Sarah Guido

1. Ask if machine learning can solve the problem at hand.
2. Find and obtain relevant data for the problem.
3. Examine and understand the data.
4. Build a model.
5. Make predictions.
6. Evaluate your model.  

**More ML-process related topics:**

* Preprocessing and scaling: [Ch 3 Unsupervised Learning and Preprocessing](https://learning.oreilly.com/library/view/introduction-to-machine/9781449369880/ch03.html#types-of-unsupervised-learning)
* Cross validation and grid search: [Ch 5 Model Evaluation and Improvement](https://learning.oreilly.com/library/view/introduction-to-machine/9781449369880/ch05.html)
* Machine Learning pipelines for chaining models and encapsulating a workflow: [Ch 6 Algorithm Chains and Pipelines](https://learning.oreilly.com/library/view/introduction-to-machine/9781449369880/ch06.html#algorithm-chains-and-pipelines)
  

## Generating Multiple Test Sets

If it is possible for multiple holdout test sets to be generated, using different ones for each evaluation in IMT and SDMT will produce the best results. 

However, it is often not possible for practitioners to generate , and there is research to support that substantial overfitting does not occur even if a single test set is used multiple times ([Roelofs et al. 2019](https://proceedings.neurips.cc/paper/2019/file/ee39e503b6bedf0c98c388b7e8589aca-Paper.pdf)). 

To differentiate between evaluations, we recommend ensuring good version control for models as they are the unit by which MLTE tracks evaluations.
    

## Model Property Definition

Research on model property definition.

- [Model Quality: Defining Correctness and Fit](https://ckaestne.medium.com/model-quality-defining-correctness-and-fit-a8361b857df)
- [Model Quality: Measuring Prediction Accuracy](https://ckaestne.medium.com/model-quality-measuring-prediction-accuracy-38826216ebcb)
- [Model Quality: Slicing, Capabilities, Invariant, and Other Testing Strategies](https://ckaestne.medium.com/model-quality-slicing-capabilities-invariants-and-other-testing-strategies-27e456027bd)
- [Quality Attributes of ML Components](https://ckaestne.medium.com/quality-drivers-in-architectures-for-ml-enabled-systems-836f21c44334)
- [The Tail at Scale](https://research.google/pubs/pub40801/)
- [Estimation of Energy Consumption in Machine Learning](https://www.sciencedirect.com/science/article/pii/S0743731518308773)
  

## Requirements Selection

Research on requirements selection.

- [Requirements Engineering for Machine Learning](https://arxiv.org/pdf/1908.04674.pdf)
- [Towards Guidelines for Assessing Qualities of Machine Learning Systems](https://arxiv.org/ftp/arxiv/papers/2008/2008.11007.pdf)