from json.decoder import JSONDecodeError
from aiohttp.web import json_response


async def decode_request(request):
    try:
        return await request.json()
    except JSONDecodeError:
        raise json_response(
            {"status": "fail", "data": {"message": "Improper JSON format"}}, status=406
        )


def gen_file(data, dst, template):
    file = open(dst, "w")
    output = template.render(data=data)
    file.write(output)
    file.close()