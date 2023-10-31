from settings import config
from exceptions import DocsServiceRequestError
import requests


def create_doc(body):
    try:
        doc_url = f"{config['docs_service']['host']}/docs"

        requests.post(
            doc_url,
            json=body,
            headers={},
        )
    except Exception as e:
        raise DocsServiceRequestError("Fail to create document")
