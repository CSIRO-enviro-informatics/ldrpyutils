from openpyxl import load_workbook
import rdflib
from rdflib import RDFS, RDF, URIRef, Literal
from rdflib.namespace import NamespaceManager, Namespace
import requests
import json
import argparse
import pkg_resources

DATA_PATH = pkg_resources.resource_filename("ldrpyutils", 'data/')

def load_simple_file(excel_file,  user=None, passwd=None, emitFile=False, registry_auth_url=None,
                     updateOnlineRegisters=False,
                     verbose=False):
    wb = load_workbook(excel_file)

    if verbose:
        print wb.get_sheet_names()

    sheetsDict = {}
    reginfo_ws = False
    for sheet in wb:
        sheetname = sheet.title
        if sheetname == 'registerinfo':
            reginfo_ws = sheet

        else:
            regitems_ws = sheet
            sheetsDict[sheetname] = regitems_ws

    #process the register info
    reginfo_obj = get_registerinfo(reginfo_ws)

    #process the register items
    regitems_obj = process_all_registeritems_in_dict(sheetsDict)

    if verbose:
        print reginfo_obj
        print regitems_obj


    (g, status) = build_graph_and_post(reginfo_obj, regitems_obj,
                        user=user, passwd=passwd,
                        emitFile=emitFile,
                        registry_auth_url=registry_auth_url,
                        updateOnlineRegisters=updateOnlineRegisters,
                        verbose=verbose
                        )
    if verbose:
        print status
    return True

def get_registerinfo(ws):
    if ws == False:
        return False

    registerinfo_obj = parse_sheet(ws)

    result = {}
    for key, value in registerinfo_obj['items']:
        result[key] = value

    return result



def process_all_registeritems_in_dict(sheetsDict, verbose=False):
    if sheetsDict == False:
        return False

    regItemsObj = {}
    for registerid, ws in sheetsDict.iteritems():
        res = get_registeritems(registerid, ws, verbose=verbose)
        arrResults = []
        for i, rowvalues in enumerate(res['items']):
            result = {}

            for j, cellvalues in enumerate(rowvalues):
               key = res['header'][j]
               result[key] = cellvalues
            arrResults.append(result)
        regItemsObj[registerid] = arrResults

    return regItemsObj

def get_registeritems(registerid, sheet, verbose=False):
    if verbose:
        print "reg id: " + registerid
    return parse_sheet(sheet)


def parse_sheet(sheet):
    # parse header
    first_row = sheet[1]
    header = []
    for cell in first_row:
        #print cell.value
        header.append(cell.value)

    count = 0
    arrItems = []
    for row in sheet.iter_rows():
        count = count + 1

        if count > 1:
            currArr = []
            for cell in row:
                #print cell.value
                currArr.append(cell.value)

            arrItems.append(currArr)

    result = {}
    result['header'] = header
    result['items'] = arrItems
    return result

