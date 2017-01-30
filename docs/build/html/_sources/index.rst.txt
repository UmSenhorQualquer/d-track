.. d-tracker documentation master file, created by
   sphinx-quickstart on Mon Jan 30 09:40:02 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

D-Track
=====================================

D-Track is a software that is part of a system used to track objects in a whater pool.

The system is composed by 2 GoPro Hero 2 cameras that synchronize the records.


.. image:: /_static/poll-reconstruction.png


Downloads
---------------------------------

====================	====================================================
Windows binaries		`here <http://opencv.org/downloads.html>`_ 
====================	====================================================


Requirements
--------------------------------

The software was developed and tested with the operating system Ubuntu 14.04.5 LTS (Trusty Tahr).

====================	=============
**LIBRARY**				  **VERSION**
Python 					        2.7.6
Numpy 					        1.8.2
OpenCV 					        3.1.0
PyOpenGL 				      3.1.1a1
PyOpenGL_accelerate 	      3.1.1a1
PyForms 				    v1.0.beta
csv 					          1.0
py3dengine				          0.0
====================	=============


Installation and execution
---------------------------------

From the binaries
____________________________

Installation
~~~~~~~~~~~~~~~~~~~~~~

* Download the windows binaries.
* Uncompress them for indevidual folders.

Run the applications
~~~~~~~~~~~~~~~~~~~~~~

* Execute the executable file (*.exe) from each forlder.


From the source code
____________________________

Installation
~~~~~~~~~~~~~~~~~~~~~~

* Ubuntu already comes with python 2.7 installed, therefore there is not need to install python.
* Download and install the source code of Numpy 1.8.2 `here <https://sourceforge.net/projects/numpy/files/NumPy/1.8.2/>`_ . 
* Download the OpenCV library from the `opencv.org <http://opencv.org/downloads.html>`_ website, and follow the instructions to compile and install it with cmake.
* Execute the command: ``sudo pip2.7 install pyopengl pyopengl_accelerate``.
* Follow the instructions located `here <pyforms.readthedocs.io/en/v1.0.beta/>`_ to install PyForms.
* Install the csv library using the command: ``sudo pip install csv==1.0``.
* Install the py3dengine library using the command: ``sudo pip install git+https://UmSenhorQualquer@bitbucket.org/UmSenhorQualquer/py3dengine.git``.
* Download an uncompress the d-tracker source code and install it using pip: ``sudo pip install .``

Run the applications
~~~~~~~~~~~~~~~~~~~~~~

On the terminal execute the command ``d-tracker-singlecam`` or the ``d-tracker-smoothpath``.



User manual
---------------------------------

d-tracker-singlecam
____________________________

This application is used to segment the images of each camera and find the dolphin in the pool.

.. image:: /_static/singlecam.png

d-tracker-smoothpath
____________________________

This application is used merge the output of the **d-tracker-singlecam** application of the 2 cameras.

.. image:: /_static/smoothpath.png