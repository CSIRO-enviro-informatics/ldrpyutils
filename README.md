# ldrpyutils
Python utils for the Linked Data Registry

Persistent Link: http://doi.org/10.4225/08/5a2744c74d949 
Attribution Statement: Yu, Jonathan (2017): ldrpyutils. v1. CSIRO. Software Collection. 10.4225/08/5a2744c74d949

## excel2ldr

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
1. Ensure Python 2.7 and pip is installed
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
$ virtualenv venv
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

