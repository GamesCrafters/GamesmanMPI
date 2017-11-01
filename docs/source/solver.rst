Using the Solver
================

Basic Usage
^^^^^^^^^^^

Games to be solved are loaded via the command line, with the following syntax:

::

    mpiexec -n <number of processes> python solver_launcher.py <your game file>


For example, you could load our example game, Four-To-One, by running

::

    mpiexec -n 5 python solver_launcher.py test_games/four_to_one.py

Your game file must follow the conventions outlined in the API

The Solver for Developers
^^^^^^^^^^^^^^^^^^^^^^^^^
