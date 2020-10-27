# -*- coding: utf-8 -*-
"""
Created on Thu May 30 16:22:49 2019

@author: z003vrzk
"""

import xml.etree.ElementTree as ET

project_folder = r'D:\Jobs\ABT Site Projects\Local project folder\44OP-239338_ACC_RIO_Grande'
application_folder = r'C:\Users\z003vrzk\.spyder-py3\Scripts\Work\ABT\AppCnt_0DVX'
# What do the (3) different xml files do?
xml_file1 = r"C:\Users\z003vrzk\.spyder-py3\Scripts\Work\ABT\AppCnt_0DVX\Tpl_DYEV\BAAPPC_J19O1UUBIA6202RFWWY7D9ANH.xml"
xml_file2 = r"C:\Users\z003vrzk\.spyder-py3\Scripts\Work\ABT\AppCnt_0DVX\Instance_2CKR\BAAPPC_J19O1UUBIA6202RFWWY7D9ANH.xml"
xml_file3 = r"C:\Users\z003vrzk\.spyder-py3\Scripts\Work\ABT\AppCnt_0DVX\APPTYPE\8392788-1434 - Copy.xml"

tree = ET.parse(xml_file)
root = tree.getroot()

# This is how you iterate over an elements direct children
for child in root:
    print('child.tag | child.attrib')
    print('{} | {}'.format(child.tag, child.attrib))
    
# If I want to iterate over a specific objects children, do this
# children are nested, and we can access a specific element by index
parent = root[0]
for child in parent: # Only direct descendants
    print('child.tag | child.attrib')
    print('{} | {}\n'.format(child.tag, child.attrib))

# To iterate over all descendants of an element..
engObjectParent = root[1][0][0][0][0][1][0][1][0][2] # All engineering Objects
element = root[1][0][0][0][0][1][0][1][0][2][0] # Specific engineering Object
for child in element.iter():
    print('child.tag | child.attrib')
    print('{} | {}\n'.format(child.tag, child.attrib))


# Find all engineering objects under the root
# Each engineering object has a tag as shown below
for EngineeringObject in root.iter(tag='{http://www.sibt.com/Industry/03.00/BuildingTechnologies/domain/}EngineeringObject'):
    print(EngineeringObject.attrib)

# element.findall() finds only ements with a tag that are direct children of
# The current element
engObjectParent = root[1][0][0][0][0][1][0][1][0][2] # All engineering Objects
for EngineeringObject in engObjectParent.findall('{http://www.sibt.com/Industry/03.00/BuildingTechnologies/domain/}EngineeringObject'):
    print(EngineeringObject.attrib)

# NOTE there is a default namespace in this xml document
# The default namespace is '{http://www.sibt.com/Industry/03.00/BuildingTechnologies/domain/}
# Accessing document elements requires prefixing the namespace to the element tag
# For example {uri}tag. uri is the namespace

#%%
"""Attempt 1
Use the document namespace to search for all engineering objects
The namespace dictionary can be passed to element.findall('object_name', namespace)
to prefix all element tags with the namespace.
Remember that element.findall() only searches direct children"""
namespaces = {'mynamespace':'http://www.sibt.com/Industry/03.00/BuildingTechnologies/domain/'}
engObjectParent = root[1][0][0][0][0][1][0][1][0][2] # All engineering Objects
my_eng_objects = engObjectParent.findall('mynamespace:EngineeringObject', namespaces)


"""Creating Namespaces based on existing in document
Same as before, but this time we are automatically adding namespaces to xml
documents. Add namespaces directly by registering each namespace with the ET 
module"""
my_namespaces = dict([node for _, node in ET.iterparse(xml_file, events=['start-ns'])])
for name, value in my_namespaces.items():
    ET.register_namespace(name,value)
my_namespaces['default_global'] = my_namespaces['']
engObjectParent = root[1][0][0][0][0][1][0][1][0][2] # All engineering Objects
my_eng_objects = engObjectParent.findall('default_global:EngineeringObject', my_namespaces)

#%% Finding ObjectName of an engineering object

my_namespaces = dict([node for _, node in ET.iterparse(xml_file, events=['start-ns'])])
for name, value in my_namespaces.items():
    ET.register_namespace(name, value) # Why did I do this?

my_namespaces['default_global'] = my_namespaces['']
engObjectParent = root[1][0][0][0][0][1][0][1][0][2] # All engineering Objects
my_eng_objects = engObjectParent.findall('default_global:EngineeringObject', my_namespaces)

eng_object = my_eng_objects[0]
eng_object.tag

# NOTE : element.iter() WILL give all branch objects (not just direct child)
for element in eng_object.iter():
    print('{} | {}\n'.format(element.tag, element.attrib))


# NOTE : element.iterfind() only returns top-level children. It does not give
# All branch objects
for element in eng_object.iterfind('default_global:StandardFeature', my_namespaces):
    print('{} | {}\n'.format(element.tag, element.attrib))

#%% Engineering object structure
"""
EngineeringObject
    StandardFeature
        EOTypeRef (target, prototype)
    ParameterFeature # Multiple per EngineeringObject
        EOParameter (name)
            Category (type)
                Value (value)
            EOParameterTypeRef (target)
    EOBAcnetFeature
        ObjectIdentifier
            ObjectType
            InstanceNumber
        ObjectName
"""




