This is a test implementation of a virtual environment management tool using Python.

As presented, the problem is:
We want to be able to have a central application that can have different packages, modules, tools, etc involved that can be enabled or disabled.
Each tool should be accessible from the central application depending on if it is installed.
A CLI tool might be able to invoke the packages with some wrapper functionality. A GUI tool might act as a workbench software with buttons/plugins for each tool.

For instance, it might have compatibility for two tools:
DeepMRSeg (deep learning based segmentation, lots of dependencies)
pyHYDRA (another python module developed at CBICA)


Each of these are "installable packages". 
But users should be able to pick and choose. Our central application should not have a "hard" dependency on any of those tools.


AT INSTALL TIME:
The central application should iterate over all installable packages and ask the user if they wish to install each.
For each selected package, the central application will create a virtual environment for that package and install any necessary dependencies into it.

AT RUN TIME:
The central application should be able to detect which of the installable tools are installed/present/available.
It should also be able to invoke these tools as directly as possible with their corresponding environments.
For example, if DeepMRSeg requires numpy 1.18.4 and pyHYDRA requires numpy 1.20.2, this is an irreconcilable dependency, so they cannot be run (reliably) in the same environment.
The central app should be able to dynamically load the environments created at install time to execute each package appropriately when requested by the user.


In essence: We need to be able to run any number of packages that require different dependencies/versions. 
Ideally, invoking the installed tools should be as painless and seamless as possible.
It is probably not possible (or, at least, a good idea) to do this all in the form of single-process Python code.
Instead we can run each tool in a separate Python process, using the various mechanisms Python has in place to load environments dynamically.

Several mechanisms exist. See https://stackoverflow.com/questions/23678993/automatically-load-a-virtualenv-when-running-a-script/23762093 for some.
1. Changing the PYTHONPATH variable before runtime to change search directories.
2. Changing PYTHONPATH or sys.path from inside a script to prepend the search directories.
3. If you directly run a script or the python interpreter from the virtualenv’s bin/ directory (e.g. path/to/env/bin/pip or /path/to/env/bin/python script.py) there’s no need for activation.
4. Put the name of the virtual env python into first line of some kind of wrapper script, like this: #!/your/virtual/env/path/bin/python
5. See this: https://stackoverflow.com/a/23845366 (Basically use execfile to call the virtual environment's activation)


