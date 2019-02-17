import pytest
import Json_Handler

bad_filenames = ['', 'badfile.json']
good_filenames = ['bad.json', 'ugly.json']

"""
JSON deserialization should fail gracefully if no JSON file is passed.
This means either a "Blank" value, or a non-existent JSON file.
"""


@pytest.mark.parametrize('bad_filenames', bad_filenames)
def test_no_file_or_bad_file(bad_filenames):
    with pytest.raises(FileNotFoundError) as error:
        Json_Handler.Json_Deserialize.deserialize(bad_filenames)
    assert error.value.args[0] == "File does not exist or no JSON file has been supplied.  Please try again."


"""
JSON that is going to be deserialized should be valid JSON.
A test should occur to determine that.
"""


@pytest.mark.parametrize('good_filenames', good_filenames)
def test_bad_json(good_filenames):
    with pytest.raises(ValueError) as error:
        Json_Handler.Json_Deserialize.deserialize(good_filenames)
    assert error.value.args[0] == "File is invalid JSON.  Please edit your file and try again."


"""
Given good JSON we should be able to properly return the JSON back as a dict.
"""


def test_good_json():
    proper_files = 'good.json'
    assert Json_Handler.Json_Deserialize.deserialize(proper_files) == [
        {"name": "wat", "group": "group 1", "search": "ou=people,dc=example,dc=com"}]


"""
Given good JSON with multiple searches we should get back an appropriate dict. 
"""


def test_good_multisearch_json():
    proper_files = 'good_multisearch.json'
    assert Json_Handler.Json_Deserialize.deserialize(proper_files) == [
        {'name': 'A Searched Named Example', 'group': 'Group 1', 'search': 'ou=people,o=example',
         'filter': '(objectclass=*)', 'scope': 'sub'},
        {'name': 'A Search Named Example 2 - Electric Boogaloo', 'group': 'group 1', 'search': 'ou=people,o=example',
         'filter': '(st=MI)', 'scope': 'sub'},
        {'name': 'A Search Named Example 3 - The Search Strikes Back', 'group': 'group 2',
         'search': 'ou=people,o=example', 'filter': '(&(l=Rockford)(st=NM))', 'scope': 'sub'}]
