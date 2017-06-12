import json


class UserEncoder(json.JSONEncoder):

    def default(self, data):
        roles = [{'id': role.id, 'name': role.name} for role in data.roles]

        try:
            to_serialize = {
                'id': data.id,
                'name': data.name,
                'roles': roles
            }
            return to_serialize
        except AttributeError:
            return super().default(data)
