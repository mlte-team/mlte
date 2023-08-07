---
name: Artifact Protocol Port
about: Port an existing MLTE artifact to the Artifact Protocol.
title: ''
labels: enhancement
assignees: ''

---

The current requirements for porting an existing artifact to the artifact protocol are as follows:

- Implement the model for the artifact
- Implement unit tests for the artifact model (e.g. ensure that it can serialize and deserialize properly, 
- Implement the artifact protocol for the artifact itself
	- `to_model()`
	- `from_model()`
	- `save_with()`
	- `load_with()`
- Implement unit tests for the artifact
