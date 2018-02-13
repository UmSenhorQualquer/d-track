.. pybpodapi documentation master file, created by
   sphinx-quickstart on Wed Jan 18 09:35:10 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _installing-label:

******************
Run D-Track
******************

|

.. note::
    
    Please make sure you have installed the environment before trying to execute the application.


Windows mode
--------------------------------

* Open the terminal and execute the next command in the terminal to activate the environment.

  .. code-block:: bash

     source activate py3dengine-environment

* Execute the next command to open the Tracking application.

  .. code-block:: bash

     d-track-singlecam

* Or execute the next command to open the Smooth Path application.

  .. code-block:: bash

     d-track-smoothpath

* Execute the next command to open the Render application.

  .. code-block:: bash

     d-track-render


.. image:: /_static/singlecam.png

--------------------------- 

|

Batch/Terminal mode
----------------------------------------------

Executing the software in batch mode is useful to analyse the videos on a computational cluster or to configure analysis to run one after each other using a shellscript.

To activate the batch mode, thanks to the `PyForms <https://pyforms.readthedocs.io>`_ framework, you just need to add the next 2 parameters to the applications calls.

.. code-block:: bash

   d-track-singlecam terminal_mode --exec execute

or

.. code-block:: bash

   d-track-smoothpath terminal_mode --exec execute

or

.. code-block:: bash

   d-track-render terminal_mode --exec execute


More parameters
==========================

Call the command **help** to now which parameters you can use more.

.. code-block:: bash

   d-track-smoothpath terminal_mode --help


.. image:: /_static/batch-help.png


Full commands examples:

.. code-block:: bash
   
   d-track-singlecam terminal_mode --_sceneFile 04Hugo201302211037_Scenario.obj --_video 04Hugo201302211037MergedEntrada.MP4 --_camera Camera1 --_blockSize1 1001 --_cValue1 296 --_blockSize2 1001 --_cValue2 297 --_blockSize3 1001 --_cValue3 297 --_range 13500,105249 --exec execute

   d-track-singlecam terminal_mode --_sceneFile 04Hugo201302211037_Scenario.obj --_video 04Hugo201302211037MergedCascata.MP4 --_camera Camera2 --_blockSize1 1001 --_cValue1 277 --_blockSize2 1001 --_cValue2 277 --_blockSize3 1001 --_cValue3 277 --_range 13500,105249 --exec execute

   d-track-render terminal_mode --_sceneFile 04Hugo201302211037_Scenario.obj --_video0 04Hugo201302211037MergedEntrada.MP4 --_video1 04Hugo201302211037MergedCascata.MP4 --_data output/04Hugo201302211037_Scenario_3d_tracking.csv --_outputfile test.avi --exec execute