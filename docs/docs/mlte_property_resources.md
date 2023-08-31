# MLTE Property Resources

*Properties* are characteristics of the trained model, the procedure used to train it (including training data), or its ability to perform inference. This section gives more detail and background on each property within MLTE. The properties are organized into three categories: 

- Functionality
- Robustness
- Costs   

## Functionality

### Task Efficacy

- Objective: Assess the ability of the model to perform the task for which it is designed.
- Metric: Select a task-appropriate model quality evaluation metric.
- Rationale: Measuring efficacy on a critical task is important to project success.
- Implementation: Select a task-appropriate implementation of your metric.

### Fairness

- Objective: Data and models should be free of bias to avoid unfair treatment of certain groups, to ensure a fair distribution of benefits and costs, and to offer those affected an opportunity to seek redress against adverse decisions made by the system or the humans operating it (<a href="https://arxiv.org/pdf/1810.08810.pdf" target="_blank">Chouldechova & Roth 2018</a>). 
- Metric: Statistical metrics of fairness include raw positive classification rate (<a href="https://arxiv.org/pdf/1412.3756v3.pdf" target="_blank">Feldman et al. 2015</a>), false positive and false negative rates, or positive predictive value (<a href="https://arxiv.org/pdf/1703.00056.pdf" target="_blank">Chouldechova 2017</a>). However, every fairness metric includes tradeoffs, so if this is important to the system then the model and system teams must discuss the overall effects and the appropriate tradeoffs to ensure fairness.
- Rationale: Biased models result in a <a href="https://dl.acm.org/doi/pdf/10.1145/3290605.3300830" target="_blank">degraded user experience</a> for certain sub-populations, and can damage user trust in a system.
- Implementation: Start by identifying the protected attribute in your dataset, and then determine what fairness measure the model and system should prioritize. 

#### Research on Fairness

- Metrics of statistical fairness: <a href="https://arxiv.org/pdf/1412.3756v3.pdf" target="_blank">Certifying and Removing Disparate Impact</a> and <a href="https://arxiv.org/pdf/1703.00056.pdf" target="_blank">Fair Prediction with Disparate Impact</a>
- Tradeoffs of individual versus statistical fairness: <a href="https://arxiv.org/pdf/1810.08810.pdf" target="_blank">The Frontiers of Fairness in Machine Learning</a>
- Testing/measuring individual fairness: <a href="https://arxiv.org/pdf/1710.03184.pdf" target="_blank">On Formalizing Fairness in Prediction with Machine Learning</a>
- How to consider the dynamic effects of decisions on a system: <a href="https://arxiv.org/pdf/1808.09004.pdf" target="_blank">Downstream Effects of Affirmative Action</a> and <a href="http://proceedings.mlr.press/v80/liu18c/liu18c.pdf" target="_blank">Delayed Impact of Fair Machine Learning</a>
- If you are familiar with the bias or skew of the data, an option is to use rank-preserving procedures for repairing features to reduce or remove pairwise dependence with the protected attribute: <a href="https://arxiv.org/pdf/1412.3756v3.pdf" target="_blank">Certifying and Removing Disparate Impact</a>
- A general discussion of bias and fairness in machine learning: <a href="http://ciml.info/dl/v0_99/ciml-v0_99-ch08.pdf" target="_blank">Ch 8 Bias and Fairness</a> from <a href="http://ciml.info" target="_blank">A Course in Machine Learning</a>
- Different definitions and examples of bias, discrimination, and fairness, as well as examples of fair versions of a number of types of machine learning models: <a href="https://arxiv.org/pdf/1908.09635.pdf" target="_blank">A Survey on Bias and Fairness in Machine Learning</a>
- Understanding, mitigating, and accounting for bias: <a href="https://arxiv.org/pdf/2001.09762v1.pdf" target="_blank">Bias in Data-driven AI Systems</a>
- Consider and articulate explicitly the assumptions about the circumstances and data being modeled: <a href="https://dl.acm.org/doi/pdf/10.1145/3433949" target="_blank">The (Im)possibility of Fairness: Different Value Systems Require Different Mechanisms For Fair Decision Making</a>
- The importance of having procedures, policies, and monitoring methods in place for machine learning: <a href="https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1270.pdf" target="_blank">Towards a Standard for Identifying and Managing Bias in Artificial Intelligence</a>

