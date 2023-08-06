---
name: Artifact Protocol Port
about: Port an existing MLTE artifact to the Artifact Protocol.
title: ''
labels: enhancement
assignees: ''

---

The current requirements for porting an existing artifact to the artifact protocol are as follows:

- Implement the model for the artifact
- Implement unit tests for the artifact model
- Implement the artifact protocol for the artifact itself
	- `to_model()`
	- `from_model()`
	- `save_with()`
	- `load_with()`
- Implement unit tests for the artifact
- Add the interface to the Store base class (write_X, read_X, delete_X)
- Add the implementation to the underlying store implementations:
	- `InMemoryStore`
	- `RemoteHttpStore`
- Add unit tests for the underlying store implementations:
	- `InMemoryStore`
	- `RemoteHttpStore`
- Add relevant endpoints to the web store implementation
- Add unit tests to the web store implementation
