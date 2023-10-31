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
import datetime
from json.decoder import JSONDecodeError
import time
import datetime
import json
import requests
import base64

from google.protobuf.json_format import MessageToJson
from .errors import BadRequest, InternalError, CommunicationError
# generated from **Protobuf**
from .protobuf import result_pb2
from .protobuf import subject_pb2
from .protobuf import professor_pb2
from .protobuf import student_pb2
from .protobuf import classroom_pb2
from .protobuf import staff_pb2
from .protobuf import university_pb2
from .protobuf import certificate_pb2
from .protobuf import payload_pb2
from .addressing import addresser

from jsonschema import validate
from jsonschema import ValidationError
from .messaging import Messenger

from .AES_encrypt import AESCipher
from .file_handler import upload_file


class Handler(object):
    def __init__(self):
        validator_url='http://localhost:32001'
        endpoint='http://localhost:32002'
        self._messenger = Messenger(validator_url)
        self.endpoint = endpoint
        self.sdk_key = '1be13b50-6b26-4e41-bb30-920a18854813'
        self.data_folder_id = '6242749a0505467dc0bac291'
    
    def trace(self, transaction_ids):
        result = self.get_data_blockchain(transaction_ids)
        return result

    def gen_key_pair(self):
        public_key, private_key = self._messenger.get_new_key_pair()
        return public_key, private_key

    def create_result(self, result_id, middlescore, finallscore, student_student_id, classroom_class_id, private_key
):
        temp = {}
            
            
            
            
            
        
        batch = self._messenger.send_create_result_transaction(
            private_key=private_key,
            timestamp=get_time(),
            result_id=result_id,
    
            middlescore=middlescore,
    
            finallscore=finallscore,
    
            student_student_id=student_student_id,
    
            classroom_class_id=classroom_class_id
    
 
        )
        transaction_id = batch.transactions[0].header_signature
        return {
            "data": {
                "txid": transaction_id
            }
        }

    def create_subject(self, subject_id, subject_name, credit, status, classroom_class_ids, university_university_id, private_key
):
        temp = {}
            
            
            
            
            
            
        
        batch = self._messenger.send_create_subject_transaction(
            private_key=private_key,
            timestamp=get_time(),
            subject_id=subject_id,
    
            subject_name=subject_name,
    
            credit=credit,
    
            status=status,
    
            classroom_class_ids=classroom_class_ids,
    
            university_university_id=university_university_id
    
 
        )
        transaction_id = batch.transactions[0].header_signature
        return {
            "data": {
                "txid": transaction_id
            }
        }

    def create_professor(self, profess_id, name, email, phone, address, status, public_key, classroom_class_ids, university_university_id, private_key
):
        temp = {}
            
            
            
            
            
            
            
            
            
        
        batch = self._messenger.send_create_professor_transaction(
            private_key=private_key,
            timestamp=get_time(),
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
        transaction_id = batch.transactions[0].header_signature
        return {
            "data": {
                "txid": transaction_id
            }
        }

    def create_student(self, student_id, name, phone, email, address, public_key, certificate_certi_ids, result_result_ids, university_university_id, private_key
):
        temp = {}
            
            
            
            
            
            
            
            
            
        
        batch = self._messenger.send_create_student_transaction(
            private_key=private_key,
            timestamp=get_time(),
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
        transaction_id = batch.transactions[0].header_signature
        return {
            "data": {
                "txid": transaction_id
            }
        }

    def create_classroom(self, class_id, semester, status, subject_subject_id, professor_profess_id, result_result_ids, private_key
):
        temp = {}
            
            
            
            
            
            
        
        batch = self._messenger.send_create_classroom_transaction(
            private_key=private_key,
            timestamp=get_time(),
            class_id=class_id,
    
            semester=semester,
    
            status=status,
    
            subject_subject_id=subject_subject_id,
    
            professor_profess_id=professor_profess_id,
    
            result_result_ids=result_result_ids
    
 
        )
        transaction_id = batch.transactions[0].header_signature
        return {
            "data": {
                "txid": transaction_id
            }
        }

    def create_staff(self, staff_id, name, email, phone, address, status, public_key, university_university_id, private_key
):
        temp = {}
            
            
            
            
            
            
            
            
        
        batch = self._messenger.send_create_staff_transaction(
            private_key=private_key,
            timestamp=get_time(),
            staff_id=staff_id,
    
            name=name,
    
            email=email,
    
            phone=phone,
    
            address=address,
    
            status=status,
    
            public_key=public_key,
    
            university_university_id=university_university_id
    
 
        )
        transaction_id = batch.transactions[0].header_signature
        return {
            "data": {
                "txid": transaction_id
            }
        }

    def create_university(self, university_id, university_name, email, phone, address, status, public_key, certificate_certi_ids, staff_staff_ids, professor_profess_ids, student_student_ids, subject_subject_ids, private_key
):
        temp = {}
            
            
            
            
            
            
            
            
            
            
            
            
        
        batch = self._messenger.send_create_university_transaction(
            private_key=private_key,
            timestamp=get_time(),
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
        transaction_id = batch.transactions[0].header_signature
        return {
            "data": {
                "txid": transaction_id
            }
        }

    def create_certificate(self, certi_id, cpa, type, status, student_student_id, university_university_id, private_key
):
        temp = {}
            
            
            
            
            
            
        
        batch = self._messenger.send_create_certificate_transaction(
            private_key=private_key,
            timestamp=get_time(),
            certi_id=certi_id,
    
            cpa=cpa,
    
            type=type,
    
            status=status,
    
            student_student_id=student_student_id,
    
            university_university_id=university_university_id
    
 
        )
        transaction_id = batch.transactions[0].header_signature
        return {
            "data": {
                "txid": transaction_id
            }
        }

    def update_result(self, result_id, middlescore, finallscore, student_student_id, classroom_class_id, private_key
):
        temp = {}
            
            
            
            
            
        
        batch = self._messenger.send_update_result_transaction(
            private_key=private_key,
            timestamp=get_time(),
            result_id=result_id,
    
            middlescore=middlescore,
    
            finallscore=finallscore,
    
            student_student_id=student_student_id,
    
            classroom_class_id=classroom_class_id
    
 
        )
        transaction_id = batch.transactions[0].header_signature
        return {
            "data": {
                "txid": transaction_id
            }
        }

    def update_subject(self, subject_id, subject_name, credit, status, classroom_class_ids, university_university_id, private_key
):
        temp = {}
            
            
            
            
            
            
        
        batch = self._messenger.send_update_subject_transaction(
            private_key=private_key,
            timestamp=get_time(),
            subject_id=subject_id,
    
            subject_name=subject_name,
    
            credit=credit,
    
            status=status,
    
            classroom_class_ids=classroom_class_ids,
    
            university_university_id=university_university_id
    
 
        )
        transaction_id = batch.transactions[0].header_signature
        return {
            "data": {
                "txid": transaction_id
            }
        }

    def update_professor(self, profess_id, name, email, phone, address, status, public_key, classroom_class_ids, university_university_id, private_key
):
        temp = {}
            
            
            
            
            
            
            
            
            
        
        batch = self._messenger.send_update_professor_transaction(
            private_key=private_key,
            timestamp=get_time(),
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
        transaction_id = batch.transactions[0].header_signature
        return {
            "data": {
                "txid": transaction_id
            }
        }

    def update_student(self, student_id, name, phone, email, address, public_key, certificate_certi_ids, result_result_ids, university_university_id, private_key
):
        temp = {}
            
            
            
            
            
            
            
            
            
        
        batch = self._messenger.send_update_student_transaction(
            private_key=private_key,
            timestamp=get_time(),
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
        transaction_id = batch.transactions[0].header_signature
        return {
            "data": {
                "txid": transaction_id
            }
        }

    def update_classroom(self, class_id, semester, status, subject_subject_id, professor_profess_id, result_result_ids, private_key
):
        temp = {}
            
            
            
            
            
            
        
        batch = self._messenger.send_update_classroom_transaction(
            private_key=private_key,
            timestamp=get_time(),
            class_id=class_id,
    
            semester=semester,
    
            status=status,
    
            subject_subject_id=subject_subject_id,
    
            professor_profess_id=professor_profess_id,
    
            result_result_ids=result_result_ids
    
 
        )
        transaction_id = batch.transactions[0].header_signature
        return {
            "data": {
                "txid": transaction_id
            }
        }

    def update_staff(self, staff_id, name, email, phone, address, status, public_key, university_university_id, private_key
):
        temp = {}
            
            
            
            
            
            
            
            
        
        batch = self._messenger.send_update_staff_transaction(
            private_key=private_key,
            timestamp=get_time(),
            staff_id=staff_id,
    
            name=name,
    
            email=email,
    
            phone=phone,
    
            address=address,
    
            status=status,
    
            public_key=public_key,
    
            university_university_id=university_university_id
    
 
        )
        transaction_id = batch.transactions[0].header_signature
        return {
            "data": {
                "txid": transaction_id
            }
        }

    def update_university(self, university_id, university_name, email, phone, address, status, public_key, certificate_certi_ids, staff_staff_ids, professor_profess_ids, student_student_ids, subject_subject_ids, private_key
):
        temp = {}
            
            
            
            
            
            
            
            
            
            
            
            
        
        batch = self._messenger.send_update_university_transaction(
            private_key=private_key,
            timestamp=get_time(),
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
        transaction_id = batch.transactions[0].header_signature
        return {
            "data": {
                "txid": transaction_id
            }
        }

    def update_certificate(self, certi_id, cpa, type, status, student_student_id, university_university_id, private_key
):
        temp = {}
            
            
            
            
            
            
        
        batch = self._messenger.send_update_certificate_transaction(
            private_key=private_key,
            timestamp=get_time(),
            certi_id=certi_id,
    
            cpa=cpa,
    
            type=type,
    
            status=status,
    
            student_student_id=student_student_id,
    
            university_university_id=university_university_id
    
 
        )
        transaction_id = batch.transactions[0].header_signature
        return {
            "data": {
                "txid": transaction_id
            }
        }

    def get_result(self, result_id):
        result_address = addresser.get_result_address(result_id)

        url = '{}/state/{}'.format(self.endpoint, result_address)
        response = requests.get(url)
        if response.status_code == 200:
            try:
                content = response.content
                content_json = content.decode('utf8').replace("'", '"')
                payload_bytes_response = json.loads(content_json)['data']
                container = result_pb2.ResultContainer()
                container.ParseFromString(base64.b64decode(payload_bytes_response))
                json_data = json.loads(MessageToJson(container, preserving_proto_field_name=True))
                return {
                    "data": {
                        'result': json_data["entries"][0],
                    }
                }
            except:
                raise InternalError('Cannot decode the response')
        else:
            raise CommunicationError('Cannot get result with result_id={}'.format(result_id))

    def get_subject(self, subject_id):
        subject_address = addresser.get_subject_address(subject_id)

        url = '{}/state/{}'.format(self.endpoint, subject_address)
        response = requests.get(url)
        if response.status_code == 200:
            try:
                content = response.content
                content_json = content.decode('utf8').replace("'", '"')
                payload_bytes_response = json.loads(content_json)['data']
                container = subject_pb2.SubjectContainer()
                container.ParseFromString(base64.b64decode(payload_bytes_response))
                json_data = json.loads(MessageToJson(container, preserving_proto_field_name=True))
                return {
                    "data": {
                        'subject': json_data["entries"][0],
                    }
                }
            except:
                raise InternalError('Cannot decode the response')
        else:
            raise CommunicationError('Cannot get subject with subject_id={}'.format(subject_id))

    def get_professor(self, profess_id):
        professor_address = addresser.get_professor_address(profess_id)

        url = '{}/state/{}'.format(self.endpoint, professor_address)
        response = requests.get(url)
        if response.status_code == 200:
            try:
                content = response.content
                content_json = content.decode('utf8').replace("'", '"')
                payload_bytes_response = json.loads(content_json)['data']
                container = professor_pb2.ProfessorContainer()
                container.ParseFromString(base64.b64decode(payload_bytes_response))
                json_data = json.loads(MessageToJson(container, preserving_proto_field_name=True))
                return {
                    "data": {
                        'professor': json_data["entries"][0],
                    }
                }
            except:
                raise InternalError('Cannot decode the response')
        else:
            raise CommunicationError('Cannot get professor with profess_id={}'.format(profess_id))

    def get_student(self, student_id):
        student_address = addresser.get_student_address(student_id)

        url = '{}/state/{}'.format(self.endpoint, student_address)
        response = requests.get(url)
        if response.status_code == 200:
            try:
                content = response.content
                content_json = content.decode('utf8').replace("'", '"')
                payload_bytes_response = json.loads(content_json)['data']
                container = student_pb2.StudentContainer()
                container.ParseFromString(base64.b64decode(payload_bytes_response))
                json_data = json.loads(MessageToJson(container, preserving_proto_field_name=True))
                return {
                    "data": {
                        'student': json_data["entries"][0],
                    }
                }
            except:
                raise InternalError('Cannot decode the response')
        else:
            raise CommunicationError('Cannot get student with student_id={}'.format(student_id))

    def get_classroom(self, class_id):
        classroom_address = addresser.get_classroom_address(class_id)

        url = '{}/state/{}'.format(self.endpoint, classroom_address)
        response = requests.get(url)
        if response.status_code == 200:
            try:
                content = response.content
                content_json = content.decode('utf8').replace("'", '"')
                payload_bytes_response = json.loads(content_json)['data']
                container = classroom_pb2.ClassroomContainer()
                container.ParseFromString(base64.b64decode(payload_bytes_response))
                json_data = json.loads(MessageToJson(container, preserving_proto_field_name=True))
                return {
                    "data": {
                        'classroom': json_data["entries"][0],
                    }
                }
            except:
                raise InternalError('Cannot decode the response')
        else:
            raise CommunicationError('Cannot get classroom with class_id={}'.format(class_id))

    def get_staff(self, staff_id):
        staff_address = addresser.get_staff_address(staff_id)

        url = '{}/state/{}'.format(self.endpoint, staff_address)
        response = requests.get(url)
        if response.status_code == 200:
            try:
                content = response.content
                content_json = content.decode('utf8').replace("'", '"')
                payload_bytes_response = json.loads(content_json)['data']
                container = staff_pb2.StaffContainer()
                container.ParseFromString(base64.b64decode(payload_bytes_response))
                json_data = json.loads(MessageToJson(container, preserving_proto_field_name=True))
                return {
                    "data": {
                        'staff': json_data["entries"][0],
                    }
                }
            except:
                raise InternalError('Cannot decode the response')
        else:
            raise CommunicationError('Cannot get staff with staff_id={}'.format(staff_id))

    def get_university(self, university_id):
        university_address = addresser.get_university_address(university_id)

        url = '{}/state/{}'.format(self.endpoint, university_address)
        response = requests.get(url)
        if response.status_code == 200:
            try:
                content = response.content
                content_json = content.decode('utf8').replace("'", '"')
                payload_bytes_response = json.loads(content_json)['data']
                container = university_pb2.UniversityContainer()
                container.ParseFromString(base64.b64decode(payload_bytes_response))
                json_data = json.loads(MessageToJson(container, preserving_proto_field_name=True))
                return {
                    "data": {
                        'university': json_data["entries"][0],
                    }
                }
            except:
                raise InternalError('Cannot decode the response')
        else:
            raise CommunicationError('Cannot get university with university_id={}'.format(university_id))

    def get_certificate(self, certi_id):
        certificate_address = addresser.get_certificate_address(certi_id)

        url = '{}/state/{}'.format(self.endpoint, certificate_address)
        response = requests.get(url)
        if response.status_code == 200:
            try:
                content = response.content
                content_json = content.decode('utf8').replace("'", '"')
                payload_bytes_response = json.loads(content_json)['data']
                container = certificate_pb2.CertificateContainer()
                container.ParseFromString(base64.b64decode(payload_bytes_response))
                json_data = json.loads(MessageToJson(container, preserving_proto_field_name=True))
                return {
                    "data": {
                        'certificate': json_data["entries"][0],
                    }
                }
            except:
                raise InternalError('Cannot decode the response')
        else:
            raise CommunicationError('Cannot get certificate with certi_id={}'.format(certi_id))

    def get_data_blockchain(self, transaction_ids):
        results = []
        for transaction_id in transaction_ids:
            url = '{}/transactions/{}'.format(self.endpoint, transaction_id)
            response = requests.get(url)
            if response.status_code == 200:
                try:
                    transaction_dict = json.loads(response.content)
                    payload_string = transaction_dict['data']['payload']
                    data_model = payload_pb2.DappPayload()
                    data_model.ParseFromString(base64.b64decode(payload_string))
                    json_data = json.loads(MessageToJson(data_model, preserving_proto_field_name=True))
                    transaction_dict["payload_decode"] = json_data
                    # for key, value in json_data.items():
                    #     if key != "action" and key != "timestamp":
                    #         result = {}
                    #         for property_key, property_value in value.items():
                    #             split_name = property_key.split("__")
                    #             if len(split_name) == 1:
                    #                 result[split_name[0]] = property_value
                    #             else:
                    #                 current_level = result
                    #                 for index in range(len(split_name)):
                    #                     if index == len(split_name)-1:
                    #                         current_level[split_name[index]] = property_value
                    #                         break
                    #                     if split_name[index] not in current_level:
                    #                         current_level[split_name[index]] = {}
                    #                     current_level = current_level[split_name[index]]
                    #         results.append(result)
                    results.append(transaction_dict)
                except:
                    raise CommunicationError("Error to get data from blockchain")

        return results

def validate_fields(required_fields, body):
    for field in required_fields:
        if body.get(field) is None:
            raise BadRequest(
                "'{}' parameter is required".format(field))


def validate_types(schema, body):
    try:
        validate(instance=body, schema=schema)
    except ValidationError as e:
        string_array_error = str(e).split("\n")
        array = {"On instance","[","]","'",":"," "}
        for a in array:
            string_array_error[5] = string_array_error[5].replace(a,"")
        message = string_array_error[0]+" on field '"+ string_array_error[5] +"'"

        raise BadRequest(message)

def get_time():
    dts = datetime.datetime.utcnow()
    return round(time.mktime(dts.timetuple()) + dts.microsecond/1e6)