#### Fairness Questions

* Are subsets or groups within your dataset equally likely to be classified or predicted?
* If your model is being used on demographic groups, does your predictor produce similar outputs for similar individuals across demographic groups (<a href="https://arxiv.org/pdf/1710.03184.pdf" target="_blank">Gajane & Pechenizkiy 2018</a>)? 
* If your model feeds into a socio-technical system, will it dynamically affect the environment and the incentives of human actors who interact with the system?
* Is your dataset potentially biased or skewed in some way?

#### Considerations and Methods for Implementing Fairness

* Consider using metrics of statistical fairness (a small number of protected demographic groups should have parity of some statistical measure across all groups) such as raw positive classification rate (<a href="https://arxiv.org/pdf/1412.3756v3.pdf" target="_blank">Feldman et al. 2015</a>), false positive and false negative rates, or positive predictive value (last two from <a href="https://arxiv.org/pdf/1703.00056.pdf" target="_blank">Chouldechova 2017</a>).
*   Note that there are tradeoffs to individual versus statistical fairness, see <a href="https://arxiv.org/pdf/1810.08810.pdf" target="_blank">Chouldechova & Roth 2018</a>.
* If there is a reliable and non-discriminating distance metric, see <a href="https://arxiv.org/pdf/1710.03184.pdf" target="_blank">Gajane & Pechenizkiy's</a> definition 4 for a test by which individual fairness can be measured.
* <a href="https://arxiv.org/pdf/1808.09004.pdf" target="_blank">Kannan et al.</a> and <a href="http://proceedings.mlr.press/v80/liu18c/liu18c.pdf" target="_blank">Liu et al.</a> demonstrate how to consider the dynamic effects of decisions on a system; using the context of your system, identify ways in which downstream effects might modify the social fabric and determine if those parts of the model or the system need to be modified accordingly.
* Depending upon your knowledge of bias or skew in the data, consider using rank-preserving procedures for repairing features to reduce or remove pairwise dependence with the protected attribute from <a href="https://arxiv.org/pdf/1412.3756v3.pdf" target="_blank">Feldman et al. 2015</a>.

### Interpretability

- Objective: Some systems necessitate an ability to be explained or presented in human-understandable terms (<a href="https://arxiv.org/pdf/1702.08608.pdf" target="_blank">Doshi-Velez & Kim 2017</a>). 
- Metric: Interpretability is difficult to measure; it can be considered from an end-user perspective or from a developer perspective by observing and evaluating the interactions of these teams with the system, or having a domain expert explain model outputs in context (<a href="https://arxiv.org/pdf/1702.08608.pdf" target="_blank">Doshi-Velez & Kim 2017</a>).
- Rationale: Depending on the system purpose, it may be critical for the system to be explainable and understandable.
- Implementation: Options include, among others: intrinsic interpretability in which a model is self explanatory, or post-hoc interpretability where another model is created to explain outputs from the first (<a href="https://arxiv.org/pdf/1808.00033.pdf" target="_blank">Du et al. 2019</a>). 

#### Research on Interpretability

- <a href="https://arxiv.org/pdf/1702.08608.pdf" target="_blank">Towards A Rigorous Science of Interpretable Machine Learning</a>
- <a href="https://arxiv.org/pdf/1808.00033.pdf" target="_blank">Techniques for Interpretable Machine Learning</a>

#### Interpretability Questions

