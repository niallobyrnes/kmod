#!/usr/bin/env python


import os
import yaml
import pprint

mod = 'icc'


MAP = {'append-path': 'append',
       'prepend-path': 'prepend',
       'setenv': 'setenv',
       'prereq': 'prereq',
       'set-alias': 'alias',
       'conflict': 'conflict',
       }

config = dict()

ignore = [
    "source [file dirname $::ModulesCurrentModulefile]/../../common/common_setup2.tcl",
    "source [file dirname $::ModulesCurrentModulefile]/../../common/common_setup2.tcl",
    "GeneralAppSetup",
    "} else {",
    "}",
    ]

def add2list(param):
    name, val = param[:2]
    name = MAP[name]

    if name not in config:
        config[name] = dict()

    if val in config[name]:
        config[name].append(val)
    else:
        config[name] = [val] 



def add3list(param):
    name, key, val = param[:3]
    name = MAP[name]

    if name not in config:
        config[name] = dict()

    if key in config[name]:
        config[name][key].append(val)
    else:
        config[name][key] = [val] 


def additem(param):
    name, key, val = param[:3]
    name = MAP[name]

    if name not in config:
        config[name] = dict()

    config[name][key] = val

def parsit(filename):
    with open(filename) as f:
        cannot_parse = list()

        for line in f:
            ignoreme = False
            line = line.strip()
            param = line.split()
            if not param:
                continue

            if line.startswith('#'):
                continue

            if line.startswith('if ![is-loaded'):
                continue

            for i in ignore:
                if i == line:
                    ignoreme = True
            if ignoreme:
                continue



            if param[0] in ['prepend-path', 'append-path']:
                add3list(param)

            elif param[0] in ['prereq', 'set-alias', 'conflict']:
                add2list(param)

            elif param[0] in ['setenv']:
                additem(param)

            elif param[0] == 'set':
                config[param[1]] = param[2]

            elif param[0] == 'module' and param[1] == 'add':
                if len(param) > 3:
                    
                    print "TOO MANY MODULE ADD"*3
                    print line
                    print param
                tmp = ['prereq']
                tmp.extend(param[2:])
                add2list(tmp)

            else:
                cannot_parse.append('Cannot Parse "%s"' % line)


    with open(mod + '.yaml', 'w') as outfile:
        outfile.write( yaml.dump(config, default_flow_style=False))
            
    if cannot_parse:
        print filename
        print '\n'.join(cannot_parse)
        print '\n'


root = '/opt/share/modules/applications-extra/'
dirs = os.listdir(root)


for d in dirs:
    filename = root + d + '/.base'
    parsit(filename)

    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(config)



