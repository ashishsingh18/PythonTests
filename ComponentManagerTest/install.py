# This file serves as an install-time script that asks the user whether they'd like to install each sub-component.
# For our example we'll ask the user to install DeepMRSeg and/or pyHYDRA. They might enable either, neither, or both.
# For each selected component, we will:
# 1. create a corresponding python virtual environment and 
# 2. install any necessary packages/dependencies to that environment, then
# 3. mark that component as available to the central application and 
# 4. perform any setup needed to expose it in the CLI/GUI.
# Steps 3 and 4 can be empty placeholders for now, but as the application develops they will probably need extension.
# 

# The contents of this file might be placed in a custom install command in setup.py (with some slight edits)...
# or an external installer could just run this script directly. 

import venv
import argparse
import platform
from pathlib import Path
import os

def buildVenv(component):
    # See https://docs.python.org/3/library/venv.html#api for a general idea
    
    # Install the venv ALONGSIDE the **currently running script**.
    env_dir = str(Path(__file__).parent) + "/" + component
    builder = venv.EnvBuilder(system_site_packages=False, clear=True, symlinks=False, 
                    upgrade=False, with_pip=True)
                    
    builder.create(env_dir)
    
    # Now install the package itself to that venv. (We might eventually need to break this out to a separate script per tool.)
    # TODO: Double check this for cross-platform compatibility, "Scripts" and "bin" may differ.
    # Might need to change environment variables here too.
    system_call = str(os.path.abspath(env_dir) + "/Scripts/python -m pip install " + component)
    print(system_call)
    os.system(system_call)
    
    # Any post install steps go here like checking for errors or performing configuration.
    
    
def buildCondaEnvironment(component):
    pass #TODO for conda usage. Not sure if this is actually strictly required but it might be nice.
    
def buildComponent(component, use_conda=False):
    if use_conda:
        buildCondaEnvironment(component)
    else:
        buildVenv(component)
    

# This can be filled from an external file or something
allInstallableComponents = ["DeepMRSeg", "pyHYDRA", "numpy"]

# Just ask the user and get the list to install
toBeInstalled = []
for component in allInstallableComponents:
    response = input("Would you like to install " + component + " and all related plugins? (Y/N): ")
    if (response == "Y"):
        toBeInstalled.append(component)
        
for component in toBeInstalled:
    print("Installing " +  component + " component...")
    buildComponent(component)
    print("Done.")
    

print("Finished installation.")
   





