Cite as: Yu, Jonathan (2017): ldrpyutils. v1. CSIRO. Software Collection. 10.4225/08/5a2744c74d949
Persistent Link: http://doi.org/10.4225/08/5a2744c74d949 

## ldrpyutils

A python library for interfacing with the Linked Data registry

## <a name="excel2ldr"></a> Excel2ldr 

Preparing and uploading vocabulary content to a [Linked Data Registry](http://ukgovld.github.io/ukgovldwg/guides/registry.html) service, e.g. [the CSIRO Linked Data Registry](http://registry.it.csiro.au/), can be tricky and at times requires knowledge of tools such as `curl`, `RDF editors`, and concepts such as `HTTP` and `REST`. 

`Excel2LDR` is a small component that streamlines the creation and revision of vocabulary content on any Linked Data Registry (LDR) service based on Excel templates that are compatible with it. It provides a GUI front-end to help users upload and update content on the LDR. We currently only support Windows. (Please [raise a Github issue](https://github.com/CSIRO-enviro-informatics/ldrpyutils/issues/new) if you would like a Mac version!)

![Excel2ldr screenshot](https://confluence.csiro.au/download/thumbnails/499941408/image2017-12-9_0-11-29.png?version=1&modificationDate=1512738690337&api=v2)

Downloads:
* Excel2LDR for Windows. [Download here](https://confluence.csiro.au/download/attachments/499941408/Excel2ldrGui.exe?version=6&modificationDate=1519124121550&api=v2)

### Pre-requisites
* Access to a Linked Data Registry instance, e.g. http://registry.it.csiro.au/
* User account on a Linked Data Registry instance
* Stub registers created on Linked Data Registry instance

### Quick start

Steps:
1. Download the Excel2LDR Excel Template - see [simple.xlsx](https://github.com/CSIRO-LW-LD/ldrpyutils/raw/master/test-data/simple.xlsx)

2. Extend this with your content and save the file

Using the simple template, fill in details of the 'registerinfo' sheet with appropriate values in Column B. This info includes an id, a descriptive (short) label, a description (long form), the URL for the register location, source notes, and maintainer.

![Excel template registerinfo](https://confluence.csiro.au/download/attachments/499941408/excel2ldr-template0.JPG?version=1&modificationDate=1527058110238&api=v2)


In the second Excel sheet, extend/customise the content to include your vocabulary terms. Each row represents a term or SKOS concept.

The 'id' field is special as it mints the unique identifier for the concept in the register - this is mandatory and must be unique! 

Fill in all the other fields, noting that they are optional (but it would be useful if they were filled out!).

The 'broader' field provides users with the ability to link terms/concepts to broader concepts. The values expected are either a) the id of other concepts in the sheet; or b) a URL which represents the broader concept (perhaps from another register).

![Excel template content](https://confluence.csiro.au/download/attachments/499941408/excel2ldr-template1.JPG?version=1&modificationDate=1527058110310&api=v2)

3. Download the Excel2LDR tool 

4. Open the Excel2LDR application

5. Enter in the Excel file and your account username and password

![Excel template content](https://confluence.csiro.au/download/thumbnails/499941408/excel2ldr-screenshot.JPG?version=1&modificationDate=1527059344860&api=v2)

6. Submit and Done!


### Excel templates

You will need to use a simple excel format or a multiple-register excel format. Examples of these are provided in the test-data folder of the Github repository. Extend these to suit your content. We have endeavoured to add comments in the Excel template to guide users on what content to enter in which cell/column. If you find bug or problems, please [raise a Github issue](https://github.com/CSIRO-enviro-informatics/ldrpyutils/issues/new)

#### Single register of vocabs (i.e. simple list) 

This allows users to create a single register to contain a simple vocabulary with a flat list of terms. The list of terms may relate to each other referencing using the broader column. This is the simplest to get going with.

See [test-data/simple.xlsx](https://github.com/CSIRO-LW-LD/ldrpyutils/raw/master/test-data/simple.xlsx)

#### Multiple registers of vocabs (i.e. one for each sheet)

This allows users to create and maintain multiple lists of vocabulary registers. Excel2LDR uploads and updates all of them at the same time. This is suited for situations where you would like to maintain a file for a number of vocabularies.

See [test-data/multi-register.xlsx](https://github.com/CSIRO-LW-LD/ldrpyutils/raw/master/test-data/multi-register.xlsx)


`Excel2LDR` uses the underlying `ldrpytils` Python code library to create the RDF/SKOS content, authenticate to an LDR instance and push content to the specified registry.


## <a name="excel2ldr-commandline"></a> Excel2ldr Command Line Edition

Don't need a GUI interface? Perhaps you would like to create a CRON job to regularly update your vocabulary content? The command line edition of Excel2LDR is for you! 

This is essentially the same tool as the GUI edition, but in a command line form. See below for instructions to get started.

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
