Set up immuneML for development
----------------------------------
Prerequisites:

- Python 3.8: it might work with other python versions (3.7 or 3.6), but might require additional packages to be manually installed (e.g., dataclasses package if running immuneML with Python 3.6). Alternatively, a custom python interpreter can be assigned to the virtual environment (in PyCharm, for development purposes, or in a conda environment).

- Optionally R 3.6.x with libraries Rmisc and readr and library ggexp (which cannot be installed directly with conda, but can be installed with devtool library from `the GitHub repository <https://github.com/keshav-motwani/ggexp>`_). See :ref:`When should I install immuneML with R dependencies?`

Note: for development purposes, it is much more convenient to clone the codebase using PyCharm. To set up the project in PyCharm, see
`the official JetBrains tutorial for creating a PyCharm project from an existing GitHub repository <https://www.jetbrains.com/help/pycharm/manage-projects-hosted-on-github.html>`_.
Alternatively, the following 5 steps describe how to perform the process manually.

Steps:

1. Create a directory where the code should be located and navigate to that directory.

2. Execute the command to clone the repository:

.. code-block:: console

  git clone https://github.com/uio-bmi/immuneML.git

3. Create and activate a virtual environment as described here
https://docs.python.org/3/library/venv.html (python virtual environment)
or use conda instead with python 3.8.

4. From the project folder (immuneML folder created when the repository was cloned
from GitHub), install the requirements from the requirements.txt file (this file can be found in the immuneML root folder):

.. code-block:: console

  pip install -r requirements.txt

See also this FAQ: :ref:`When installing all requirements from requirements.txt, there is afterward an error with yaml package (No module named yaml)?`.

If you want to install optional requirements (to use R for plotting, DeepRC or TCRdist), install the corresponding requirements files (some or all of them):

.. code-block:: console

  pip install -r requirements_R_plots.txt
  pip install -r requirements_DeepRC.txt
  pip install -r requirements_TCRdist.txt

5. If not setting up the project in PyCharm, it is necessary to manually add the root project folder to PYTHONPATH. The syntax for Unix-based systems is the following:

.. code-block:: console

  export PYTHONPATH=$PYTHONPATH:/<path_to_immuneML_project_root>

To run a sample analysis, from the project folder run:

.. code-block:: console

  python3 source/workflows/instructions/quickstart.py
