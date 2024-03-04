# MLTE Negotiation Card

## System Requirements

### Goals of the System

Goals or objectives that the model is going to help satisfy. For each goal, there can be one or more metrics to measure that goal, and every metric has a corresponding baseline.

Example: Match voice recordings that belong to the same person 

#### Metric

For each goal, select a performance metric that captures the system's ability to accomplish that goal.

Example: Accuracy on matching voices from the same person

#### Baseline 

Select a baseline for each performance metric, which means a measurement that evaluates whether or not the model will/can achieve the main goal for which it is being created. If the goal cannot be measured directly, select a reasonable proxy and justify how that will reliably predict the model’s performance in achieving its goal.

Example: Human accuracy for matching voices is ~60%

### ML Problem Type 

Type of ML problem that the model is intended to solve.

Example: Classification

### ML Task 

Well-defined task that model is expected to perform, or problem that the model is expected to solve.

Example: Identifying which voice recordings were spoken by the same person

### Usage Context

Who is intended to utilize the system/model; how the results of the model are going to be used by end users or in the context of a larger system.

Example: Analyzing many recordings to determine which ones include a specific person of interest

### Risk of Producing a False Positive

### Risk of Producing a False Negative

### Other Risks of Producing Incorrect Results

## Data

Details of the data that will influence development efforts; fill out all that are known.

### Data Description

Describe the data generally.

### Data Source

Where is the data coming from?

### Data Classification

What classification is the data?

### Data Access / Availability

How will the data be accessed? Record what needs to happen to access the data, such as accounts that need to be created or methods for data transportation.

### Data Labels / Distribution
List out all the labels for the data, along with the percentage of data they account for (if known).

### Data Schema

Include relevant information that is known about the data; fill out all sections below for each data field. E.g., if there are four data fields, you would have four versions of the following descriptors, one for each data field.

#### Field Name: 
#### Field Description: 
#### Field Type: 
#### Expected Values: 
#### Missing Values: 
#### Special Values: 

### Data Rights

Are there particular ways in which the data can and cannot be used?

### Data Policies 

Are there policies that govern the data and its use, such as Personally Identifiable Information [PII]?

## Model

### Development Compute Resources

Describe the amount and type of compute resources needed for training.

#### GPUs: 
#### CPUs: 
#### Memory: 
#### Storage: 

### Integration

Describe how the model will be integrated into the system; this likely includes descriptions of model deployment, application hosting, etc.

### Input Specification

Describe the input data type and format needed for the model to conduct inference.

### Output Specification

Describe the output format and specification needed for the system to ingest model results.

## Production Compute Resources

Describe the hardware and software requirements for inference.

#### GPUs: 
#### CPUs: 
#### Memory: 
#### Storage: 

### Other Considerations