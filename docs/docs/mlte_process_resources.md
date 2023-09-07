# MLTE Process Resources

`MLTE` was created based on existing techniques and cutting-edge research for machine learning. This section gives some explanations of why the team made the choices we did for the `MLTE` framework and infrastructure.


## Baseline and Performance Metric Selection

### Information on Baseline Selection

* Some datasets and methods already have an accepted baseline that can be used (for instance, <a href="http://host.robots.ox.ac.uk/pascal/VOC/pubs/everingham10.pdf" target="_blank">PASCAL VOC</a> is an object category recognition and detection benchmark).
* Classify everything as the majority (as described by Chapter 7.2 of <a href="https://smltar.com/mlclassification.html#classnull" target="_blank">Hvitfeldt & Silge 2021</a>).
* If the model implements a task that is currently performed manually, conduct a test in which humans perform the task and use the human performance as the baseline.
  
### Information on Performance Metric Selection

The choice of metric depends on the exact nature of the system being created; following are some examples to consider from commonly used disciplines of ML.  

* Classification:
    * Receiver Operating Characteristics (<a href="https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc.html?highlight=roc" target="_blank">ROC</a>) curves and the Area Under the Curve (<a href="https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_auc_score.html#sklearn.metrics.roc_auc_score" target="_blank">AUC</a>): Evaluation metrics for standard classification tasks. 
    * Precision Recall Curves and Area Under the Precision Recall Curve (<a href="https://scikit-learn.org/stable/modules/generated/sklearn.metrics.PrecisionRecallDisplay.html#sklearn.metrics.PrecisionRecallDisplay" target="_blank">AUPRC</a>): Used when there are class imbalances.
* Object Detection:
    * Average Precision (<a href="https://scikit-learn.org/stable/auto_examples/model_selection/plot_precision_recall.html?highlight=precision%20recall" target="_blank">AP</a>) is the weighted mean of precisions achieved at each recall threshold.
    * <a href="https://arxiv.org/abs/2112.02814" target="_blank">mAP50</a>: Used when detecting multiple classes. mAP50 is the precision accumulated over different levels of recall under the intersection over union (IOU) threshold of 0.50 (commonly used on the PASCAL VOC benchmark).
    * <a href="https://arxiv.org/abs/2112.02814" target="_blank">mAP</a>: Extension of mAP50 that is averaged over ten IOU thresholds {0.5 : 0.05 : 0.95}, and is commonly used on the Microsoft Common Objects in Context (MS COCO) <a href="https://arxiv.org/pdf/1405.0312v3.pdf" target="_blank">benchmark</a>.

## Resources on Machine Learning Pipelines and Processes

### ML Training Best Practices

* Ensuring that representative training and test data is available or provided for the problem at hand, and handling the data appropriately based on any associated permissions or authorities that are required.
* Splitting the data correctly for training, validation, and testing.
* Appropriately selecting a model type and then fine-tuning it. 
  
### <a href="https://learning.oreilly.com/library/view/hands-on-machine-learning/9781098125967/ch02.html" target="_blank">Ch 2 End-to-End Machine Learning</a> from <a href="https://learning.oreilly.com/library/view/hands-on-machine-learning/9781098125967/" target="_blank">Hands-On Machine Learning</a> by <a href="https://github.com/ageron" target="_blank">Aurélien Géron</a>

1. Look at the big picture.
2. Get the data.
3. Explore and visualize the data to gain insights.
4. Prepare the data for Machine Learning algorithms.
5. Select a model and train it.
6. Fine-tune your model.
7. Present your solution.
8. Launch, monitor, and maintain your system.

### <a href="http://ciml.info" target="_blank">A Course in Machine Learning</a> by <a href="http://hal3.name/" target="_blank">Hal Daumé III</a>

- Feature engineering, tuning hyperparameters, debugging techniques: <a href="http://ciml.info/dl/v0_99/ciml-v0_99-ch05.pdf" target="_blank">Ch 5 Practical Issues</a>
- Neural networks: <a href="http://ciml.info/dl/v0_99/ciml-v0_99-ch10.pdf" target="_blank">Ch 10 Neural Networks</a>
- Gradient descent, feature hashing: <a href="http://ciml.info/dl/v0_99/ciml-v0_99-ch14.pdf" target="_blank">Ch 14 Efficient Learning</a>

### <a href="https://www.oreilly.com/library/view/introduction-to-machine/9781449369880/" target="_blank">Introduction to Machine Learning with Python</a> by <a href="https://amueller.github.io" target="_blank">Andreas C. Müller</a> and Sarah Guido

1. Ask if machine learning can solve the problem at hand.
2. Find and obtain relevant data for the problem.
3. Examine and understand the data.
4. Build a model.
5. Make predictions.
6. Evaluate your model.  

**More ML-process related topics:**

* Preprocessing and scaling: <a href="https://learning.oreilly.com/library/view/introduction-to-machine/9781449369880/ch03.html#types-of-unsupervised-learning" target="_blank">Ch 3 Unsupervised Learning and Preprocessing</a>
* Cross validation and grid search: <a href="https://learning.oreilly.com/library/view/introduction-to-machine/9781449369880/ch05.html" target="_blank">Ch 5 Model Evaluation and Improvement</a>
* Machine Learning pipelines for chaining models and encapsulating a workflow: <a href="https://learning.oreilly.com/library/view/introduction-to-machine/9781449369880/ch06.html#algorithm-chains-and-pipelines" target="_blank">Ch 6 Algorithm Chains and Pipelines</a>
  

## Generating Multiple Test Sets

If it is possible for multiple holdout test sets to be generated, using different ones for each evaluation in IMT and SDMT will produce the best results. 

However, it is often not possible for practitioners to generate , and there is research to support that substantial overfitting does not occur even if a single test set is used multiple times (<a href="https://proceedings.neurips.cc/paper/2019/file/ee39e503b6bedf0c98c388b7e8589aca-Paper.pdf" target="_blank">Roelofs et al. 2019</a>). 

To differentiate between evaluations, we recommend ensuring good version control for models as they are the unit by which `MLTE` tracks evaluations.
    

## Model Property Definition

Research on model property definition.

- <a href="https://ckaestne.medium.com/model-quality-defining-correctness-and-fit-a8361b857df" target="_blank">Model Quality: Defining Correctness and Fit</a>
- <a href="https://ckaestne.medium.com/model-quality-measuring-prediction-accuracy-38826216ebcb" target="_blank">Model Quality: Measuring Prediction Accuracy</a>
- <a href="https://ckaestne.medium.com/model-quality-slicing-capabilities-invariants-and-other-testing-strategies-27e456027bd" target="_blank">Model Quality: Slicing, Capabilities, Invariant, and Other Testing Strategies</a>
- <a href="https://ckaestne.medium.com/quality-drivers-in-architectures-for-ml-enabled-systems-836f21c44334" target="_blank">Quality Attributes of ML Components</a>
- <a href="https://research.google/pubs/pub40801/" target="_blank">The Tail at Scale</a>
- <a href="https://www.sciencedirect.com/science/article/pii/S0743731518308773" target="_blank">Estimation of Energy Consumption in Machine Learning</a>
  

## Requirements Selection

Research on requirements selection.

- <a href="https://arxiv.org/pdf/1908.04674.pdf" target="_blank">Requirements Engineering for Machine Learning</a>
- <a href="https://arxiv.org/ftp/arxiv/papers/2008/2008.11007.pdf" target="_blank">Towards Guidelines for Assessing Qualities of Machine Learning Systems</a>