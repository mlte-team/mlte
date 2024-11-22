
# Machine Learning Test and Evaluation (MLTE)

<img src="https://raw.githubusercontent.com/mlte-team/mlte/master/assets/MLTE_Logo_Color.svg" alt="mlte_logo" width="120"/>

`MLTE` (pronounced "melt") is a process and a Python library that provides infrastructure for machine learning (ML) test and evaluation. `MLTE` enables teams to more effectively negotiate, document, and evaluate model and system qualities. 

## MLTE Process
![MLTE Diagram](img/MLTE_Diagram_Dark.png)
*Diagram to be updated October 2024*

### Continuous Negotiation
To begin, model developers and project stakeholders meet to determine mission, business, and system requirements that will influence model development such as the deployment environment, available data, model requirements, and system requirements. Throughout the process, teams continue to have meetings to update their assumptions and requirements.

#### MLTE Negotiation Card
As part of the negotiation, teams fill out a `MLTE` [Negotiation Card](negotiation_card.md) which allows them to record agreements and drives model development and testing.

#### Quality Attribute Scenarios
Quality attribute scenarios are a way to specify a system’s structural and behavioral requirements; MLTE leverages this approach during negotiations to help teams move from vague statements to concrete requirements.

### Initial Model Testing (IMT)
Teams use information from the [Negotiation Card](negotiation_card.md) during initial model development to inform model requirements and thresholds. Once initial development is complete, model teams do initial testing during this step to determine when the model exceeds their baselines.

### System Dependent Model Testing (SDMT)
Once a model passes its baseline requirements in IMT, teams can then focus on ensuring that it passes the larger set of system and model requirements. To do so, teams use system requirement and quality attribute information from the [Negotiation Card](negotiation_card.md) to develop a test specification, which contains code that will evaluate each model or system requirement.

#### Test Catalog
The `MLTE` Test Catalog contains reusable — local or organizational — examples of test cases organized by quality attribute. Model developers can use it to find examples of tests (like looking for code examples on StackOverflow).

#### Communicating Results
Once SDMT has provided evidence of how a model performs against required model and system qualities, a MLTE Report can be generated to communicate test results and provide the context for requirements and results.

If results are satisfactory, the output is a production-ready model (meaning that it meets defined system and model requirements), along with all testing evidence (code, data, and results). 

If results are not satisfactory, more negotiation is required to determine if requirements are realistic, whether more experimentation is required, or whether results triggered additional requirements or tests.

## Further Information

- [MLTE Process](mlte_process.md) (A more detailed guide than above)
- [Setting Up MLTE](setting_up_mlte.md)
- [Development Environment](development.md)
- MLTE <a href="https://arxiv.org/abs/2303.01998" target="_blank">Paper</a> (ICSE 2023 - 45th International Conference on Software Engineering)
- <a href="https://doi.org/10.48550/arXiv.2406.08575" target="_blank">Using Quality Attribute Scenarios for ML Model Test Case Generation</a> (SAML 2024 - 3rd International Workshop on Software Architecture and Machine Learning)

## MLTE Metadata

- Version: 1.0.1
- Contact Email: mlte dot team dot info at gmail dot com
- Citations: While not required, it is highly encouraged and greatly appreciated if you cite our paper when you use `MLTE` for academic research.

    ```
    @inproceedings{maffey2023,
        title={{MLTEing models: Negotiating, Evaluating, and Documenting Model and System Qualities}},
        author={Maffey, Katherine R and Dotterrer, Kyle and Niemann, Jennifer and Cruickshank, Iain 
        and Lewis, Grace A and K{\"a}stner, Christian},
        booktitle={2023 IEEE/ACM 45th International Conference on Software Engineering: New Ideas and
        Emerging Results (ICSE-NIER)},
        pages={31--36},
        year={2023},
        organization={IEEE}
    }
    ```
    ... or if you use, or are inspired by, quality attributes for ML model test case generation.
    ```
    @inproceedings{brower2024,
        author={Brower-Sinning, Rachel and Lewis, Grace A. and Echeverría, Sebastián and Ozkaya, Ipek},
        booktitle={2024 IEEE 21st International Conference on Software Architecture Companion (ICSA-C)}, 
        title={Using Quality Attribute Scenarios for ML Model Test Case Generation}, 
        year={2024},
        pages={307-310},
        organization={IEEE}
    }  
    ```


## Check out `MLTE` on <a href="https://github.com/mlte-team/mlte" target="_blank">GitHub</a>!