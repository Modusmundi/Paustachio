import ldap3
from ldap3.core.exceptions import *
import ipaddress
import time
from fqdn import FQDN


class LdapConnect:


    def __init__(self, config_file):
        self.config_file = config_file

    def connect(config_file):
        """
        This constructs a connection to a given LDAP server.

        The logic behind this is pretty straightforward- read the entries in the configuration file.
        Assign host, port, credentials to appropriate values.

        :param config_file: A deserialized JSON file
        :return connection: Established connection to LDAP server.
        """

        configbreak = 0
        config_exception = Exception("Configuration data presented has more than one configuration present.")

        for entry in config_file:
            host = entry['host']
            fqdn_test = FQDN(host)

            if not fqdn_test.is_valid:
                try:
                    ipaddress.ip_address(host)
                except ValueError:
                    raise ValueError("Provided host is not a valid FQDN or IP Address.  Please validate.")

            try:
                port = int(entry['port'])
            except ValueError:
                raise ValueError("Port specified is not an integer (0-65535).  Please try again.")
            username = entry['username']
            password = entry['password']
            if 'host' or 'port' or 'username' or 'password' in entry:
                configbreak += 1

        if configbreak > 1:
            raise config_exception

        server = ldap3.Server(host=host, port=port, get_info=ldap3.ALL)
        try:
            connection = ldap3.Connection(server, user=username, password=password, auto_bind=True)
        except LDAPSocketOpenError:
            raise LDAPSocketOpenError("Unable to make connection to server.  Please check hostname and port and try again.")
        return connection

class LdapSearch:
    def __init__(self, search_file, connection):
        self.search_file = search_file
        self.connection = connection

    def continue_search(search_file, connection):
        """
        This performs searches when provided an established connection, with predefined searches.

        :param search_file: A deserialized JSON file containing search parameters.
        :param connection: Established connection to LDAP server.
        :return results: A key-value structure that returns the the number of results returned and when the search occurred.
        TODO: See if there is a sane way to encrypt sensitive configuration data.
        TODO: Set up a way to allow for paged searching, possibly in the configuration file?
        TODO: Set up TLS because non-TLS searches are bad news bears.
        TODO: I don't like how scope transformation works- is there a better way to sanitize weird output?
        """

        new_list = []

        for dict_entry in search_file:
            total = 0

            run_scope = ''
            base_dn = dict_entry['search']
            search_filter = dict_entry['filter']
            scope = dict_entry['scope'].lower()

            if scope == 'base':
                run_scope = 'BASE'
            elif scope == 'one':
                run_scope = 'LEVEL'
            elif scope == 'sub':
                run_scope = 'SUBTREE'
            else:
                raise LDAPInvalidScopeError("Provided scope must be BASE, ONE, or SUB.  Please edit your search.")

            search = connection.extend.standard.paged_search(search_base=base_dn, search_filter=search_filter,
                                                             search_scope=run_scope, paged_size=100)

            for entry in search:
                total += 1

            search_timestamp = time.ctime()

            dict_entry.update({'total': total})
            dict_entry.update({'timestamp': search_timestamp})

            new_list.append(dict_entry)
        return new_list