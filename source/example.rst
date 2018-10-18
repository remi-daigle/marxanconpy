
New Projects
============

The first step is to import the package and create a MarCon dictionary.
This is one giant dictionary that contains all required options,
filepaths, etc. These can also be produced using the GUI `Marxan
Connect <marxanconnect.ca>`__

.. code:: ipython2

    import marxanconpy
    import os
    
    project = marxanconpy.marcon.new_project()
    

Load Projects
-------------

We can also load pre-existing ``.MarCon`` files

.. code:: ipython2

    path = os.path.dirname(marxanconpy.__file__)
    project = marxanconpy.marcon.load_project(os.path.join(path,'data','CF_demographic','tutorial.MarCon'))
    


.. parsed-literal::

    Warning: This project file was created with a different version of Marxan Connect. Attempting to update for compatibility
    Warning: This project file does not contain all the required fields (marxan). Attempting to update for compatibility
    

Editing Projects
----------------

.. code:: ipython2

    project['filepaths']['aa_filepath'] = "path\to\file.shp"

Saving Projects
---------------

.. code:: ipython2

    ## Preparing Connectivity Data
    
    ## Calculating Metrics
    
    ## Running Marxan
    
    ## Posthoc
