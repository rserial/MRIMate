# process-3T-MRI-data: the MRIMate library

This is a Python library for processing par/rec MRI data. So far it is specific to the V-10 3T Philips scanner.

## Features
- Process par/rec MRI data into spin density and/or phase/velocity images.
- Access experiment parameters, check units/information, etc. I still need to finish updating the definition of the different parameters.
- Data can be exported to hdf5 (still need to test if the h5 was written correctly).
- Processed data can be plotted. For now only 2D or MS experiments.

## Quickstart
A Linux distribution is required. For windows users we reccomend following the [wiki guide](https://collaborating.tuhh.de/v-10/private/documentation/wiki/-/wikis/Guides/IT/Working-with-Git-using-WSL) on how to install a Windows Linux Subsystem.

1. Create a Virtual Environment: you can use `venv` or `poetry` for example. `venv` is a bit easier to use in my opinion. 

    ```python
    cd your_project_directory
    python3 -m venv myenv
    source myenv/bin/activate
    ```
    Install packages within the virtual environment using `pip`. Deactivate the environment when finished:

    ```python
    deactivate
    ```
2. Integrate with Jupyter Notebook in VSCode: Install `ipykernel` and load the environment to the notebook.

    ```python
    pip install ipykernel
    python -m ipykernel install --user --name=myenv --display-name "Python (myenv)”
    ```
3. Install the MRIMate library
    ```
    pip install git+https://collaborating.tuhh.de/v-10/private/data-evaluation/MRImate.git
    ```
4. Check the [quick demo notebook](./notebooks/quick_example.ipynb) to learn how to use it.

## Credits
Raquel - raquel.serial@tuhh.de
This package was created with [Cookiecutter][cookiecutter] and the [fedejaure/cookiecutter-modern-pypackage][cookiecutter-modern-pypackage] project template.

[cookiecutter]: https://github.com/cookiecutter/cookiecutter
[cookiecutter-modern-pypackage]: https://github.com/fedejaure/cookiecutter-modern-pypackage
