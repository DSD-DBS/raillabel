<!--
 ~ Copyright DB InfraGO AG and contributors
 ~ SPDX-License-Identifier: Apache-2.0
 -->

# RailLabel

<!-- prettier-ignore -->
![image](https://github.com/DSD-DBS/raillabel/actions/workflows/build-test-publish.yml/badge.svg)
![image](https://github.com/DSD-DBS/raillabel/actions/workflows/lint.yml/badge.svg)

A devkit for working with recorded and annotated train ride data from Deutsche Bahn.

You can install the latest released version directly from PyPI.

```zsh
pip install raillabel
```

For the full documentation look at [the Github pages](https://dsd-dbs.github.io/raillabel).

# Examples

The first step in using `raillabel` is downloading a desired dataset (like [OSDaR23](https://data.fid-move.de/dataset/osdar23)). You can then load any scene by running
```python
import raillabel

scene = raillabel.load("path/to/annotation_file.json")
```

This returns a [`raillabel.Scene`](https://dsd-dbs.github.io/raillabel/code/raillabel.html#raillabel.Scene), which is the root class for the annotations.

You can then extract information about the scene from the file
```python
# Iterate over all annotations
for frame in scene.frames.values():
    for annotation in frame.annotations.values():
        pass  # do something with the annotation here
```

If a file is too extensive for your use-case you can filter out certain parts of a scene like this
```python
from raillabel.filter import (
    IncludeObjectTypeFilter,
    ExcludeAnnotationTypeFilter,
    StartTimeFilter, ExcludeFrameIdFilter,
    IncludeAttributesFilter
)

scene_with_only_trains = scene.filter([IncludeObjectTypeFilter(["rail_vehicle"])])

scene_without_bboxs = scene.filter([ExcludeAnnotationTypeFilter(["bbox"])])

cut_scene_with_only_red_trains = scene.filter([
    StartTimeFilter("1587349200.004200000"),
    ExcludeFrameIdFilter([2, 4]),
    IncludeObjectTypeFilter(["rail_vehicle"]),
    IncludeAttributesFilter({"color": "red"}),
])
```
An overview of all available filters can be found [here](https://dsd-dbs.github.io/raillabel/code/raillabel.filter.html#module-raillabel.filter).

If you then want to save your changes, then use
```python
raillabel.save(cut_scene_with_only_red_trains, "/path/to/target.json")
```

# Contributing

To set up a development environment, clone the project and install it into a
virtual environment.

```zsh
git clone https://github.com/DSD-DBS/raillabel
cd raillabel
python -m venv .venv

source .venv/bin/activate.sh  # for Linux / Mac
.venv\Scripts\activate  # for Windows

pip install -U pip pre-commit
pip install -e '.[docs,test]'
pre-commit install
```

We'd love to see your bug reports and improvement suggestions! Please take a
look at our [guidelines for contributors](CONTRIBUTING.md) for details.

# Licenses

This project is compliant with the
[REUSE Specification Version 3.0](https://git.fsfe.org/reuse/docs/src/commit/d173a27231a36e1a2a3af07421f5e557ae0fec46/spec.md).

Copyright DB InfraGO AG, licensed under Apache 2.0 (see full text in
[LICENSES/Apache-2.0.txt](LICENSES/Apache-2.0.txt))

Dot-files are licensed under CC0-1.0 (see full text in
[LICENSES/CC0-1.0.txt](LICENSES/CC0-1.0.txt))
