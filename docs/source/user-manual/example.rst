**********
Example
**********

.. note::

   .. image:: https://about.zenodo.org/static/img/logos/zenodo-gradient-round.svg
      :width: 200 px
      :align: right

   Download the files for this example `here <http://doi.org/10.5281/zenodo.1253284>`_.

   This example execute the applications in terminal mode.  


* First use the command **d-track-singlecam** to extract from each camera the dolphin positions pixel positions.


.. code-block:: bash
   
   d-track-singlecam terminal_mode --_sceneFile 04Hugo201302211037_Scenario.obj --_video camera1.mp4 --_camera Camera1 --_blockSize1 1001 --_cValue1 296 --_blockSize2 1001 --_cValue2 297 --_blockSize3 1001 --_cValue3 297 --_range 0,17965 --exec execute

   d-track-singlecam terminal_mode --_sceneFile 04Hugo201302211037_Scenario.obj --_video camera2.mp4 --_camera Camera2 --_blockSize1 1001 --_cValue1 277 --_blockSize2 1001 --_cValue2 277 --_blockSize3 1001 --_cValue3 277 --_range 0,17965 --exec execute


* Use the **d-track-smothpath** to combine both cameras pixels positions and estimate the dolphin 3d position.

.. code-block:: bash
   
   d-track-smoothpath terminal_mode --_scenefile 04Hugo201302211037_Scenario.obj --_trackfile0 output/camera1_out.csv --_trackfile1 output/camera2_out.csv --_refraction_index 1.4 --exec execute

* Render the result with the **d-track-render** command.

.. code-block:: bash

   d-track-render terminal_mode --_sceneFile 04Hugo201302211037_Scenario.obj --_video0 camera1.mp4 --_video1 camera2.mp4 --_data output/04Hugo201302211037_Scenario_3d_tracking.csv --_outputfile test.avi --exec execute


.. image:: /_static/d-track-render-scene.png


Example of a video rendered with the software.

.. raw:: html
   
   <iframe width="700" height="270" src="https://www.youtube.com/embed/Wk2oMkCNSoM?rel=0&amp;showinfo=0" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>