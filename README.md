# ldrpyutils
Python utils for the Linked Data Registry (https://csiro-enviro-informatics.github.io/ldrpyutils)

Persistent Link: http://doi.org/10.4225/08/5a2744c74d949 
Attribution Statement: Yu, Jonathan (2017): ldrpyutils. v1. CSIRO. Software Collection. 10.4225/08/5a2744c74d949

![Travis build](https://travis-ci.org/CSIRO-LW-LD/ldrpyutils.svg?branch=master)


## Excel2ldrGui Window-based tool
(https://csiro-enviro-informatics.github.io/ldrpyutils/index#excel2ldr)

Excel2ldrGui is a GUI front-end to Excel-to-LDR to help users upload and update content on a Linked Data Registry. 

![Excel2ldrGui screenshot](https://confluence.csiro.au/download/thumbnails/499941408/image2017-12-9_0-11-29.png?version=1&modificationDate=1512738690337&api=v2)

The standalone executables have been precompiled for Windows and Mac. [Download here](https://confluence.csiro.au/display/VOCAB/Linked+Data+Registry+tools#LinkedDataRegistrytools-Excel2ldrGui)

### Pre-requisites

1. Access to a Linked Data Registry instance, e.g. http://registry.it.csiro.au/
2. User account on a Linked Data Registry instance
3. Stub registers created on Linked Data Registry instance


### Example Excel formats

For Excel2ldrGui, you will need to use a simple excel format or a multiple-register excel format. Examples of these are providedin the  test-data repository. 

1. Single register of vocabs (i.e. simple list) - see test-data/simple.xlsx
2. Multiple registers of vocabs (i.e. one for each sheet) - see test-data/multi-register.xlsx 


## excel2ldr command line tool

### Quickstart

```
$ pip install ldrpyutils

# download starter pack
$ wget https://github.com/CSIRO-LW-LD/ldrpyutils/blob/master/quickstart/csiro-starter-pack.zip
$ unzip csiro-starter-pack.zip

# edit fields in examples/simple.xlsx to point to your register on a LDR instance
# edit config to point to your LDR instance
$ excel2ldr --user username --pass passwd examples/simple.xlsx
```


### Pre-requisites

1. Access to a Linked Data Registry instance
2. User account on a Linked Data Registry instance
3. Stub registers created on Linked Data Registry instance

#### Windows Pre-requisites

```
1. Ensure Python 3.4+ and pip is installed
2. Ensure Python and pip is added to the PATH environment variable
```

### Installing


#### Installing via pip

```
$ pip install ldrpyutils
```


#### Installing and running from source
```
# clone this git repository
$ git clone https://github.com/CSIRO-LW-LD/ldrpyutils.git
$ cd ldrpyutils

# (optional) setup a virtualenv
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt 

# install the ldrpyutils library locally
$ pip install -e .
```

### Running
```
# run excel2ldr - transform excel data to a single register of vocabs, build graph, post to a LDR registry
$ excel2ldr --user username --pass passwd  test-data/simple.xlsx

# run excel2ldr - transform excel sheets to multiple registers of vocabs, build graph, post to a LDR registry
$ excel2ldr --user username --pass passwd --multi test-data/simple.xlsx

```



### Configuration

excel2ldr expects a config.json in current dir to contain details to an instance of a Linked Data Registry.

config.json currently allows specification of registry url but might expand to include other details in the future.
```
{
   "registry_url" : "http://my-ldr-here.com"
}
```

### Example Excel formats

Examples of the excel formats are given in test-data repository. There is currently 2 formats supported for use
cases considered.

1. Single register of vocabs (i.e. simple list) - see test-data/simple.xlsx
2. Multiple registers of vocabs (i.e. one for each sheet) - see test-data/multi-register.xlsx 

