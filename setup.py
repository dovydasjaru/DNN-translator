from setuptools import setup

setup(
    name='Translator',
    version='1.0',
    packages=[''],
    url='',
    license='',
    author='Dovydas Jaru',
    author_email='',
    description='Tool for translating Deep Neural Networks outputs',
    classifiers=['Programming Language :: Python :: 3.7'],
    install_requires=['textblob', 'requests', 'beautifulsoup4'],
    python_requires='>=3.6',
    package_data={'': ['en_lt.csv']},
)
