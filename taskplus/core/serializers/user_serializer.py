import json


class UserEncoder(json.JSONEncoder):

    def default(self, data):
        try:
            to_serialize = {
                'id': data.id,
                'name': data.name,
                'role': {
                    'id': data.role.id,
                    'name': data.role.name
                }
            }
            return to_serialize
        except AttributeError:
            return super().default(data)
