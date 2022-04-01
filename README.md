# YAMLHParams
A small extension to the `ruamel.yaml` `CommentedMap` YAML parser class (see [https://yaml.readthedocs.io/en/latest/](https://yaml.readthedocs.io/en/latest/)). 
This extension enables access to and manipulation of hyperparameters stored in YAML files using hierarchical/path-like 
(`/path/to/value`) lookups of attributes and may perform simple version controlling against a separate 
Python package and its parent folder `git` repository. Changes made to the hyperparameters in memory can be easily written to disk preserving comments and 
order of YAML blocks.

The intended usage is for e.g. machine learning research projects for maintaining a consistent set of hyperparameters 
on-disk and in-memory while keeping track of the software version used to run a given set of experiments.

## Installation
```bash
pip install yamlhparams
```

## Examples
Given a file `hyperparameters.yaml` with content:

```yaml
fit:
  n_epochs: 100
  loss_function:  # Some comment
    class: cross_entropy
    kwargs:
      class_weights: [1.5, 0.4, 2.0]
  optimizer:
    learning_rate: 1e-5

logging:
  path: /my/path
  level: WARNING
```

Loading and accessing hyperparameters using typical dictionary lookup or hierarchical `/path/to/value` styles and 
performing version control against a 3rd party package `my_ml_package`:
```python
from yamlhparams import YAMLHParams
hparams = YAMLHParams('hyperparameters.yaml', 
                      version_control_package_name='my_ml_package')
print(hparams['logging']['level'])
>> WARNING

print(hparams.get_group('/fit/loss_function/class'))
>> cross_entropy

print(hparams.get_group('/fit/optimizer'))
>> ordereddict([('learning_rate', 1e-05)])
```

Adding/deleting groups to/from the hyperparameter file:
```python
hparams.set_group('/data/splits', {'train_inds':[1, 4, 6], 
                                   'test_inds': [2, 3, 5]}, 
                  missing_parents_ok=True)

hparams.delete_group('/logging')

# Save changes to file, preserving comments and order
hparams.save_current()
```

The modified file now has the following content:

```yaml
__package_info__:
  package: my_ml_package
  version: 0.1.0
  git:
    commit: 31dd454
    branch: main

fit:
  n_epochs: 100
  loss_function:  # Some comment
    class: cross_entropy
    kwargs:
      class_weights: [1.5, 0.4, 2.0]
  optimizer:
    learning_rate: 1e-5

data:
  splits:
    train_inds:
    - 1
    - 4
    - 6
    test_inds:
    - 2
    - 3
    - 5
```

Loading the same hyperparameter file with the installed `my_ml_package` later 
updated to version `0.2.0` will raise a `RuntimeWarning`:

```
[...]
RuntimeWarning: Parameter file indicates that this project was created under 
                my_ml_packagae version 0.1.0, but the current version is 0.2.0. 
                If you wish to continue using this software version on this project dir, 
                manually update to the following lines in the hyperparameter file:

__package_info__:
  version: 0.2.0
```
