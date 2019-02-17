import pytest
from ldap3.core.exceptions import LDAPException, LDAPInvalidPortError, LDAPSocketOpenError, LDAPInvalidScopeError

import Ldap_Tools

#TODO: Figure out if there's a way to mock LDAP instead of using a local dev instance.

ports = ['-1', '0', '1389', '2636', '65535', '70000']
realpassword = ""

"""
We need to make sure we only have one configuration in our configuration to ensure nothing weird happens.
"""


def test_singular_keys_in_configuration():
    sample_config = [{"host": "192.168.1.42", "port": "2389", "username": "cn=someuser", "password": "somepassword"},
                     {"host": "192.168.1.42", "port": "1636", "username": "cn=someuser", "password": "somepassword"}]
    with pytest.raises(Exception) as error:
        Ldap_Tools.LdapConnect.connect(config_file=sample_config)
    assert error.value.args[0] == "Configuration data presented has more than one configuration present."


"""
We need to make sure that we treat ports as integers when handing them to LDAP.
"""


def test_port_cast_to_int():
    sample_config = [{"host": "192.168.1.250", "port": "fifteen", "username": "cn=someuser", "password": "somepassword"}]
    with pytest.raises(ValueError) as error:
        Ldap_Tools.LdapConnect.connect(config_file=sample_config)
    assert error.value.args[0] == "Port specified is not an integer (0-65535).  Please try again."


"""
We need to make sure that ports handed to us from configuration are between 0 and 65535.
"""


def test_port_sanity_check_less_than_0():
    sample_config = [{"host": "192.168.1.250", "port": "-1636", "username": "uid=tester,ou=People,o=example", "password": realpassword}]
    with pytest.raises(LDAPInvalidPortError) as error:
        Ldap_Tools.LdapConnect.connect(config_file=sample_config)
    assert error.value.args[0] == "port must in range from 0 to 65535"


def test_port_sanity_check_greater_than_0():
    sample_config = [{"host": "192.168.1.250", "port": "70000", "username": "uid=tester,ou=People,o=example", "password": realpassword}]
    with pytest.raises(LDAPInvalidPortError) as error:
        Ldap_Tools.LdapConnect.connect(config_file=sample_config)
    assert error.value.args[0] == "port must in range from 0 to 65535"


"""
We need to make sure that if there is an error during connection due to a bad hostname or IP it is presented to the user.
"""


def test_ip_validity():
    sample_config = [{"host": "256.256.256.256", "port": "1389", "username": "cn=someuser", "password": "somepassword"}]
    with pytest.raises(ValueError) as error:
        Ldap_Tools.LdapConnect.connect(config_file=sample_config)
    assert error.value.args[0] == "Provided host is not a valid FQDN or IP Address.  Please validate."


def test_hostname_validity():
    sample_config = [{"host": "example", "port": "1389", "username": "cn=someuser", "password": "somepassword"}]
    with pytest.raises(ValueError) as error:
        Ldap_Tools.LdapConnect.connect(config_file=sample_config)
    assert error.value.args[0] == "Provided host is not a valid FQDN or IP Address.  Please validate."

"""
We need to test the case of a bad server.
"""

def test_bad_server():
    sample_config = [{"host": "192.168.1.251", "port": "1389", "username": "uid=tester,ou=People,o=example", "password": realpassword}]
    with pytest.raises(LDAPSocketOpenError) as error:
        connection = Ldap_Tools.LdapConnect.connect(config_file=sample_config)
    assert error.value.args[0] == "Unable to make connection to server.  Please check hostname and port and try again."


"""
We need to test the case of a good server, but bad port.
"""


def test_bad_port_good_server():
    sample_config = [{"host": "192.168.1.250", "port": "1388", "username": "uid=tester,ou=People,o=example", "password": realpassword}]
    with pytest.raises(LDAPSocketOpenError) as error:
        connection = Ldap_Tools.LdapConnect.connect(config_file=sample_config)
    assert error.value.args[0] == "Unable to make connection to server.  Please check hostname and port and try again."


"""
We need to make sure that if there is an error with the presented credentials that it is presented to the user.
"""