* Is it important that the model is explainable to the user? Some machine learning systems do not require explainability because “(1) there are no significant consequences for unacceptable results or (2) the problem is sufficiently well-studied and validated in real applications that we trust the system’s decision, even if the system is not perfect” (<a href="https://arxiv.org/pdf/1702.08608.pdf" target="_blank">Doshi-Velez & Kim 2017</a>).
* Can interpretability be done at the model-agnostic level and simply analyze outputs with respect to their context?

#### Considerations and Methods for Implementing Interpretability

* If interpretability is important, consider using intrinsic interpretability (in which the model is self-explanatory) or post-hoc interpretability (create another model to explain outputs from the first) from <a href="https://arxiv.org/pdf/1808.00033.pdf" target="_blank">Du et al. 2019</a>.
A domain expert can also be called upon to explain model outputs in their proper context (<a href="https://arxiv.org/pdf/1702.08608.pdf" target="_blank">Doshi-Velez & Kim 2017</a>).

## Robustness

### General Robustness Research

- Identifying model capabilities and generating test cases based on those capabilities helps ensure a robust model: <a href="https://www.cs.cmu.edu/~sherryw/assets/pubs/2020-checklist.pdf" target="_blank">Behavioral Testing</a>
- Practical examination of methods and metrics for robustness with case studies and scenarios: <a href="https://link.springer.com/chapter/10.1007/978-3-030-79150-6_21" target="_blank">Robustness Testing of AI Systems</a>
- Specific information about computer vision dataset augmentation: <a href="https://proceedings.neurips.cc/paper/2019/file/b05b57f6add810d3b7490866d74c0053-Paper.pdf" target="_blank">Model Robustness in Computer Vision</a>
- Performance measures for adversarial deep learning robustness: <a href="https://arxiv.org/pdf/2003.01993.pdf" target="_blank">Metrics and Methods for Robustness Evaluation</a>
- Proposed novel robustness ROC metric: <a href="https://www.journalfieldrobotics.org/Field_Robotics/Volume_1_files/10_Pezzementi.pdf" target="_blank">Perception Robustness Testing</a>

### Capability Approach for Robustness in Computer Vision

* Identify critical computer vision capabilities of the model to evaluate. See <a href="https://www.cs.cmu.edu/~sherryw/assets/pubs/2020-checklist.pdf" target="_blank">Ribeiro et al.</a> for content on identifying capabilities and developing task tests. Favor the model that has best learned the most relevant capabilities. Computer vision capabilities to consider testing include: 
*   Identifying shape
*   Robustness to altered texture
*   Robustness to novel backgrounds
*   Segmentation into regions
* Teams can test types including minimum functionality, invariance, and directional expectation
* Teams can curate test data through mutating existing inputs, generating new inputs, or obtaining new inputs.  

### Robustness to Naturally Occurring Data Challenges

- Objective: Ensure that the model is robust to naturally occurring data challenges that it will encounter in the ambient conditions of the system (<a href="https://link.springer.com/chapter/10.1007/978-3-030-79150-6_21" target="_blank">Berghoff et al. 2021</a>).
- Metric: Depending on the identified data challenges and the task specific properties, model robustness can be measured by a robustness score across the perturbation parameter space. This is a metric that calculates the fraction of correctly identified robust samples in the dataset. Reassessing the model accuracy with augmented datasets is a common metric for robustness (<a href="https://link.springer.com/chapter/10.1007/978-3-030-79150-6_21" target="_blank">Berghoff et al. 2021</a>).
- Rationale: Models implemented in a system will experience common data challenges like illumination, motion blur, occlusion, changes in perspective, and weather impacts. These perturbations affect the data and can have significant impacts on the quality of the model prediction, so they must be addressed before deployment (<a href="http://aima.cs.berkeley.edu" target="_blank">Russell & Norivg</a>). 
- Implementation: Dependent on the identified data challenges; the AutoAugment data augmentation policy proposed in <a href="https://proceedings.neurips.cc/paper/2019/file/b05b57f6add810d3b7490866d74c0053-Paper.pdf" target="_blank">Yin et. al</a> is a recommended starting point. The <a href="https://www.cs.cmu.edu/~sherryw/assets/pubs/2020-checklist.pdf" target="_blank">Ribeiro et al.</a> paper is also a useful tool to identify capabilities necessary for the model to promote robustness. 

