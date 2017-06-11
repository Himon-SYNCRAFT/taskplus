import sys
import traceback
from taskplus.core.shared.response import ResponseFailure


class Action(object):

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
