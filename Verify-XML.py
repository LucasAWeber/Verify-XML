#  Verify-XML.py
# 
#  Python script that checks to make sure XML file(s) are valid
#  (follow xml syntax, and schema)

import sys
import os
import argparse
from lxml import etree

parser = argparse.ArgumentParser(description="This script verifies that the given XML file(s) follow correct XML syntax," \
                                 " includes the given schema, follow the given schema, and contain the correct schema version")
parser.add_argument('xml', type=str, nargs='+', help='path to one or more xml files to verify')
parser.add_argument('-s', '--schema', type=str, nargs='?', help='path to a schema file used to check the xml file(s)')
args = parser.parse_args()

check_schema = False
if (args.schema != None):
    if (args.schema.endswith(".xsd")):
        schema_path = args.schema
        schema_file = os.path.basename(schema_path)
        schema_xml = etree.XMLSchema(etree.parse(schema_path))
        check_schema = True
    else:
        sys.exit(1)

# Loops through all xml files in cfg
for xml_path in args.xml:
    if (xml_path.endswith(".xml")):
        # Throws error if incorrect xml syntax
        xml_tree = etree.parse(xml_path)
        if (not check_schema):
            continue
        # Checks if xml file includes schema
        is_schema = False
        with open(xml_path, "r") as f:
            if (schema_file not in f.readline()):
                raise Exception("XML file (" + xml_path + ") doesnt reference the schema (" + schema_path + ")")
        
        # Checks if schema version in xml matches current schema version
        schema_tree = etree.parse(schema_path)
        schema_version = schema_tree.getroot().attrib["version"]
        xml_version = xml_tree.find("header").find("schema_version").text
        if (schema_version != xml_version):
            raise Exception("Schema version mismatch! Schema (" + schema_path +
                            ") is version " + schema_version + " but XML file (" + xml_path + ") reports schema version " + xml_version)

        # Checks if xml file follow schema correctly
        result = schema_xml.validate(xml_tree)
        if (not result):
            raise Exception("XML config file (" + xml_path + ") does not conform to schema (" + schema_path + ")")
                        
sys.exit(0)