#### Research on Robustness to Naturally Occurring Data Challenges

- Methods of addressing the potential naturally occurring data challenges that might arise from the ambient coditions of the system: <a href="https://link.springer.com/chapter/10.1007/978-3-030-79150-6_21" target="_blank">Robustness Testing of AI Systems</a> 

#### Questions on Robustness to Naturally Occurring Data Challenges

* What data challenges may occur when your model is deployed to the system? Could your model face: 
    *    Significant changes in illumination or color transformations (brightness, contrast, saturation, hue, grayscale, color-depth)?
    *   Motion blur or other pixel perturbations?
        *   Occlusion of the target object?
    *   Changes in perspective (rotation, translation, scaling, shearing, blurring, sharpening, flipping)?
    *   Weather impacts? (<a href="http://aima.cs.berkeley.edu" target="_blank">Russell & Norvig 2003</a>, Ch. 25)
    *   Other system specific conditions? (For example, stickers on objects or damaged objects)
* What are the typical and atypical system conditions in which your model will be deployed?
* How may data collection processes or physical sensors be degraded with time, use, or damage?
* Are there any extreme distribution shifts or long tail events that could cause large accuracy drops? (<a href="https://arxiv.org/pdf/2109.13916.pdf" target="_blank">Hendrycks et al. 2021</a>)

#### Considerations and Methods for Implementing Robustness to Naturally Occurring Data Challenges

* If there are known specific data challenges the model will face, consider prioritizing robustness to those perturbations. (For example, Gaussian data augmentation improves robustness to noise and blurring but degrades performance on fog and contrast (<a href="https://proceedings.neurips.cc/paper/2019/file/b05b57f6add810d3b7490866d74c0053-Paper.pdf" target="_blank">Yin et. al</a>)). Generate a list of task specific properties and plot the model robustness (measured by robustness score, or fraction of correctly identified robust samples in the dataset) across the perturbation parameter space (<a href="https://link.springer.com/chapter/10.1007/978-3-030-79150-6_21" target="_blank">Berghoff et al. 2021</a>).   
* Otherwise, to achieve the most generally robust model the AutoAugment data augmentation policy proposed in <a href="https://proceedings.neurips.cc/paper/2019/file/b05b57f6add810d3b7490866d74c0053-Paper.pdf" target="_blank">Yin et. al</a> achieves the most generalizable robustness to data augmentation. 
* You might also consider tying into the system-level framework in order to build in feedback loops that could influence the environment.

### Robustness to Adversarial Attack

 - Objective: Ensure that the model is robust to synthetic manipulation or targeted adversarial attacks (<a href="https://arxiv.org/pdf/2109.13916.pdf" target="_blank">Hendrycks et al.</a> and <a href="https://berryvilleiml.com/docs/ara.pdf" target="_blank">McGraw et al. 2020</a>).
- Metric: There are performance metrics for adversarial robustness (<a href="https://arxiv.org/pdf/2003.01993.pdf" target="_blank">Buzhinsky et al. 2020</a>) and existing benchmarked adversarial robustness tools such as <a href="https://github.com/cleverhans-lab/cleverhans" target="_blank">CleverHans</a>, <a href="https://github.com/bethgelab/foolbox" target="_blank">Foolbox</a>, and the Adversarial Robustness Toolbox (<a href="https://github.com/Trusted-AI/adversarial-robustness-toolbox" target="_blank">ART</a>) that may be used. 
- Rationale: A model deployed in a system may face different vulnerabilities (data pollution, physical infrastructure, etc.) and attacks (poisoning, extraction, inference, etc.) that can significantly degrade the performance, security, or safety of the model. 
- Implementation: Approaches to implementing robustness to adversarial attack vary depending on which methods of attack are most likely and most detrimental for your system. 

