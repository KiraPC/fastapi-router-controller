# pylint: disable=line-too-long
'''
    :author: Pasquale Carmone Carbone

    Setup module
'''
import os
import setuptools

with open('README.md', 'r') as fh:
    LONG_DESCRIPTION = fh.read()

with open('requirements.txt', 'r') as fin:
    REQS = fin.read().splitlines()

setuptools.setup(
    version=os.environ.get('RELEASE_VERSION'),
    name='fastapi-router-controller',
    author='Pasquale Carmine Carbone',
    author_email='pasqualecarmine.carbone@gmail.com',
    description='A FastAPI utility to allow Controller Class usage',
    long_description=LONG_DESCRIPTION,
    url='https://github.com/KiraPC/fastapi-router-controller',
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(exclude=['venv', 'fastapi-router-controller.egg-info', 'build']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development',
        'Typing :: Typed',
    ],
    python_requires='>=3.6',
    install_requires=REQS
)
