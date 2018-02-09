.. pybpodapi documentation master file, created by
   sphinx-quickstart on Wed Jan 18 09:35:10 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _installing-label:

*************
Install
*************

Install on Ubuntu 17.10
--------------------------------

* Download and install `Anaconda <https://www.anaconda.com/download/#linux>`_ or `Miniconda <https://conda.io/miniconda.html>`_
* Download the zip file containing the `code <https://github.com/UmSenhorQualquer/d-track/archive/master.zip>`_.
* Uncompress the zip file to a folder.
* Open the terminal and change the current directory to the uncompressed folder.

  .. code-block:: bash

     cd <d-track directory>

* Execute the next command in the terminal to install the python environment.

  .. code-block:: bash

     conda env create -f environment-ubuntu17.yml

* Activate the environment.

  .. code-block:: bash

     source activate py3dengine-environment

* Run the installation script.

  .. code-block:: bash

     python install.py