#### Questions on Robustness to Adversarial Attack

* How is an adversary most likely going to attempt to break your model?
* What would be the most dangerous method an adversary could use to break your model?
* Did you consider different types and natures of vulnerabilities such as data pollution, physical infrastructure, and cyber-attacks? (<a href="https://arxiv.org/pdf/2109.13916.pdf" target="_blank">Hendrycks et al. 2021</a>)
* What is the threat of evasion attacks, poisoning attacks, extraction attacks, and inference attacks, and does the model need to be prepared to address these? (<a href="https://github.com/Trusted-AI/adversarial-robustness-toolbox" target="_blank">ART</a>)
* Did you consult with the systems team to put measures in place to ensure integrity and resilience of the system against attacks?

#### Considerations and Methods for Implementing Robustness to Adversarial Attack

 * Consider using performance metrics for adversarial robustness like in <a href="https://arxiv.org/pdf/2003.01993.pdf" target="_blank">Buzhinsky et al. 2020</a>. Adversarial robustness in the latent space is the “resilience” to the worst-case noise additions. Metrics include local latent adversarial robustness, generation severity, reconstructive severity, and reconstructive accuracy. 
* Generate simulations for possible adversarial attacks to predict behavior in settings that preclude practical testing of the system itself (<a href="https://www.journalfieldrobotics.org/Field_Robotics/Volume_1_files/10_Pezzementi.pdf" target="_blank">Pezzementi et al. 2021</a>). Evaluate model performance based on a metric like a robustness receiver operating curve (ROC). 
* Consider using a benchmarked adversarial robustness tool like <a href="https://github.com/cleverhans-lab/cleverhans" target="_blank">CleverHans</a>, <a href="https://github.com/bethgelab/foolbox" target="_blank">Foolbox</a>, or <a href="https://github.com/Trusted-AI/adversarial-robustness-toolbox" target="_blank">ART</a>.
* If it would be beneficial to detect adversarial anomalies or assign low confidence values to potential adversarial inputs, that is something that should be tied into the system framework. 

### Robustness to Device-Generated Perturbations

- Objective: Ensure that the model and the system are robust to perturbations resulting from devices that are part of the system. An example of a device-generated perturbation would be a camera taking unfocused video or pictures, making it impossible for the computer vision model to detect objects.
- Metric: If sensor redundancy is determined to be necessary, establish a common representation of the input and evaluate the system with simulated sensor failures. If robustness to single sensor noise is acceptable, determine the most likely sensor degradations and evaluate the mAP on a simulated degraded dataset.
- Rationale: Models are often evaluated with full sensor availability. However, in a safety-critical system, unexpected scenarios like sensor degradation or failure must be accounted for. 
- Implementation: Depending on the system in which the model will be deployed, an option is to implement sensor redundancy. An architecture that uses multiple sensors to perform object detection jointly can provide robustness to sensor failure (<a href="https://odr.chalmers.se/bitstream/20.500.12380/300780/1/master-thesis-report_berntsson-tonderski.pdf" target="_blank">Berntsson & Tonderski 2019</a>). Alternatively, if typical sensor degradation patterns are known or possible to predict, robustness tests specific to the sensor can be designed (<a href="https://trace.tennessee.edu/cgi/viewcontent.cgi?article=6960&context=utk_gradthes" target="_blank">Seals 2019</a>). For example, evaluating the mAP of the model against speckle noise, salt and pepper noise, contrast alterations, or Gaussian noise can be used to determine robustness. 

### Robustness to Synthetic Image Modifications

Addressing synthetic image modifications allows models to handle images that have been modified synthetically (for instance, a filter has been applied). 

#### Questions on Robustness to Synthetic Image Modifications