def test_credential_validity():
    sample_config = [{"host": "192.168.1.250", "port": "1389", "username": "uid=tester,ou=People,o=example", "password": realpassword}]
    connection = Ldap_Tools.LdapConnect.connect(config_file=sample_config)
    connection_attrs = connection.server.info
    connection_attrs = str(connection_attrs)
    assert connection_attrs.index("Supported LDAP versions") != -1


"""
We need to make sure a search properly returns on a server that exists, in all scopes possible!
"""


def test_search_validity_one():
    sample_config = [{"host": "192.168.1.250", "port": "1389", "username": "uid=tester,ou=People,o=example", "password": realpassword}]
    sample_search = [{ "name": "A Search Named Example","group": "Group 1","search": "ou=people,o=example","filter": "(objectclass=*)","scope": "one"}]
    connection = Ldap_Tools.LdapConnect.connect(config_file=sample_config)
    returned_results = Ldap_Tools.LdapSearch.continue_search(sample_search,connection)
    assert returned_results[0]['total'] > 1

def test_search_validity_base():
    sample_config = [{"host": "192.168.1.250", "port": "1389", "username": "uid=tester,ou=People,o=example", "password": realpassword}]
    sample_search = [{ "name": "A Search Named Example","group": "Group 1","search": "ou=people,o=example","filter": "(objectclass=*)","scope": "base"}]
    connection = Ldap_Tools.LdapConnect.connect(config_file=sample_config)
    returned_results = Ldap_Tools.LdapSearch.continue_search(sample_search,connection)
    assert returned_results[0]['total'] == 1

def test_search_validity_sub():
    sample_config = [{"host": "192.168.1.250", "port": "1389", "username": "uid=tester,ou=People,o=example", "password": realpassword}]
    sample_search = [{ "name": "A Search Named Example","group": "Group 1","search": "ou=people,o=example","filter": "(objectclass=*)","scope": "sub"}]
    connection = Ldap_Tools.LdapConnect.connect(config_file=sample_config)
    returned_results = Ldap_Tools.LdapSearch.continue_search(sample_search,connection)
    print(returned_results)
    assert returned_results[0]['total'] >= 1

"""
We need to make sure that if a bad scope is passed that the proper exception is returned.
"""


def test_scope_validity():
    sample_config = [{"host": "192.168.1.250", "port": "1389", "username": "uid=tester,ou=People,o=example", "password": realpassword}]
    sample_search = [{ "name": "A Search Named Example","group": "Group 1","search": "ou=people,o=example","filter": "(objectclass=*)","scope": "broken"}]
    connection = Ldap_Tools.LdapConnect.connect(config_file=sample_config)
    with pytest.raises(LDAPInvalidScopeError) as error:
        returned_results = Ldap_Tools.LdapSearch.continue_search(sample_search,connection)
    assert error.value.args[0] == "Provided scope must be BASE, ONE, or SUB.  Please edit your search."

def test_scope_validity_weirdCase():
    sample_config = [{"host": "192.168.1.250", "port": "1389", "username": "uid=tester,ou=People,o=example", "password": realpassword}]
    sample_search = [{ "name": "A Search Named Example","group": "Group 1","search": "ou=people,o=example","filter": "(objectclass=*)","scope": "oNe"}]
    connection = Ldap_Tools.LdapConnect.connect(config_file=sample_config)
    returned_results = Ldap_Tools.LdapSearch.continue_search(sample_search,connection)
    assert returned_results[0]['total'] >= 1


"""
We need to make sure that multiple searches happen properly.
"""

def test_scope_validity_multisearch():
    sample_config = [{"host": "192.168.1.250", "port": "1389", "username": "uid=tester,ou=People,o=example", "password": realpassword}]
    sample_search = [{'name': 'A Searched Named Example', 'group': 'Group 1', 'search': 'ou=people,o=example', 'filter': '(objectclass=*)', 'scope': 'sub'}, {'name': 'A Search Named Example 2 - Electric Boogaloo', 'group': 'group 1', 'search': 'ou=people,o=example', 'filter': '(st=MI)', 'scope': 'sub'}, {'name': 'A Search Named Example 3 - The Search Strikes Back', 'group': 'group 2', 'search': 'ou=people,o=example', 'filter': '(&(l=Rockford)(st=NM))', 'scope': 'sub'}]
    connection = Ldap_Tools.LdapConnect.connect(config_file=sample_config)
    returned_results = Ldap_Tools.LdapSearch.continue_search(sample_search,connection)