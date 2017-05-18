from taskplus.core.shared.request import Request


class AddTaskRequest(Request):

    def __init__(self, name, content, creator_id):
        super().__init__()
        self.name = name
        self.content = content
        self.creator_id = creator_id

    def _validate(self):
        self.errors = []

        if self.name is None:
            self._add_error('name', 'is required')
        elif isinstance(self.name, str) and not self.name.strip():
            self._add_error('name', 'is required')
        elif not isinstance(self.name, str):
            self._add_error('name', 'expected str, got {}({})'.format(
                self.name.__class__.__name__, self.name
            ))

        if self.content is None:
            self._add_error('content', 'is required')
        elif isinstance(self.content, str) and not self.content.strip():
            self._add_error('content', 'is required')
        elif not isinstance(self.content, str):
            self._add_error('content', 'expected str, got {}({})'.format(
                self.content.__class__.__name__, self.content
            ))

        if self.creator_id is None:
            self._add_error('creator_id', 'is required')
        elif not isinstance(self.creator_id, int):
            self._add_error('creator_id', 'expected int, got {}({})'.format(
                self.creator_id.__class__.__name__, self.creator_id
            ))
