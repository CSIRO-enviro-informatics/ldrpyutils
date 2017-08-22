# ldrpyutils
Python utils for the Linked Data Registry


## excel2ldr

### Quickstart

```
# (optional) setup a virtualenv
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt 

# install the ldrpyutils library locally
$ pip install -e .

# run excel2ldr - transform excel data to a single register of vocabs, build graph, post to a LDR registry
$ excel2ldr --user usename --pass passwd --verbose  test-data/simple.xlsx

# run excel2ldr - transform excel sheets to multiple registers of vocabs, build graph, post to a LDR registry
$ excel2ldr --user usename --pass passwd --verbose --multi test-data/simple.xlsx

```

### Pre-requisites

1. Access to a Linked Data Registry instance
2. User account on a Linked Data Registry instance
3. Stub registers created on Linked Data Registry instance


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