def build_graph_and_post(reginfo_obj, regitems_obj,
                user=None, passwd=None, mode='single', emitFile=False,
                registry_auth_url=None,
                updateOnlineRegisters=False,
                verbose=False):
    if reginfo_obj == False or regitems_obj == False :
        return False


    ns_prefix_lookup = {
        "description" : 'dct',
        "definition": 'skos',
        "notation": 'reg',
        "note": 'skos',
        "label" : 'rdfs',
    }

    prefixes_g = rdflib.Graph()
    if verbose:
        print "Prefix file..."
    PREFIX_FILE = pkg_resources.resource_filename("ldrpyutils", 'data/prefixes.ttl')
    if verbose:
        print PREFIX_FILE
    prefixes_g.parse(PREFIX_FILE, format="ttl")
    nsMgr = NamespaceManager(prefixes_g)

    all_ns = [n for n in nsMgr.namespaces()]
    prefix_idx = {}
    for prefix, namespace in all_ns:
        #print (prefix, namespace.n3())
        prefix_idx[prefix] = Namespace(namespace)


    g = None
    status = {
        "didEmitFile" : False,
        "didUpdateOnlineRegisters": False,
    }
    if mode == 'single':
        register_id = reginfo_obj['id']
        register_url = reginfo_obj['registry_location']

        g = get_register_graph(register_id, reginfo_obj, regitems_obj[register_id], nsMgr, prefix_idx, ns_prefix_lookup)
        data = g.serialize(None,format='turtle')
        if verbose:
            print "Outputting graph for " + register_id
            print data
        if emitFile or updateOnlineRegisters:
            filename = register_id + ".ttl"
            g.serialize(filename, format="turtle")
            status['didEmitFile'] = True
            if updateOnlineRegisters:
                # use the file to update the registers
                resFlag = post_update_to_online_register(register_id, register_url, data,
                                               registry_auth_url=registry_auth_url,
                                               user=user, passwd=passwd,
                                               verbose=verbose
                                               )
                status['didUpdateOnlineRegisters'] = resFlag


    else:
        #assume multi register
        for key in reginfo_obj:
            register_id = key
            register_url = reginfo_obj[key]['registry_location']
            g = get_register_graph(register_id, reginfo_obj[key], regitems_obj[key], nsMgr, prefix_idx, ns_prefix_lookup)
            data = g.serialize(format='turtle')
            status['didEmitFile'] = True
            if verbose:
                print data
            if emitFile:
                filename = register_id + ".ttl"
                g.serialize(filename, format="turtle")
                if updateOnlineRegisters:
                    #use the file to update the registers
                    resFlag = post_update_to_online_register(register_id, register_url, data,
                                                   registry_auth_url=registry_auth_url,
                                                   user=user, passwd=passwd,
                                                    verbose=verbose
                                                   )
                    status['didUpdateOnlineRegisters'] = resFlag

    return (g, status)



def get_register_graph(register_id, register_info, register_items, nsMgr, prefix_idx, ns_prefix_lookup):
    DCT = prefix_idx['dct']
    SKOS = prefix_idx['skos']
    REG = prefix_idx['reg']

    #register = URIRef(register_id)
    #registerNsStr = URIRef(register_id + "/")
    #registerNs = Namespace(registerNsStr)
    #nsMgr.bind(register_id, registerNsStr)

    g = rdflib.Graph(namespace_manager=nsMgr)

    #g.add((register, RDF.type, URIRef(REG.Register)))
    #g.add((register, RDF.type, SKOS.Collection))
    #g.add((register, RDFS.label, Literal(register_info['label'])))
    #g.add((register, DCT.description, Literal(register_info['description'])))

    # process items
    arrConcepts = []
    items_data = register_items
    for item in items_data:
        concept = URIRef(str(item['id']))
        g.add((concept, RDF.type, SKOS.Concept))

        #g.add((register, RDFS.member, concept))

        arrConcepts.append(concept)
        for key in item:
            if key != 'id':
                # get prefix
                currPrefix = ns_prefix_lookup[key]
                currNs = prefix_idx[currPrefix]
                g.add((concept, currNs[key], Literal(item[key])))
    return g

def post_update_to_online_register(register_id, register_url, data, registry_auth_url=None, user=None, passwd=None,
                                   verbose=False):
    s = requests.Session()
    r = s.post(registry_auth_url, data={'userid': user, 'password': passwd})

    resFlag = False

    if verbose:
        print r.status_code
        print r.text
        print r.cookies.get_dict()

    if r.status_code == 200:
        #upload the data
        url = register_url
        headers = {"Content-Type": "text/turtle"}
        if verbose:
            print s.cookies.get_dict()

        r=s.post(url, data=data, headers=headers)
        if verbose:
            print r.status_code
        if r.status_code == 403:
            #force update
            url = register_url + "?edit"
            headers = {"Content-Type": "text/turtle"}
            if verbose:
                print s.cookies.get_dict()

            r = s.post(url, data=data, headers=headers)
            if r.status_code == 204:
                resFlag = True
            if verbose:
                print r.status_code
    return resFlag

