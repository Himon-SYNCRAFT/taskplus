import json


class TaskEncoder(json.JSONEncoder):

    def default(self, data):
        doer = None

        if data.doer:
            doer_roles = [
                {'id': role.id, 'name': role.name} for role in data.doer.roles]
            doer = {
                'id': data.doer.id,
                'name': data.doer.name,
                'roles': doer_roles
            }

        try:
            creator_roles = [
                {'id': role.id, 'name': role.name} for role in data.creator.roles]
            to_serialize = {
                'id': data.id,
                'name': data.name,
                'content': data.content,
                'creator': {
                    'id': data.creator.id,
                    'name': data.creator.name,
                    'roles': creator_roles
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