* Are there critical computer vision capabilities that would allow the model to generalize robustly beyond controlled training settings?
* How may a human approach the task in the face of synthetic modifications? Is edge detection necessary to complete the task?
* Is there existing knowledge or theories about the task that can be leveraged?

#### Capability Approach for Robustness to Synthetic Image Modifications

* Identify critical computer vision capabilities of the model to evaluate. See <a href="https://www.cs.cmu.edu/~sherryw/assets/pubs/2020-checklist.pdf" target="_blank">Ribeiro et al.</a> for content on identifying capabilities and developing task tests. Favor the model that has best learned the most relevant capabilities. Computer vision capabilities to consider testing include: 
*   Identifying shape
*   Robustness to altered texture
*   Robustness to novel backgrounds
*   Segmentation into regions
* Teams can test types including minimum functionality, invariance, and directional expectation
* Teams can curate test data through mutating existing inputs, generating new inputs, or obtaining new inputs.  

### Security

- Objective: Ensure that the model is insulated to compromise from internal error.
- Metric: The metric by which security is measured will depend on what risks are most likely for your given model. Areas of focus could include adversarial attacks (as described above), reproducibility, overfitting, and output integrity among others. See <a href="https://berryvilleiml.com/docs/ara.pdf" target="_blank">McGraw et al.</a> for a comprehensive list of risks and recommended methods of addressing them.
- Rationale: A model and the system in which it is encased have numerous risk areas that can be traced back to intrinsic design flaws (<a href="https://berryvilleiml.com/docs/ara.pdf" target="_blank">McGraw et al. 2020</a>).
- Implementation: Prioritize risks based on your model and system, and address them in order of probability that they occur.  

## Costs

### Model Size (Static)

- Objective: Measure the static size of a trained model.
- Metric: The storage requirement for the model in bytes or some multiple thereof (e.g. kilobytes, megabytes, etc.). This metric is absolute.
- Rationale: A model’s static size is its size at rest, when it is ready to perform inference. The static size of the model may limit the infrastructure on which it may be deployed. 
- Implementation: Measure the on-disk size of the model static format. The exact implementation may vary based on the development platform and environment available. Examples of potential implementations are provided below.

On UNIX-like systems, use the `du` ("disk usage") command to measure model size:

```bash
# For models stored statically as a single file
$ du --bytes model

# For models stored statically as a directory
$ du --bytes model/*
```

On Windows systems, the Explorer GUI displays file and directory size. Alternatively, use the following commands in a Powershell interpreter to measure model size:

```powershell
# For models stored statically as a single file
Get-Item model | Measure-Object -Property Length -Sum

# For models stored statically as a directory
Get-ChildItem model/ | Measure-Object -Property Length -Sum
```

Programmatically measuring the file size may be the most useful when automating this procedure in an ML pipeline. `MLTE` provides functionality for measuring the size of models stored on the local filesystem:

```python
from mlte.measurement import model_size

path = # the path to model on local filesystem
size = model_size(path)
print(size)
```
	
### Model Size (Dynamic)

- Objective: Measure the dynamic size of a trained model in terms of its storage requirements.
- Metric: The storage requirement for the model in bytes or some multiple thereof (e.g., kilobytes, megabytes, etc.). This metric is absolute.
- Rationale: A model’s dynamic size is its size in a serialized form that is appropriate for transport (e.g. via removable media or over the network). The dynamic size of the model determines the difficulty (time requirement) of transporting the model. This concern manifests both internally during development of an automated training pipeline as well as externally during deployment. The dynamic size of a model may depend on the choice of serialization format, compression, and encryption, among other factors.
- Implementation: Measure the on-disk size of the model dynamic format. The exact implementation may vary based on the development platform and environment available. Examples of potential implementations are provided below.

On UNIX-like systems, use the `du` ("disk usage") command to measure model size:

```bash
# For models stored statically as a single file
$ du --bytes model

# For models stored statically as a directory
$ du --bytes model/*
```

