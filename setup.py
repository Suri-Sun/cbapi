from setuptools import setup, find_packages
import io
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with io.open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='cbapi',
    version='0.0.1',
    description='Crunchbase business information downloader',
    long_description=long_description,
    url='https://github.com/Suri-Sun/cbapi',
    author='Tongtong (Suri) Sun',
    author_email='suri.g.sue@gmail.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Development Status :: 3 - Alpha',

        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Office/Business :: Financial',
        'Topic :: Office/Business :: Financial :: Investment',
        'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',

        'Programming Language :: Python :: 3',
    ],
    platforms=['any'],
    keywords='pandas, Crunchbase',
    packages=find_packages(),
    install_requires=['pandas>=0.24', 'numpy>=1.15',
                      'requests>=2.20', 'multitasking>=0.0.7'],
)