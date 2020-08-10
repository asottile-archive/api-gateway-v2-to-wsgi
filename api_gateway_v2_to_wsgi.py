import base64
import collections
import io
import sys
from types import TracebackType
from typing import Any
from typing import Callable
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Protocol
from typing import Tuple
from typing import Type
from typing import Union

_ExcInfo = Tuple[Type[BaseException], BaseException, TracebackType]


class _StartResponse(Protocol):
    def __call__(
            self,
            status: str,
            headers: List[Tuple[str, str]],
            exc_info: Optional[_ExcInfo] = ...,
    ) -> Callable[[Union[bytes, bytearray]], Any]:
        ...


_App = Callable[[Dict[str, Any], _StartResponse], Iterable[bytes]]
_Handler = Callable[[Dict[str, Any], Dict[str, Any]], Dict[str, str]]


class _Responder:
    def __init__(self) -> None:
        self.status_code = 500
        self.body = io.BytesIO()
        self.headers: Dict[str, List[str]] = collections.defaultdict(list)

    def __call__(
            self,
            status: str,
            headers: List[Tuple[str, str]],
            exc_info: Optional[_ExcInfo] = None,
    ) -> Callable[[Union[bytes, bytearray]], Any]:
        if exc_info is not None:
            _, e, tb = exc_info
            raise e.with_traceback(tb)

        code, _, _ = status.partition(' ')
        self.status_code = int(code)
        for k, v in headers:
            self.headers[k].append(v)
        return self.body.write

    def response(self) -> Dict[str, Any]:
        return {
            'statusCode': self.status_code,
            'body': self.body.getvalue().decode(),
            'multiValueHeaders': self.headers,
        }


def _environ(event: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    body = event.get('body', '')
    if event['isBase64Encoded']:
        body_b = base64.b64decode(body)
    else:
        body_b = body.encode()

    environ = {
        'CONTENT_LENGTH': len(body_b),
        'CONTENT_TYPE': event['headers'].get('content-type', ''),
        'PATH_INFO': event['rawPath'],
        'QUERY_STRING': event['rawQueryString'],
        'REMOTE_ADDR': event['requestContext']['http']['sourceIp'],
        'REQUEST_METHOD': event['requestContext']['http']['method'],
        'SCRIPT_NAME': '',
        'SERVER_NAME': event['headers']['host'],
        'SERVER_PORT': event['headers']['x-forwarded-port'],
        'SERVER_PROTOCOL': event['requestContext']['http']['protocol'],
        'meta.context': context,
        'meta.event': event,
        'wsgi.errors': sys.stderr,
        'wsgi.input': io.BytesIO(body_b),
        'wsgi.multiprocess': False,
        'wsgi.multithread': False,
        'wsgi.run_once': False,
        'wsgi.url_scheme': event['headers']['x-forwarded-proto'],
        'wsgi.version': (1, 0),
    }

    for k, v in event['headers'].items():
        environ[f'HTTP_{k.upper().replace("-", "_")}'] = v

    return environ


def make_lambda_handler(app: _App) -> _Handler:
    def handler(
            event: Dict[str, Any],
            context: Dict[str, Any],
    ) -> Dict[str, Any]:
        responder = _Responder()
        for data in app(_environ(event, context), responder):
            responder.body.write(data)
        return responder.response()
    return handler
