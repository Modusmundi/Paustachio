import pytest
import csv
import csv_tools
import os

good_csv = 'good_csv.csv'
results = 'results.csv'
"""
We need to test that in the event of no supplied filename, a default file is generated.
"""


def test_default_csv_generation():
    if os.path.exists(results):
        print("Cleaned up results file from previous test.")
        os.remove(results)
    sample_results = [{'name': 'A Searched Named Example', 'group': 'Group 1', 'search': 'ou=people,o=example',
                       'filter': '(objectclass=*)', 'scope': 'sub', 'total': 2002,
                       'timestamp': 'Sun Oct 21 21:35:12 2018'},
                      {'name': 'A Search Named Example 2 - Electric Boogaloo', 'group': 'group 1',
                       'search': 'ou=people,o=example', 'filter': '(st=MI)', 'scope': 'sub', 'total': 51,
                       'timestamp': 'Sun Oct 21 21:35:12 2018'},
                      {'name': 'A Search Named Example 3 - The Search Strikes Back', 'group': 'group 2',
                       'search': 'ou=people,o=example', 'filter': '(&(l=Rockford)(st=NM))', 'scope': 'sub', 'total': 1,
                       'timestamp': 'Sun Oct 21 21:35:12 2018'}]
    file_generated = csv_tools.csv_write.write(search_results=sample_results)
    assert os.path.isfile(results) == 1


"""
We need to test that when a file is generated with multiple entries, that the entries come back appropriately.
"""


def test_rowcount_truthiness():
    resultcounter = 0
    if os.path.exists(results):
        print("Rowcount truthiness - Cleaned up results file from previous test.")
        os.remove(results)
    sample_results = [{'name': 'A Searched Named Example', 'group': 'Group 1', 'search': 'ou=people,o=example',
                       'filter': '(objectclass=*)', 'scope': 'sub', 'total': 2002,
                       'timestamp': 'Sun Oct 21 21:35:12 2018'},
                      {'name': 'A Search Named Example 2 - Electric Boogaloo', 'group': 'group 1',
                       'search': 'ou=people,o=example', 'filter': '(st=MI)', 'scope': 'sub', 'total': 51,
                       'timestamp': 'Sun Oct 21 21:35:12 2018'},
                      {'name': 'A Search Named Example 3 - The Search Strikes Back', 'group': 'group 2',
                       'search': 'ou=people,o=example', 'filter': '(&(l=Rockford)(st=NM))', 'scope': 'sub', 'total': 1,
                       'timestamp': 'Sun Oct 21 21:35:12 2018'}]
    file_generated = csv_tools.csv_write.write(search_results=sample_results)

    with open(file=results, mode='r', newline='') as csvfile:
        resultsreader = csv.reader(csvfile, dialect='excel', quotechar='"', doublequote=True,
                                   quoting=csv.QUOTE_MINIMAL)
        for row in resultsreader:
            resultcounter += row.count('sub')
    csvfile.close()
    assert resultcounter == 3


"""
We need to test that in the event that a filename is supplied, that file is generated with an appropriate name.
"""


def test_bespoke_csv_generation():
    if os.path.exists(good_csv):
        print("Bespoke CSV generation - Cleaned up results file from previous test.")
        os.remove(good_csv)
    sample_results = [{'name': 'A Searched Named Example', 'group': 'Group 1', 'search': 'ou=people,o=example',
                       'filter': '(objectclass=*)', 'scope': 'sub', 'total': 2002,
                       'timestamp': 'Sun Oct 21 21:35:12 2018'},
                      {'name': 'A Search Named Example 2 - Electric Boogaloo', 'group': 'group 1',
                       'search': 'ou=people,o=example', 'filter': '(st=MI)', 'scope': 'sub', 'total': 51,
                       'timestamp': 'Sun Oct 21 21:35:12 2018'},
                      {'name': 'A Search Named Example 3 - The Search Strikes Back', 'group': 'group 2',
                       'search': 'ou=people,o=example', 'filter': '(&(l=Rockford)(st=NM))', 'scope': 'sub', 'total': 1,
                       'timestamp': 'Sun Oct 21 21:35:12 2018'}]
    file_generated = csv_tools.csv_write.write(search_results=sample_results, save_file=good_csv)
    assert os.path.isfile(good_csv) == 1


"""
We need to test that in the event of no CSV existing, appropriate headers are generated when the file is made.
"""


def test_good_header_testing():
    rowcounter = 0
    rowholder = {}
    if os.path.exists(good_csv):
        print("Good header testing - Cleaned up results file from previous test.")
        os.remove(good_csv)
    sample_results = [{'name': 'A Searched Named Example', 'group': 'Group 1', 'search': 'ou=people,o=example',
                       'filter': '(objectclass=*)', 'scope': 'sub', 'total': 2002,
                       'timestamp': 'Sun Oct 21 21:35:12 2018'},
                      {'name': 'A Search Named Example 2 - Electric Boogaloo', 'group': 'group 1',
                       'search': 'ou=people,o=example', 'filter': '(st=MI)', 'scope': 'sub', 'total': 51,
                       'timestamp': 'Sun Oct 21 21:35:12 2018'},
                      {'name': 'A Search Named Example 3 - The Search Strikes Back', 'group': 'group 2',
                       'search': 'ou=people,o=example', 'filter': '(&(l=Rockford)(st=NM))', 'scope': 'sub', 'total': 1,
                       'timestamp': 'Sun Oct 21 21:35:12 2018'}]
    file_generated = csv_tools.csv_write.write(search_results=sample_results, save_file=good_csv)

    with open(file=results, mode='r', newline='') as csvfile:
        resultsreader = csv.reader(csvfile, dialect='excel', quotechar='"', doublequote=True,
                                   quoting=csv.QUOTE_MINIMAL)
        for row in resultsreader:
            rowholder[rowcounter] = row
            rowcounter += 1
    csvfile.close()

    assert rowholder[0] == ['Name', 'Group', 'Time of Search', 'Search DN', 'Filter Used', 'Search Scope', 'Record Count']
