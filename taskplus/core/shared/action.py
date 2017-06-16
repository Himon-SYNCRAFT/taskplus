import traceback
from taskplus.core.shared.response import ResponseFailure


class Action(object):

    def __init__(self):
        self._before_execution_hooks = set()
        self._after_execution_hooks = set()

    def execute(self, request):
        if not request.is_valid():
            return ResponseFailure.build_from_invalid_request(request)

        try:
            return self.process_request(request)
        except Exception as exc:
            traceback.print_exc()
            return ResponseFailure.build_system_error(
                '{}: {}'.format(exc.__class__.__name__, exc)
            )

    def process_request(self, request):
        raise NotImplementedError(
            'process_request() not implemented by Action class')

    @classmethod
    def get_name(cls):
        return cls.__name__

    def _call_before_execution_hooks(self, request, resource):
        for func in self._before_execution_hooks:
            func(self.get_name(), data=dict(request=request, resource=resource))

    def _call_after_execution_hooks(self, request, resource):
        for func in self._after_execution_hooks:
            func(self.get_name(), data=dict(request=request, resource=resource))

    def add_before_execution_hook(self, func):
        self._before_execution_hooks.add(func)

    def add_after_execution_hook(self, func):
        self._after_execution_hooks.add(func)

    def remove_before_execution_hook(self, func):
        self._before_execution_hooks.remove(func)

    def remove_after_execturion_hook(self, func):
        self._after_execution_hooks.remove(func)

    def clear_before_execution_hooks(self):
        self._before_execution_hooks.clear()

    def clear_after_execution_hooks(self):
        self._after_execution_hooks.clear()