On Windows systems, the Explorer GUI displays file and directory size. Alternatively, use the following commands in a Powershell interpreter to measure model size:

```powershell
# For models stored statically as a single file
Get-Item model | Measure-Object -Property Length -Sum

# For models stored statically as a directory
Get-ChildItem model/ | Measure-Object -Property Length -Sum
```

Programmatically measuring the file size may be the most useful when automating this procedure in an ML pipeline. `MLTE` provides functionality for measuring the size of models stored on the local filesystem:

```python
from mlte.measurement import model_size

path = # the path to model on local filesystem
size = model_size(path)
print(size)
```
	
### Training Time

- Objective: Measure the total time required to train the model.
- Metric: The wall-clock time required to run the model training process in seconds or some multiple thereof (e.g. minutes, hours, etc.). This metric is relative.
- Rationale: Training time is a critical constraint on the machine learning pipeline. Long-training times limit the ability of the ML engineer to iterate on the model and make improvements during development. Long-training times also limit the frequency with which new models may be deployed to production. 
- Implementation: The wall-clock time required to train a machine learning model is highly-dependent upon the system on which training occurs. A system with better hardware properties (e.g. CPU cores, clock frequency, cache capacity, RAM capacity) trains faster than a weaker one. Whether or not a GPU is available, and the quality thereof, is another consideration. When the input dataset is large, storage system performance may become the bottleneck. For models that require distributed training, cluster properties confound these measurements. This variability necessitates a common benchmark infrastructure for model training time.

### Training CPU Consumption

- Objective: Measure the peak and average CPU utilization during model training. 
- Metric: The percentage of compute resources utilized by the training process as a percentage of the total compute available to the system on which it is evaluated. This metric is _relative_.
- Rationale: The computational requirements of model training determine the load that it places on the system during the training procedure. Typically, we are not concerned with the efficiency of other jobs that run concurrently on the same machine during model training. Therefore, the peak and average CPU consumption of the training process are primarily relevant because they determine the resource requirements necessary to train efficiently. This metric is not directly applicable to a distributed training procedure.
- Implementation: Measure the CPU utilization of the process running the training procedure. The measurement procedure will vary depending on the training environment.

Measure the CPU utilization of the training procedure with `MLTE`:

```python
from mlte.monitoring import cpu_utilization

pid = # identifier of training process 

stats = cpu_utilization(pid)
print(stats)
```

### Training Memory Consumption

- Objective: Measure the peak and average memory consumption during model training.
- Metric: The volume of memory consumed in bytes or some multiple thereof (kilobytes, megabytes, etc.). This metric is absolute. 
- Rationale: The memory requirements of model training determine the load that is places on the system during the training procedure. Typically, we are not concerned with the efficiency of other jobs that run concurrently on the same machine during model training. Therefore, the peak and average memory consumption of the training process are primarily relevant because they determine the resource requirements necessary to train efficiently.  This metric is not directly applicable to a distributed training procedure.
- Implementation: Measure the memory consumption of the process running the training procedure. The measurement procedure will vary depending on the training environment.

Measure the memory consumption of the training procedure with `MLTE`:

```python
from mlte.monitoring import memory_consumption

pid = #  identifier of training process

stats = memory_consumption(pid)
print(stats)
```

### Training Energy Consumption

- Objective: Measure the energy consumption of the model training process.
- Metric: The energy consumed by the training process in joules (total power consumption over a time interval).
- Rationale: For large-scale machine learning applications, energy consumption may be a major driver in the total cost of development and maintenance. The model training process is frequently the most energy-intensive stage of the machine learning pipeline.
- Implementation: Energy consumption and power requirements are a relatively-new consideration in the field of machine learning. Accordingly, methods for convenient and accurate measurement are limited.

### Inference Latency (Mean)

