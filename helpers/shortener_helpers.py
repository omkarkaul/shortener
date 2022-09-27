from common.constants import Constants


def handle_exception(func):
    def handler(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            return build_response(
                status=Constants.HTTP_SERVER_FAIL,
                message=f'Failed to execute function {func.__name__} with following message: {str(ex)}'
            )

    return handler


def build_response(status, message="", result=None):
    ok = status in [Constants.HTTP_SUCCESS, Constants.HTTP_CREATED]
    return {
        'ok': ok,
        'status': status,
        'message': message,
        'result': {} if result is None else result
    }
