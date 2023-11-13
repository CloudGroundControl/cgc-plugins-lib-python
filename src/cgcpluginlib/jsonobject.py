import json


class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


def remove_null_values(d) -> dict:
    result = {key: value for key, value in d.items() if value is not None}
    return result


def get_json_repr(obj) -> str:
    output = json.dumps(obj, cls=CustomEncoder)
    filtered_dict = json.loads(output, object_hook=remove_null_values)
    filtered_output = json.dumps(filtered_dict)
    return filtered_output


class JsonObject:
    def __repr__(self) -> str:
        return get_json_repr(self)

    def json(self) -> str:
        return get_json_repr(self)