- Objective: Measure the mean inference latency of a trained model.
- Metric: The time required to complete a single inference request, in milliseconds. This metric is relative.
- Rationale: Inference latency refers to the time required for a trained model to make a single prediction given some input data. While the machine learning model is likely only a small part of the intelligent system in which it is integrated, it may contribute substantially to the overall latency of the service.
- Implementation: Measure the latency of the model across many inference requests and compute the mean. The measurement procedure will vary based on the development environment.

Measure the mean latency of model inference with `MLTE`:

```python
from mlte.measurement import mean_latency

model = # trained model that implements __call__()
d_gen = # input generator that implements __call__()

latency = mean_latency(model, d_gen)
print(f"Mean latency: {latency}ms")
```

### Inference Latency (Tail)

- Objective: Measure the tail inference latency of a trained model.
- Metric: The time required to complete a single inference request, in milliseconds. This metric is relative.
- Rationale: Tail latency refers to the latency of model inference at the (right) tail of the latency distribution. In many production environments, mean latency does not adequately reflect the production viability of model in terms of its runtime requirements. Instead, tail latency provides a more informative measure of the guarantees we can provide about model runtime performance.
- Implementation: Measure the latency of the model across many inference requests and compute the desired tail percentile. The measurement procedure will vary based on the development environment.

Measure the tail latency of model inference with `MLTE`. By default, the `tail_latency()` function computes the 99th percentile latency, but this value may be changed via a keyword argument.

```python
from mlte.measurement import tail_latency

model = # trained model that implements __call__()
d_gen = # input generator that implements __call__()

latency = tail_latency(model, d_gen)
print(f"Tail latency: {latency}ms")
```

### Inference Throughput

- Objective: Measure the inference throughput of a trained model.
- Metric: The number of inference requests completed in one second. This metric is relative.
- Rationale: For some applications, service throughput is a more important metric than service latency. In such cases, we may be unconcerned with the latency of inference requests to the model and more concerned with its throughput.
- Implementation: Measure the throughput of the model by providing it with a stream of many inference requests, computing the time required to complete all of these requests, and dividing the number of completed requests by this duration. The measurement procedure will vary based on the 

Measure the throughput of model inference with `MLTE`.

```python
from mlte.measurement import throughput

model = # trained model that implements __call__()
d_gen = # input generator that implements __call__()

t_put = throughput(model, d_gen)
print(f"Throughput: {t_put} requests per second")
```

### Inference CPU Consumption

- Objective: Measure the peak and average CPU utilization during model inference.
- Metric: The percentage of compute resources utilized by the inference service as a percentage of the total compute available to the system on which it is evaluated. This metric is relative.
- Rationale: The computational requirements of model inference determine the load that it places on the system when performing inference. This is a key determinant in the compute resources required for model deployment. For example, a model for which inference is computationally inexpensive may be deployed to an instance with relatively light computational resources. This might allow for investment in other resources, such as memory capacity, for the instance to which the model is deployed.
- Implementation: Measure the CPU utilization of the inference service. The setup for inference measurement may be more involved than training measurement because inference is often not run as a standalone process. 

### Inference Memory Consumption

- Objective: Measure the peak and average memory consumption during model inference.
- Metric: The volume of memory consumed in bytes or some multiple thereof (kilobytes, megabytes, etc.). This metric is absolute. 
- Rationale: The memory requirements of model inference determine the load that is places on the system during inference. This is a key determinant in the memory resources required for model deployment. For example, a model for which inference is not memory-intensive may be deployed to an instance with relatively light memory resources. This might allow for investment in other resources, such as core count, for the instance to which the model is deployed. 
- Implementation: Measure the memory consumption of the process during the inference procedure.

### Inference Energy Consumption

- Objective: Measure the energy consumption of the model inference process.
- Metric: The energy consumed by the inference process in joules (total power consumption over a time interval).
- Rationale: For large-scale machine learning applications, energy consumption may be a major driver in the total cost of development and maintenance.
- Implementation: Energy consumption and power requirements are a relatively-new consideration in the field of machine learning. Accordingly, methods for convenient and accurate measurement are limited.