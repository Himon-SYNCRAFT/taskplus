import json


class TaskEncoder(json.JSONEncoder):

    def default(self, data):
        doer = None

        if data.doer:
            doer = {
                'id': data.doer.id,
                'name': data.doer.name,
                'role': {
                    'id': data.doer.role.id,
                    'name': data.doer.role.name,
                }
            }

        try:
            to_serialize = {
                'id': data.id,
                'name': data.name,
                'content': data.content,
                'creator': {
                    'id': data.creator.id,
                    'name': data.creator.name,
                    'role': {
                        'id': data.creator.role.id,
                        'name': data.creator.role.name,
                    }
                },
                'status': {
                    'id': data.status.id,
                    'name': data.status.name,
                },
                'doer': doer
            }

            return to_serialize
        except AttributeError:
            return super().default(data)
