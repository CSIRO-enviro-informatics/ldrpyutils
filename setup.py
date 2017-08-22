#from distutils.core import setup
from setuptools import setup


setup(
    name='ldrpyutils',
    version='0.2',
    packages=['ldrpyutils'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Linguistic',
      ],
    keywords='linked-data vocabularies excel linked-data-registry skos',
    url='https://github.com/CSIRO-LW-LD/ldrpyutils',
    license='MIT',
    author='Jonathan Yu',
    author_email='jonathan.yu@csiro.au',
    description='Python utils for the Linked Data Registry',
    install_requires=[
                  'openpyxl',
                  'rdflib',
                  'requests'
                        ],
    entry_points={
        'console_scripts': ['excel2ldr=ldrpyutils.core:excel2ldr'],
    },
    include_package_data=True
)
