import csv
from pathlib import Path


class csv_write:
    def __init__(self, search_results, save_file):
        self.search_results = search_results
        self.save_file = save_file if save_file is not None else 'results.csv'

    def write(search_results, save_file='results.csv'):
        """
        With write, we want to open a file to write, and append to it.
        If the file does not exist, we want to place a specific title format at the top, and then write to the file.
        We want this output to be generally excel-friendly.

        :param search_results: A dict of search results passed from Ldap_Tools.LdapSearch.continue_search generally.
        :param save_file: An optionally-passed location to save the generated CSV file.
        :return connection: Established connection to LDAP server.

        TODO: Make the results CSV home configurable.  Like, actually configurable.
        """

        results_file = Path('./' + save_file)

        # So the goal of this portion of code is to determine if our results file already exists.
        # If it does, great!  We don't need to do anything else.
        # If it does not, we need to not only create it...
        # We need to put the right things at the top so that the output makes sense.

        if not results_file.is_file():
            with open(file=results_file, mode='x', newline='') as csvfile:
                new_resultswriter = csv.writer(csvfile, dialect='excel', quotechar='"', doublequote=True,
                                               quoting=csv.QUOTE_MINIMAL)
                new_resultswriter.writerow(
                    ['Name'] + ['Group'] + ['Time of Search'] + ['Search DN'] + ['Filter Used'] + ['Search Scope'] + [
                        'Record Count'])
        csvfile.close()

        # Now we start writing each of the list-dict results to the CSV.

        with open(file=results_file, mode='a', newline='') as csvfile:
            resultswriter = csv.writer(csvfile, dialect='excel', quotechar='"', doublequote=True,
                                       quoting=csv.QUOTE_MINIMAL)

            for dict_entry in search_results:
                name = dict_entry['name']
                group = dict_entry['group']
                timestamp = dict_entry['timestamp']
                search = dict_entry['search']
                filter = dict_entry['filter']
                scope = dict_entry['scope']
                total = str(dict_entry['total'])

                resultswriter.writerow([name] + [group] + [timestamp] + [search] + [filter] + [scope] + [total])