def load_multi_register_file(excel_file, user=None, passwd=None, emitFile=False, registry_auth_url=None,
                             updateOnlineRegisters=False,
                             verbose=False):
    wb = load_workbook(excel_file)
    if verbose:
        print wb.get_sheet_names()

    sheetsDict = {}
    reginfo_ws = False
    for sheet in wb:
        sheetname = sheet.title
        if sheetname == 'registerinfo':
            reginfo_ws = sheet

        else:
            regitems_ws = sheet
            sheetsDict[sheetname] = regitems_ws

    #process the register info
    reginfo_obj = get_registerinfo_multi_register(reginfo_ws)

    #process the register items
    regitems_obj = process_all_registeritems_in_dict(sheetsDict, verbose)

    if verbose:
        print reginfo_obj
        print regitems_obj


    #build the graph
    (g, status) = build_graph_and_post(reginfo_obj, regitems_obj, user=user, passwd=passwd, mode='multi',
                        emitFile=emitFile, registry_auth_url=registry_auth_url,
                        updateOnlineRegisters=updateOnlineRegisters,
                        verbose=verbose)
    if verbose:
        print status
    return True

def get_registerinfo_multi_register(ws):
    if ws == False:
        return False

    registerinfo_obj = parse_sheet(ws)

    d = []
    for row in registerinfo_obj['items']:
        item = {}
        for i, elem in enumerate(row):
            item[registerinfo_obj['header'][i]] = elem
        d.append(item)

    result = {}
    for item in d:
        if item['Register_id'] in result:
            result[item['Register_id']][item['Register_property']] = item['Register_property_value']
        elif item['Register_id'] == None or item['Register_id'] == "":
            #do nothing
            abc = 123
        else:
           result[item['Register_id']] = {}
           result[item['Register_id']][item['Register_property']] = item['Register_property_value']
    return result

def excel2ldr():
    parser = argparse.ArgumentParser(description='Convert netCDF metadata to RDF.')
    parser.add_argument('--user', action="store", dest="user", default=None, help="User name to authenticate with registry")
    parser.add_argument('--pass', action="store", dest="passwd", default=None, help="Password to authenticate with registry")
    parser.add_argument('--no-emitfiles', action="store_true", dest="noEmitFile", default=False, help="Flag to specify not to emit files")
    parser.add_argument('--multi', action="store_true", dest="isMulti", default=False, help="Flag to indicate whether the file contains multiple registers to update")
    parser.add_argument('--staging-only', action="store_true", dest="stagingOnly", default=False, help="Flag to stage outputs without pushing updates to registry")
    parser.add_argument('--registry-url', action="store", dest="registryUrl", default=None, help="Override and use this registry url instead")
    parser.add_argument('--verbose', action="store_true", dest="isVerbose", default=False, help="Flag to specify verbose output")

    parser.add_argument("excel_file", help="Path for the excel file")

    args = parser.parse_args()

    #user = 'bba-vocabs@csiro.au'
    #passwd = "abc123"

    #load defaults from config file
    cfg = None
    with open('config.json') as data_file:
        cfg = json.load(data_file)


    registry_url = cfg['registry_url']
    #check if user wants to override configuration registry url
    if args.registryUrl:
        registry_url = args.registryUrl

    registry_auth_url = registry_url + "/system/security/apilogin"


    #check if user wants no files emitted
    emitFile = True
    if args.noEmitFile:
        emitFile = False

    #check if user just wants to stage things
    updateOnlineRegisters = True
    if args.stagingOnly:
        updateOnlineRegisters = False

    verbose = False
    if args.isVerbose:
        verbose = True
        print "Verbose mode turned on"

    user = args.user
    passwd = args.passwd
    filepath = args.excel_file


    if args.isMulti:
        resultFlag = load_multi_register_file(filepath, user, passwd, emitFile=emitFile,
                                 registry_auth_url=registry_auth_url,
                                 updateOnlineRegisters=updateOnlineRegisters,
                                 verbose=verbose)

    else:
        resultFlag = load_simple_file(filepath, user, passwd, emitFile=emitFile, registry_auth_url=registry_auth_url,
                         updateOnlineRegisters=updateOnlineRegisters,
                         verbose=verbose
                         )


if __name__ == "__main__":
    excel2ldr()

