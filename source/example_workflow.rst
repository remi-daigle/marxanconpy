Workflow
========

In this section, it is assume you have create a ``.Marcon`` project
dictionary. If you haven't, please see the `MarCon
projects </docs/example_marcon.html>`__ section

.. code:: ipython3

    import marxanconpy
    import os
    
    path = os.path.dirname(marxanconpy.__file__)
    project = marxanconpy.marcon.load_project(os.path.join(path,'data','CF_demographic','tutorial.MarCon'))
    

Preparing Connectivity Data
---------------------------

Calculating Metrics
-------------------

Running Marxan
--------------

Posthoc
-------
