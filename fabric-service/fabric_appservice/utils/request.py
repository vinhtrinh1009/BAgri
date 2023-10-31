from json.decoder import JSONDecodeError
from utils.response import ApiBadRequest


async def decode_request(request):
    try:
        return await request.json()
    except JSONDecodeError:
        raise ApiBadRequest
