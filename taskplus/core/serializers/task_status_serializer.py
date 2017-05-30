import json


class TaskStatusEncoder(json.JSONEncoder):

    def default(self, data):
        try:
            to_serialize = {
                'id': data.id,
                'name': data.name
            }
            return to_serialize
        except AttributeError:
            return super().default(data)
