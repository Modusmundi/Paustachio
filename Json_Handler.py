import json

class Json_Deserialize:

    """
    This takes a given JSON file and deserializes it.
    This is re-usable, we just need to feed the file in and make sure we know how to use the file later.

    Rough logic is this-
    Try to open the file.  If it doesn't exist, raise the error and tell us.
    If the file exists, try to load the JSON in the file.  If it is not valid JSON, raise an error and tell us.

    :param json_file: A JSON file located on disk.
    :return output_file: A Deserialized JSON file in dict format.
    """
    def __init__(self, json_file):
        self.output_file = ''
        self.json_file = json_file

    def deserialize(json_file):
        try:
            with open(json_file) as file_object:
                try:
                    output_file = json.load(file_object)
                except ValueError:
                    raise ValueError("File is invalid JSON.  Please edit your file and try again.")
        except FileNotFoundError:
            raise FileNotFoundError("File does not exist or no JSON file has been supplied.  Please try again.")

        return output_file