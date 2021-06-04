# DNN-translator
This project is a Deep Neural Networks translator. This project mainly works with Deep Neural Networks from Computer Vision like object detection, object recognition or object segmentation models. If a model has labels that are mapped to model output this project should be able to translate the labels to a different language.
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
* -i (--inputLanguage): Language that models labels are written. Should be in form of two ascii letters. Default - en.
* -o (--outputLanguage): Language that models labels will be translated. Should be in form of two ascii letters. Default - lt.
This command accepts optional flag:
* -c (--appendConfidence): A flag that means translation confidence will be appended to each translation. Default - false.
## Usage examples
This solution was tested with [Mask-RCNN](https://github.com/matterport/Mask_RCNN) demo application. So most models which have their classes written out in code should be translated. The solution won't work with .ipynb file type, so those files should be converted to .py file type.
This solution will also try to find labels that are written in a sepparate file.
