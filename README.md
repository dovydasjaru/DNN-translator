# DNN-translator
## Instalation
### Requirements
Python version 3.7 or better. Recomended is 3.7 since the project was tested with it.
### Instalation procedure
* Install Python 3.7 or better
* git clone this repository
* run python setup.py install command
## How to use
To run this project run python main.py command.
This command accepts one required argument that is folder/file location of neural network.
This command accepts optional arguments:
* -i (--inputLanguage): Language that models labels are written. Should be in form of two ascii letters.
* -o (--outputLanguage): Language that models labels will be translated. Should be in form of two ascii letters.
This command accepts optional flag:
* -c (--appendConfidence): A flag that means translation confidence will be appended to each translation.
