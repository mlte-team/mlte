# Glossary

This glossary hopes to definitively represent the conventions applied in MLTE and its API. It aims to describe acronyms and concepts while providing a reference for users and contributors. 

## Acronyms

**A2IT:** Army Artificial Intelligence Testing

**AI:** Artifical Intelligence

**AI2C:** Artificial Intelligence Integration Center

**IMT:**  Internal Model Testing 

**ML:** Machine Learning

**SDMT:** System Dependent Model Testing

## General Concepts

**[Army Artificial Intelligence Testing](https://github.com/mlte-team/a2it) Framework:** A framework containing guidelines for how teams can test their ML models and systems. Our framework is directly applicable for any individual or team who is writing or adapting a ML model for a system. While AI is a broad term that includes technologies other than ML, that is the primary implementation of AI at the moment so that is where we focused our efforts. This framework is based in work done across the ML community and is consistent with the structure of other AI safety and regulatory efforts such as capAI2 and model cards.3 Besides its grounding in academic research, our framework is also based on communication with experts in industry and the military, as well as our experiences as Army officers. Finally, our framework is updated to reflect feedback from interviews with personnel at the AI2C.

**Artificial Intelligence:** A system or model that enables computers to do things that would be considered “intelligent” if done by humans. Most commonly AI is concerned with rational action. An ideal intelligent agent takes the best possible action in a situation. Also consider capabilities of intelligence for specific tasks (reasoning, learning, language, vision, movement, etc.)

**Data Cascades:** “Compounding events causing negative, downstream effects from data issues - triggered by conventional AI/ML practices that undervalue data quality, resulting in technical debt overtime” Avoided by: Having "good" data, promoting incentives for data excellence, AI data education, and data visibility and collaboration

**[IMT](https://github.com/mlte-team/a2it/blob/master/framework/0_IMT.md):** Given the challenges inherent in accounting for inputs, outputs, and requirements of a total ML system a priori, it important to have a section dedicated to understand and evaluate the standalone conceptual ML model.

**Baselines:** To ensure the utility and value of a model, developers must select a baseline test for comparison. In some realms of ML like computer vision, there are benchmark or baseline datasets and tests that can be used. There are also standard practices for some types of ML like classification, in which an accepted baseline is to classify everything as the majority class.

**[SDMT](https://github.com/mlte-team/a2it/blob/master/framework/1_SDMT.md):** This section is dedicated to ensuring teams have the information they need to consider priorities, tradeoffs, and weaknesses of their model in the context of the system. The idea is that a model team in collaboration with the system team will read these properties, each of which has an objective, metric, rationale, and implementation, and determine which ones are most applicable for their project.

**Robustness:** Robustness contains properties pertaining to security and robustness. In ML, this takes numerous forms, so our framework includes several types of robustness: robustness to naturally occurring data challenges, robustness to adversarial attack, and robustness to device-generated perturbations.

**Functionality:** Within the functionality category, we included the following properties: prediction accuracy, fairness, and interpretability.

**Costs:** Costs ties closely into how the ML system is set up, in particular its hardware. The properties in this category are static and dynamic model size, training time, training CPU consumption, training memory consumption, training energy consumption, inference latency (mean and tail), inference throughput, inference CPU consumption, inference memory consumption, and inference energy consumption.

**Fairness:** Group fairness is the goal of groups defined by protected attributes receiving similar treatments or outcomes. Individual fairness is the goals of similar individuals receiving similar treatments or outcomes. There is also equal outcome, equal opportunity, and equal impact to consider. Cannot maximize all aspects at once.   

**Interpretability:** It is important to know the relationship between data and its associated interpretation. 

**Performance Metric:** After determining a baseline test, teams must pick a performance metric. There are a wide range of metrics that could be appropriate depending on the type of model and the context in which the task is performed. 

**Scalability:** Is the ability of AI to perform at the size, speed, and complexity required. 

**Properties:** Properties are the characteristics or traits of a ML model or system. Developers will consider priorities, tradeoffs, and weaknesses of their model in the context of the system and prioritize properties for testing. The categories that organize properties are listed in [SDMT](https://github.com/mlte-team/a2it/blob/master/framework/1_SDMT.md). Properties in MLTE are an abstract element that are measured by measurements and validated by validators which are bound to properties. 

**Measurement:** Measurements are the isntances that assesses a property. For example, the total local process memory consumptions is a *measurement* that measures the *property* of Training Memory Cost. 

**Suites:** Suites are collections of properties and their associated measurements and bound validators. Suits help contain and organize the *MLTE* properties so that models can be easily re-evaluted. It also aids in the generation of the *MLTE* report.
 
**Report:** Report contains a number of subclasses that are returned and displayed in the automatically generated *MLTE* report. The report renders as a web page and is opened automatically in an available window of the default browser. 