# Automatically configure the .vscode ```.json``` files for the nRF5 SDK

This repository has the necessary ```.json``` files to edit, build and debug nRF5 SDK projects in Visual Studio Code. It has a python script, which reades all ```include directories``` and ```defines``` from the project's makefile and automatically updates the ```.json``` files so that ```IntelliSense``` works.

## Usage
Clone the repository to your project's workspace directory (e.g. ```SDK_ROOT\examples\peripheral\blinky```):
```
git clone https://github.com/yannidd/.vscode-nrf5-sdk
```
Rename the ```.vscode-nrf5-sdk``` directory to ```.vscode```:
```
ren .\.vscode-nrf5-sdk\ .vscode
```
Open ```generate_properties.py``` and change ```proj_dir``` to match the directory that contains the ```armgcc``` and ```config``` folders (e.g. ```'pca10040/s132'```).

Now run the ```generate_properties.py``` script:
```
py .\.vscode\generate_properties.py
```

## Notes
- This will only work on Windows, but can be easily adapted to other OS.
- This has been tested on nRF52 SDK 15.2.0. For the script to work without modifications, it is assumed that the projects are located in ```SDK_ROOT\examples\some_folder\some_folder```
- You should have the required packages for building and flashing the device. I will add links to these if I have time.
- If you find a bug, please send me an e-mail and I will try to fix it.
