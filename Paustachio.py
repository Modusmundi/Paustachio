# Paustatio, a Python-based, simple auditor for LDAP queries.
#
# So what does Paustachio do?
#
# 1.) Takes JSON-formatted search requests and runs them to return counts of the search requests.
# 2.) Saves this data to a CSV file.
#

import Json_Handler
import Ldap_Tools
import csv_tools

# TODO: Make this configurable via command-line.
config_deserialized = Json_Handler.Json_Deserialize.deserialize('connectFile.json')
searches_deserialized = Json_Handler.Json_Deserialize.deserialize('searches.json')

#Connection generation
connection = Ldap_Tools.LdapConnect.connect(config_file=config_deserialized)

#Return results from the search
returned_results = Ldap_Tools.LdapSearch.continue_search(searches_deserialized,connection)

#Make the CSV
file_generated = csv_tools.csv_write.write(search_results=returned_results)
