import ipfshttpclient
import io
from constants.config import *


api = ipfshttpclient.connect('/ip4/139.59.217.172/tcp/5001/http')


async def save_to_ipfs(image_request):
    image = image_request.file

    image_content = image.read()

    # encrypt_information = encrypt_aes_gcm(imageConvert, secret_key)
    # encrypted_data = encrypt_information[0]
    # nonce = encrypt_information[1]
    # tag = encrypt_information[2]
    encrypted_data_path = "{}/data.txt".format(Config.DATABASE_DIR)
    content_id_path = "{}/cid.txt".format(Config.DATABASE_DIR)

    with open(encrypted_data_path, "wb") as f:
        f.write((image_content))

    encrypt_content_id = api.add(encrypted_data_path)["Hash"]

    file_cid = open(content_id_path, "a")
    file_cid.write(encrypt_content_id + "\n")
    file_cid.close()

    response_obj = {
        "content_id": encrypt_content_id,
    }
    return response_obj