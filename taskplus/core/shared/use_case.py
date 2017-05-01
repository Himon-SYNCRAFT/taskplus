from taskplus.core.shared.response import ResponseFailure


class UseCase(object):

    def execute(self, request):
        if not request:
            return ResponseFailure.build_from_invalid_request(request)

        try:
            return self.process_request(request)
        except Exception as exc:
            return ResponseFailure.build_system_error(
                '{}: {}'.format(exc.__class__.__name__, exc)
            )

    def process_request(self, request):
        raise NotImplementedError(
            'process_request() not implemented by UseCase class')
