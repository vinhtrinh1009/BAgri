# Copyright 2018 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------

from sawtooth_signing import create_context
from sawtooth_signing import CryptoFactory
from sawtooth_signing import secp256k1
import time
import requests


from .errors import ValidatorError
from .transaction_creation import make_create_result_transaction
from .transaction_creation import make_create_subject_transaction
from .transaction_creation import make_create_professor_transaction
from .transaction_creation import make_create_student_transaction
from .transaction_creation import make_create_classroom_transaction
from .transaction_creation import make_create_staff_transaction
from .transaction_creation import make_create_university_transaction
from .transaction_creation import make_create_certificate_transaction
from .transaction_creation import make_update_result_transaction
from .transaction_creation import make_update_subject_transaction
from .transaction_creation import make_update_professor_transaction
from .transaction_creation import make_update_student_transaction
from .transaction_creation import make_update_classroom_transaction
from .transaction_creation import make_update_staff_transaction
from .transaction_creation import make_update_university_transaction
from .transaction_creation import make_update_certificate_transaction

class Messenger(object):
    def __init__(self, validator_url):
        # self._connection = Connection(validator_url)
        self._context = create_context('secp256k1')
        self._crypto_factory = CryptoFactory(self._context)
        self._batch_signer = self._crypto_factory.new_signer(
            self._context.new_random_private_key())

    def open_validator_connection(self):
        self._connection.open()

    def close_validator_connection(self):
        self._connection.close()

    def get_new_key_pair(self):
        private_key = self._context.new_random_private_key()
        public_key = self._context.get_public_key(private_key)
        return public_key.as_hex(), private_key.as_hex()

    def send_create_result_transaction(self, private_key, timestamp,         att_result_id,         att_middlescore,         att_finallscore,         for_student_student_id,         for_classroom_class_id):
        transaction_signer = self._crypto_factory.new_signer(
            secp256k1.Secp256k1PrivateKey.from_hex(private_key))

        batch, batch_bytes = make_create_result_transaction(
            transaction_signer=transaction_signer,
            batch_signer=self._batch_signer,
            timestamp=timestamp,
            att_result_id=att_result_id,
            att_middlescore=att_middlescore,
            att_finallscore=att_finallscore,
            for_student_student_id=for_student_student_id,
            for_classroom_class_id=for_classroom_class_id
            )
        self._send_and_wait_for_commit(batch_bytes)
        return batch

    def send_create_subject_transaction(self, private_key, timestamp,         att_subject_id,         att_subject_name,         att_credit,         att_status,         for_classroom_class_ids,         for_university_university_id):
        transaction_signer = self._crypto_factory.new_signer(
            secp256k1.Secp256k1PrivateKey.from_hex(private_key))

        batch, batch_bytes = make_create_subject_transaction(
            transaction_signer=transaction_signer,
            batch_signer=self._batch_signer,
            timestamp=timestamp,
            att_subject_id=att_subject_id,
            att_subject_name=att_subject_name,
            att_credit=att_credit,
            att_status=att_status,
            for_classroom_class_ids=for_classroom_class_ids,
            for_university_university_id=for_university_university_id
            )
        self._send_and_wait_for_commit(batch_bytes)
        return batch

    def send_create_professor_transaction(self, private_key, timestamp,         att_profess_id,         att_name,         att_email,         att_phone,         att_address,         att_status,         att_public_key,         for_classroom_class_ids,         for_university_university_id):
        transaction_signer = self._crypto_factory.new_signer(
            secp256k1.Secp256k1PrivateKey.from_hex(private_key))

        batch, batch_bytes = make_create_professor_transaction(
            transaction_signer=transaction_signer,
            batch_signer=self._batch_signer,
            timestamp=timestamp,
            att_profess_id=att_profess_id,
            att_name=att_name,
            att_email=att_email,
            att_phone=att_phone,
            att_address=att_address,
            att_status=att_status,
            att_public_key=att_public_key,
            for_classroom_class_ids=for_classroom_class_ids,
            for_university_university_id=for_university_university_id
            )
        self._send_and_wait_for_commit(batch_bytes)
        return batch

    def send_create_student_transaction(self, private_key, timestamp,         att_student_id,         att_name,         att_phone,         att_email,         att_address,         att_public_key,         for_certificate_certi_ids,         for_result_result_ids,         for_university_university_id):
        transaction_signer = self._crypto_factory.new_signer(
            secp256k1.Secp256k1PrivateKey.from_hex(private_key))

        batch, batch_bytes = make_create_student_transaction(
            transaction_signer=transaction_signer,
            batch_signer=self._batch_signer,
            timestamp=timestamp,
            att_student_id=att_student_id,
            att_name=att_name,
            att_phone=att_phone,
            att_email=att_email,
            att_address=att_address,
            att_public_key=att_public_key,
            for_certificate_certi_ids=for_certificate_certi_ids,
            for_result_result_ids=for_result_result_ids,
            for_university_university_id=for_university_university_id
            )
        self._send_and_wait_for_commit(batch_bytes)
        return batch

    def send_create_classroom_transaction(self, private_key, timestamp,         att_class_id,         att_semester,         att_status,         for_subject_subject_id,         for_professor_profess_id,         for_result_result_ids):
        transaction_signer = self._crypto_factory.new_signer(
            secp256k1.Secp256k1PrivateKey.from_hex(private_key))

        batch, batch_bytes = make_create_classroom_transaction(
            transaction_signer=transaction_signer,
            batch_signer=self._batch_signer,
            timestamp=timestamp,
            att_class_id=att_class_id,
            att_semester=att_semester,
            att_status=att_status,
            for_subject_subject_id=for_subject_subject_id,
            for_professor_profess_id=for_professor_profess_id,
            for_result_result_ids=for_result_result_ids
            )
        self._send_and_wait_for_commit(batch_bytes)
        return batch

    def send_create_staff_transaction(self, private_key, timestamp,         att_staff_id,         att_name,         att_email,         att_phone,         att_address,         att_status,         att_public_key,         for_university_university_id):
        transaction_signer = self._crypto_factory.new_signer(
            secp256k1.Secp256k1PrivateKey.from_hex(private_key))

        batch, batch_bytes = make_create_staff_transaction(
            transaction_signer=transaction_signer,
            batch_signer=self._batch_signer,
            timestamp=timestamp,
            att_staff_id=att_staff_id,
            att_name=att_name,
            att_email=att_email,
            att_phone=att_phone,
            att_address=att_address,
            att_status=att_status,
            att_public_key=att_public_key,
            for_university_university_id=for_university_university_id
            )
        self._send_and_wait_for_commit(batch_bytes)
        return batch

    def send_create_university_transaction(self, private_key, timestamp,         att_university_id,         att_university_name,         att_email,         att_phone,         att_address,         att_status,         att_public_key,         for_certificate_certi_ids,         for_staff_staff_ids,         for_professor_profess_ids,         for_student_student_ids,         for_subject_subject_ids):
        transaction_signer = self._crypto_factory.new_signer(
            secp256k1.Secp256k1PrivateKey.from_hex(private_key))

        batch, batch_bytes = make_create_university_transaction(
            transaction_signer=transaction_signer,
            batch_signer=self._batch_signer,
            timestamp=timestamp,
            att_university_id=att_university_id,
            att_university_name=att_university_name,
            att_email=att_email,
            att_phone=att_phone,
            att_address=att_address,
            att_status=att_status,
            att_public_key=att_public_key,
            for_certificate_certi_ids=for_certificate_certi_ids,
            for_staff_staff_ids=for_staff_staff_ids,
            for_professor_profess_ids=for_professor_profess_ids,
            for_student_student_ids=for_student_student_ids,
            for_subject_subject_ids=for_subject_subject_ids
            )
        self._send_and_wait_for_commit(batch_bytes)
        return batch

    def send_create_certificate_transaction(self, private_key, timestamp,         att_certi_id,         att_cpa,         att_type,         att_status,         for_student_student_id,         for_university_university_id):
        transaction_signer = self._crypto_factory.new_signer(
            secp256k1.Secp256k1PrivateKey.from_hex(private_key))

        batch, batch_bytes = make_create_certificate_transaction(
            transaction_signer=transaction_signer,
            batch_signer=self._batch_signer,
            timestamp=timestamp,
            att_certi_id=att_certi_id,
            att_cpa=att_cpa,
            att_type=att_type,
            att_status=att_status,
            for_student_student_id=for_student_student_id,
            for_university_university_id=for_university_university_id
            )
        self._send_and_wait_for_commit(batch_bytes)
        return batch

    def send_update_result_transaction(self, private_key, timestamp,         att_result_id,         att_middlescore,         att_finallscore,         for_student_student_id,         for_classroom_class_id):
        transaction_signer = self._crypto_factory.new_signer(
            secp256k1.Secp256k1PrivateKey.from_hex(private_key))

        batch, batch_bytes = make_update_result_transaction(
            transaction_signer=transaction_signer,
            batch_signer=self._batch_signer,
            timestamp=timestamp,
            att_result_id=att_result_id,
            att_middlescore=att_middlescore,
            att_finallscore=att_finallscore,
            for_student_student_id=for_student_student_id,
            for_classroom_class_id=for_classroom_class_id
            )
        self._send_and_wait_for_commit(batch_bytes)
        return batch

    def send_update_subject_transaction(self, private_key, timestamp,         att_subject_id,         att_subject_name,         att_credit,         att_status,         for_classroom_class_ids,         for_university_university_id):
        transaction_signer = self._crypto_factory.new_signer(
            secp256k1.Secp256k1PrivateKey.from_hex(private_key))

        batch, batch_bytes = make_update_subject_transaction(
            transaction_signer=transaction_signer,
            batch_signer=self._batch_signer,
            timestamp=timestamp,
            att_subject_id=att_subject_id,
            att_subject_name=att_subject_name,
            att_credit=att_credit,
            att_status=att_status,
            for_classroom_class_ids=for_classroom_class_ids,
            for_university_university_id=for_university_university_id
            )
        self._send_and_wait_for_commit(batch_bytes)
        return batch

    def send_update_professor_transaction(self, private_key, timestamp,         att_profess_id,         att_name,         att_email,         att_phone,         att_address,         att_status,         att_public_key,         for_classroom_class_ids,         for_university_university_id):
        transaction_signer = self._crypto_factory.new_signer(
            secp256k1.Secp256k1PrivateKey.from_hex(private_key))

        batch, batch_bytes = make_update_professor_transaction(
            transaction_signer=transaction_signer,
            batch_signer=self._batch_signer,
            timestamp=timestamp,
            att_profess_id=att_profess_id,
            att_name=att_name,
            att_email=att_email,
            att_phone=att_phone,
            att_address=att_address,
            att_status=att_status,
            att_public_key=att_public_key,
            for_classroom_class_ids=for_classroom_class_ids,
            for_university_university_id=for_university_university_id
            )
        self._send_and_wait_for_commit(batch_bytes)
        return batch

    def send_update_student_transaction(self, private_key, timestamp,         att_student_id,         att_name,         att_phone,         att_email,         att_address,         att_public_key,         for_certificate_certi_ids,         for_result_result_ids,         for_university_university_id):
        transaction_signer = self._crypto_factory.new_signer(
            secp256k1.Secp256k1PrivateKey.from_hex(private_key))

        batch, batch_bytes = make_update_student_transaction(
            transaction_signer=transaction_signer,
            batch_signer=self._batch_signer,
            timestamp=timestamp,
            att_student_id=att_student_id,
            att_name=att_name,
            att_phone=att_phone,
            att_email=att_email,
            att_address=att_address,
            att_public_key=att_public_key,
            for_certificate_certi_ids=for_certificate_certi_ids,
            for_result_result_ids=for_result_result_ids,
            for_university_university_id=for_university_university_id
            )
        self._send_and_wait_for_commit(batch_bytes)
        return batch

    def send_update_classroom_transaction(self, private_key, timestamp,         att_class_id,         att_semester,         att_status,         for_subject_subject_id,         for_professor_profess_id,         for_result_result_ids):
        transaction_signer = self._crypto_factory.new_signer(
            secp256k1.Secp256k1PrivateKey.from_hex(private_key))

        batch, batch_bytes = make_update_classroom_transaction(
            transaction_signer=transaction_signer,
            batch_signer=self._batch_signer,
            timestamp=timestamp,
            att_class_id=att_class_id,
            att_semester=att_semester,
            att_status=att_status,
            for_subject_subject_id=for_subject_subject_id,
            for_professor_profess_id=for_professor_profess_id,
            for_result_result_ids=for_result_result_ids
            )
        self._send_and_wait_for_commit(batch_bytes)
        return batch

    def send_update_staff_transaction(self, private_key, timestamp,         att_staff_id,         att_name,         att_email,         att_phone,         att_address,         att_status,         att_public_key,         for_university_university_id):
        transaction_signer = self._crypto_factory.new_signer(
            secp256k1.Secp256k1PrivateKey.from_hex(private_key))

        batch, batch_bytes = make_update_staff_transaction(
            transaction_signer=transaction_signer,
            batch_signer=self._batch_signer,
            timestamp=timestamp,
            att_staff_id=att_staff_id,
            att_name=att_name,
            att_email=att_email,
            att_phone=att_phone,
            att_address=att_address,
            att_status=att_status,
            att_public_key=att_public_key,
            for_university_university_id=for_university_university_id
            )
        self._send_and_wait_for_commit(batch_bytes)
        return batch

    def send_update_university_transaction(self, private_key, timestamp,         att_university_id,         att_university_name,         att_email,         att_phone,         att_address,         att_status,         att_public_key,         for_certificate_certi_ids,         for_staff_staff_ids,         for_professor_profess_ids,         for_student_student_ids,         for_subject_subject_ids):
        transaction_signer = self._crypto_factory.new_signer(
            secp256k1.Secp256k1PrivateKey.from_hex(private_key))

        batch, batch_bytes = make_update_university_transaction(
            transaction_signer=transaction_signer,
            batch_signer=self._batch_signer,
            timestamp=timestamp,
            att_university_id=att_university_id,
            att_university_name=att_university_name,
            att_email=att_email,
            att_phone=att_phone,
            att_address=att_address,
            att_status=att_status,
            att_public_key=att_public_key,
            for_certificate_certi_ids=for_certificate_certi_ids,
            for_staff_staff_ids=for_staff_staff_ids,
            for_professor_profess_ids=for_professor_profess_ids,
            for_student_student_ids=for_student_student_ids,
            for_subject_subject_ids=for_subject_subject_ids
            )
        self._send_and_wait_for_commit(batch_bytes)
        return batch

    def send_update_certificate_transaction(self, private_key, timestamp,         att_certi_id,         att_cpa,         att_type,         att_status,         for_student_student_id,         for_university_university_id):
        transaction_signer = self._crypto_factory.new_signer(
            secp256k1.Secp256k1PrivateKey.from_hex(private_key))

        batch, batch_bytes = make_update_certificate_transaction(
            transaction_signer=transaction_signer,
            batch_signer=self._batch_signer,
            timestamp=timestamp,
            att_certi_id=att_certi_id,
            att_cpa=att_cpa,
            att_type=att_type,
            att_status=att_status,
            for_student_student_id=for_student_student_id,
            for_university_university_id=for_university_university_id
            )
        self._send_and_wait_for_commit(batch_bytes)
        return batch


    def _send_and_wait_for_commit(self, batch):
        response = requests.post(url='http://localhost:32002/batches', 
                                 data=batch,
                                 headers={'Content-Type': 'application/octet-stream'})
        response_json = response.json()
        if 'link' in response_json:
            count = 0
            max_try = 30
            while count < max_try:
                status = requests.get(url=response_json["link"])
                status = status.json()["data"][0]["status"]
                if status == "PENDING":
                    count = count + 1
                    time.sleep(2)
                elif status == "COMMITTED":
                    return
                elif status == "INVALID":
                    break
            raise ValidatorError(f"The transaction is {status}")
        else:
            raise ValidatorError(response_json["error"]["title"])

            