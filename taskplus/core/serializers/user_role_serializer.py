import json


class UserRoleEncoder(json.JSONEncoder):

    def default(self, o):
        try:
            to_serialize = {
                'name': o.name
            }
            return to_serialize

        except AttributeError:
            return super().default(o)
