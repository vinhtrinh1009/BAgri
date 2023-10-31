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

    def send_create_result_transaction(self, private_key, timestamp,         result_id,         middlescore,         finallscore,         student_student_id,         classroom_class_id):
        transaction_signer = self._crypto_factory.new_signer(
            secp256k1.Secp256k1PrivateKey.from_hex(private_key))

        batch, batch_bytes = make_create_result_transaction(
            transaction_signer=transaction_signer,
            batch_signer=self._batch_signer,
            timestamp=timestamp,
            result_id=result_id,
            middlescore=middlescore,
            finallscore=finallscore,
            student_student_id=student_student_id,
            classroom_class_id=classroom_class_id
            )
        self._send_and_wait_for_commit(batch_bytes)
        return batch

    def send_create_subject_transaction(self, private_key, timestamp,         subject_id,         subject_name,         credit,         status,         classroom_class_ids,         university_university_id):
        transaction_signer = self._crypto_factory.new_signer(
            secp256k1.Secp256k1PrivateKey.from_hex(private_key))

        batch, batch_bytes = make_create_subject_transaction(
            transaction_signer=transaction_signer,
            batch_signer=self._batch_signer,
            timestamp=timestamp,
            subject_id=subject_id,
            subject_name=subject_name,
            credit=credit,
            status=status,
            classroom_class_ids=classroom_class_ids,
            university_university_id=university_university_id
            )
        self._send_and_wait_for_commit(batch_bytes)
        return batch

    def send_create_professor_transaction(self, private_key, timestamp,         profess_id,         name,         email,         phone,         address,         status,         public_key,         classroom_class_ids,         university_university_id):
        transaction_signer = self._crypto_factory.new_signer(
            secp256k1.Secp256k1PrivateKey.from_hex(private_key))

        batch, batch_bytes = make_create_professor_transaction(
            transaction_signer=transaction_signer,
            batch_signer=self._batch_signer,
            timestamp=timestamp,
            profess_id=profess_id,
            name=name,
            email=email,
            phone=phone,
            address=address,
            status=status,
            public_key=public_key,
            classroom_class_ids=classroom_class_ids,
            university_university_id=university_university_id
            )
        self._send_and_wait_for_commit(batch_bytes)
        return batch

    def send_create_student_transaction(self, private_key, timestamp,         student_id,         name,         phone,         email,         address,         public_key,         certificate_certi_ids,         result_result_ids,         university_university_id):
        transaction_signer = self._crypto_factory.new_signer(
            secp256k1.Secp256k1PrivateKey.from_hex(private_key))

        batch, batch_bytes = make_create_student_transaction(
            transaction_signer=transaction_signer,
            batch_signer=self._batch_signer,
            timestamp=timestamp,
            student_id=student_id,
            name=name,
            phone=phone,
            email=email,
            address=address,
            public_key=public_key,
            certificate_certi_ids=certificate_certi_ids,
            result_result_ids=result_result_ids,
            university_university_id=university_university_id
            )
        self._send_and_wait_for_commit(batch_bytes)
        return batch

    def send_create_classroom_transaction(self, private_key, timestamp,         class_id,         semester,         status,         subject_subject_id,         professor_profess_id,         result_result_ids):
        transaction_signer = self._crypto_factory.new_signer(
            secp256k1.Secp256k1PrivateKey.from_hex(private_key))

        batch, batch_bytes = make_create_classroom_transaction(
            transaction_signer=transaction_signer,
            batch_signer=self._batch_signer,
            timestamp=timestamp,
            class_id=class_id,
            semester=semester,
            status=status,
            subject_subject_id=subject_subject_id,
            professor_profess_id=professor_profess_id,
            result_result_ids=result_result_ids
            )
        self._send_and_wait_for_commit(batch_bytes)
        return batch

    def send_create_staff_transaction(self, private_key, timestamp,         staff_id,         name,         email,         phone,         address,         status,         public_key,         university_university_id):
        transaction_signer = self._crypto_factory.new_signer(
            secp256k1.Secp256k1PrivateKey.from_hex(private_key))

        batch, batch_bytes = make_create_staff_transaction(
            transaction_signer=transaction_signer,
            batch_signer=self._batch_signer,
            timestamp=timestamp,
            staff_id=staff_id,
            name=name,
            email=email,
            phone=phone,
            address=address,
            status=status,
            public_key=public_key,
            university_university_id=university_university_id
            )
        self._send_and_wait_for_commit(batch_bytes)
        return batch

    def send_create_university_transaction(self, private_key, timestamp,         university_id,         university_name,         email,         phone,         address,         status,         public_key,         certificate_certi_ids,         staff_staff_ids,         professor_profess_ids,         student_student_ids,         subject_subject_ids):
        transaction_signer = self._crypto_factory.new_signer(
            secp256k1.Secp256k1PrivateKey.from_hex(private_key))

        batch, batch_bytes = make_create_university_transaction(
            transaction_signer=transaction_signer,
            batch_signer=self._batch_signer,
            timestamp=timestamp,
            university_id=university_id,
            university_name=university_name,
            email=email,
            phone=phone,
            address=address,
            status=status,
            public_key=public_key,
            certificate_certi_ids=certificate_certi_ids,
            staff_staff_ids=staff_staff_ids,
            professor_profess_ids=professor_profess_ids,
            student_student_ids=student_student_ids,
            subject_subject_ids=subject_subject_ids
            )
        self._send_and_wait_for_commit(batch_bytes)
        return batch

    def send_create_certificate_transaction(self, private_key, timestamp,         certi_id,         cpa,         type,         status,         student_student_id,         university_university_id):
        transaction_signer = self._crypto_factory.new_signer(
            secp256k1.Secp256k1PrivateKey.from_hex(private_key))

        batch, batch_bytes = make_create_certificate_transaction(
            transaction_signer=transaction_signer,
            batch_signer=self._batch_signer,
            timestamp=timestamp,
            certi_id=certi_id,
            cpa=cpa,
            type=type,
            status=status,
            student_student_id=student_student_id,
            university_university_id=university_university_id
            )
        self._send_and_wait_for_commit(batch_bytes)
        return batch

    def send_update_result_transaction(self, private_key, timestamp,         result_id,         middlescore,         finallscore,         student_student_id,         classroom_class_id):
        transaction_signer = self._crypto_factory.new_signer(
            secp256k1.Secp256k1PrivateKey.from_hex(private_key))

        batch, batch_bytes = make_update_result_transaction(
            transaction_signer=transaction_signer,
            batch_signer=self._batch_signer,
            timestamp=timestamp,
            result_id=result_id,
            middlescore=middlescore,
            finallscore=finallscore,
            student_student_id=student_student_id,
            classroom_class_id=classroom_class_id
            )
        self._send_and_wait_for_commit(batch_bytes)
        return batch

    def send_update_subject_transaction(self, private_key, timestamp,         subject_id,         subject_name,         credit,         status,         classroom_class_ids,         university_university_id):
        transaction_signer = self._crypto_factory.new_signer(
            secp256k1.Secp256k1PrivateKey.from_hex(private_key))

        batch, batch_bytes = make_update_subject_transaction(
            transaction_signer=transaction_signer,
            batch_signer=self._batch_signer,
            timestamp=timestamp,
            subject_id=subject_id,
            subject_name=subject_name,
            credit=credit,
            status=status,
            classroom_class_ids=classroom_class_ids,
            university_university_id=university_university_id
            )
        self._send_and_wait_for_commit(batch_bytes)
        return batch

    def send_update_professor_transaction(self, private_key, timestamp,         profess_id,         name,         email,         phone,         address,         status,         public_key,         classroom_class_ids,         university_university_id):
        transaction_signer = self._crypto_factory.new_signer(
            secp256k1.Secp256k1PrivateKey.from_hex(private_key))

        batch, batch_bytes = make_update_professor_transaction(
            transaction_signer=transaction_signer,
            batch_signer=self._batch_signer,
            timestamp=timestamp,
            profess_id=profess_id,
            name=name,
            email=email,
            phone=phone,
            address=address,
            status=status,
            public_key=public_key,
            classroom_class_ids=classroom_class_ids,
            university_university_id=university_university_id
            )
        self._send_and_wait_for_commit(batch_bytes)
        return batch

    def send_update_student_transaction(self, private_key, timestamp,         student_id,         name,         phone,         email,         address,         public_key,         certificate_certi_ids,         result_result_ids,         university_university_id):
        transaction_signer = self._crypto_factory.new_signer(
            secp256k1.Secp256k1PrivateKey.from_hex(private_key))

        batch, batch_bytes = make_update_student_transaction(
            transaction_signer=transaction_signer,
            batch_signer=self._batch_signer,
            timestamp=timestamp,
            student_id=student_id,
            name=name,
            phone=phone,
            email=email,
            address=address,
            public_key=public_key,
            certificate_certi_ids=certificate_certi_ids,
            result_result_ids=result_result_ids,
            university_university_id=university_university_id
            )
        self._send_and_wait_for_commit(batch_bytes)
        return batch

    def send_update_classroom_transaction(self, private_key, timestamp,         class_id,         semester,         status,         subject_subject_id,         professor_profess_id,         result_result_ids):
        transaction_signer = self._crypto_factory.new_signer(
            secp256k1.Secp256k1PrivateKey.from_hex(private_key))

        batch, batch_bytes = make_update_classroom_transaction(
            transaction_signer=transaction_signer,
            batch_signer=self._batch_signer,
            timestamp=timestamp,
            class_id=class_id,
            semester=semester,
            status=status,
            subject_subject_id=subject_subject_id,
            professor_profess_id=professor_profess_id,
            result_result_ids=result_result_ids
            )
        self._send_and_wait_for_commit(batch_bytes)
        return batch

    def send_update_staff_transaction(self, private_key, timestamp,         staff_id,         name,         email,         phone,         address,         status,         public_key,         university_university_id):
        transaction_signer = self._crypto_factory.new_signer(
            secp256k1.Secp256k1PrivateKey.from_hex(private_key))

        batch, batch_bytes = make_update_staff_transaction(
            transaction_signer=transaction_signer,
            batch_signer=self._batch_signer,
            timestamp=timestamp,
            staff_id=staff_id,
            name=name,
            email=email,
            phone=phone,
            address=address,
            status=status,
            public_key=public_key,
            university_university_id=university_university_id
            )
        self._send_and_wait_for_commit(batch_bytes)
        return batch

    def send_update_university_transaction(self, private_key, timestamp,         university_id,         university_name,         email,         phone,         address,         status,         public_key,         certificate_certi_ids,         staff_staff_ids,         professor_profess_ids,         student_student_ids,         subject_subject_ids):
        transaction_signer = self._crypto_factory.new_signer(
            secp256k1.Secp256k1PrivateKey.from_hex(private_key))

        batch, batch_bytes = make_update_university_transaction(
            transaction_signer=transaction_signer,
            batch_signer=self._batch_signer,
            timestamp=timestamp,
            university_id=university_id,
            university_name=university_name,
            email=email,
            phone=phone,
            address=address,
            status=status,
            public_key=public_key,
            certificate_certi_ids=certificate_certi_ids,
            staff_staff_ids=staff_staff_ids,
            professor_profess_ids=professor_profess_ids,
            student_student_ids=student_student_ids,
            subject_subject_ids=subject_subject_ids
            )
        self._send_and_wait_for_commit(batch_bytes)
        return batch

    def send_update_certificate_transaction(self, private_key, timestamp,         certi_id,         cpa,         type,         status,         student_student_id,         university_university_id):
        transaction_signer = self._crypto_factory.new_signer(
            secp256k1.Secp256k1PrivateKey.from_hex(private_key))

        batch, batch_bytes = make_update_certificate_transaction(
            transaction_signer=transaction_signer,
            batch_signer=self._batch_signer,
            timestamp=timestamp,
            certi_id=certi_id,
            cpa=cpa,
            type=type,
            status=status,
            student_student_id=student_student_id,
            university_university_id=university_university_id
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
            max_try = 60
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

            