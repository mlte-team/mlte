# Machine Learning Test and Evaluation (MLTE) Framework

## ➀ Negotiate Model Quality Requirements (IMT Negotiation)
Before development begins, the model development team and project stakeholders (including software engineers and system experts) negotiate model goals and suitable evaluation metrics. In MLTE, requirements definition directly informs how a model is evaluated. To guide this negotiation, MLTE provides a Negotiation Card, which can be accessed and persisted via the MLTE UI. After this negotiation, development ensues in accordance with the agreed-upon considerations.

## ➁ Internal Model Testing (IMT)
Internal Model Testing (IMT) is the process of evaluating a model with regard to the negotiated requirements. Teams use IMT tests after initial model development has been completed. The MLTE process assumes that ML development is an iterative process, so teams are encouraged to repeat IMT until they verify that model performance exceeds the baseline.

1. TRAINED MODEL: Performing IMT assumes that teams have a trained model. 
2. TEST MODEL AGAINST PERFORMANCE METRIC: Test the trained model against the performance metric selected during the negotiation with stakeholders during MLTE step ➀. 
3. DOES PERFORMANCE EXCEED BASELINE? 

    - YES: If performance exceeds the baseline, go to the next item in the MLTE workflow.
    
    - NO: If performance does not exceed the baseline, revisit the MLTE Negotiation Card to see if any of the items defined there need to change. After verifying model qualities via the Negotiation Card, retrain the model and then repeat IMT.

## ➂ Negotiate Model Requirements Beyond Task Efficacy (SDMT Negotiation)
Model developers and stakeholders (including software engineers and system experts) negotiate again, this time regarding model requirements with respect to the system into which the model will be integrated (e.g., robustness, fairness, inference latency, etc). 

1. NEGOTIATE MODEL REQUIREMENTS: Teams should refer to the MLTE Negotiation Card used in MLTE step ➀, and revisit all considerations discussed there. Once the Negotiation Card has been refined, teams can move onto designing their specification.
2. SPECIFICATION DESIGN and PROPERTY SELECTION: Teams design a specification by selecting and prioritizing the model requirements that are important to their project from the list of MLTE *properties*. Evidence will be collected to validate that a requirement is met by a ML system using *measurements*.  

    - A *property* is a characteristic of the trained model, the procedure used to train it (including training data), or its ability to perform inference.
    
    - A *measurement* is a concrete function that implements a property.
  
3. MEASUREMENT SELECTION: After designing the specification, which includes selecting the properties that are relevant to a team's particular ML system, they must then determine what measurements they will use.
    * Measurement selection ensures that the proper evidence is collected to show that the ML system will function as intended in its proper context.
    * Measurements correspond to properties; a list of current MLTE measurement offerings can be found here (LINK TO BE ADDED).

## ➃ System Dependent Model Testing (SDMT)
Model developers and software engineers evaluate the specification defined during the SDMT negotiation (MLTE step ➂) using measurements. By evaluating the properties using measurements, teams are able to collect evidence against the project's requirements. 

## ➄ Communicate ML Evaluation Results
Teams use the MLTE automated report functionality to encapsulate all knowledge gained about the model and the system as a consequence of the evaluation process. This facilitates the team's ability to communicate results from the evidence collected against previously-agreed-upon requirements. 