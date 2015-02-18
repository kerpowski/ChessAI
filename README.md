Simple Chess AI
========

Credit goes to Niklas Fiekas for the python-chess module.  ChessLib.py is just a port of that with appropriate cython markup for performance reasons.

Requirements
-Python 3.3
-cython
-numpy

Easiest way to get the required libraries/binaries is by installing WinPython.  

To cythonize the python files run "python setup.py build_ext --inplace".  This is done using pure python so you can run the python without this step for debugging (it will be an order of magnitude slower however).


