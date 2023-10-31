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
# -----------------------------------------------------------------------------

import hashlib
import logging

from sawtooth_sdk.protobuf import batch_pb2
from sawtooth_sdk.protobuf import transaction_pb2

from .addressing import addresser
from .protobuf import payload_pb2

LOGGER = logging.getLogger(__name__)


def make_create_result_transaction(
    transaction_signer, batch_signer, timestamp, 
    att_result_id, 
    att_middlescore, 
    att_finallscore, 
    for_student_student_id, 
    for_classroom_class_id
):

    result_address = addresser.get_result_address(att_result_id)
    
    inputs = [result_address]
    outputs = [result_address]

    action = payload_pb2.CreateResultAction(
        att_result_id=att_result_id,
        att_middlescore=att_middlescore,
        att_finallscore=att_finallscore,
        for_student_student_id=for_student_student_id,
        for_classroom_class_id=for_classroom_class_id
    )

    payload = payload_pb2.DappPayload(
        action=payload_pb2.DappPayload.CREATE_RESULT,
        create_result=action,
        timestamp=timestamp
    )
    payload_bytes = payload.SerializeToString()

    return _make_batch(
        payload_bytes=payload_bytes,
        inputs=inputs,
        outputs=outputs,
        transaction_signer=transaction_signer,
        batch_signer=batch_signer
    )

def make_create_subject_transaction(
    transaction_signer, batch_signer, timestamp, 
    att_subject_id, 
    att_subject_name, 
    att_credit, 
    att_status, 
    for_classroom_class_ids, 
    for_university_university_id
):

    subject_address = addresser.get_subject_address(att_subject_id)
    
    inputs = [subject_address]
    outputs = [subject_address]

    action = payload_pb2.CreateSubjectAction(
        att_subject_id=att_subject_id,
        att_subject_name=att_subject_name,
        att_credit=att_credit,
        att_status=att_status,
        for_classroom_class_ids=for_classroom_class_ids,
        for_university_university_id=for_university_university_id
    )

    payload = payload_pb2.DappPayload(
        action=payload_pb2.DappPayload.CREATE_SUBJECT,
        create_subject=action,
        timestamp=timestamp
    )
    payload_bytes = payload.SerializeToString()

    return _make_batch(
        payload_bytes=payload_bytes,
        inputs=inputs,
        outputs=outputs,
        transaction_signer=transaction_signer,
        batch_signer=batch_signer
    )

def make_create_professor_transaction(
    transaction_signer, batch_signer, timestamp, 
    att_profess_id, 
    att_name, 
    att_email, 
    att_phone, 
    att_address, 
    att_status, 
    att_public_key, 
    for_classroom_class_ids, 
    for_university_university_id
):

    professor_address = addresser.get_professor_address(att_profess_id)
    
    inputs = [professor_address]
    outputs = [professor_address]

    action = payload_pb2.CreateProfessorAction(
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

    payload = payload_pb2.DappPayload(
        action=payload_pb2.DappPayload.CREATE_PROFESSOR,
        create_professor=action,
        timestamp=timestamp
    )
    payload_bytes = payload.SerializeToString()

    return _make_batch(
        payload_bytes=payload_bytes,
        inputs=inputs,
        outputs=outputs,
        transaction_signer=transaction_signer,
        batch_signer=batch_signer
    )

def make_create_student_transaction(
    transaction_signer, batch_signer, timestamp, 
    att_student_id, 
    att_name, 
    att_phone, 
    att_email, 
    att_address, 
    att_public_key, 
    for_certificate_certi_ids, 
    for_result_result_ids, 
    for_university_university_id
):

    student_address = addresser.get_student_address(att_student_id)
    
    inputs = [student_address]
    outputs = [student_address]

    action = payload_pb2.CreateStudentAction(
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

    payload = payload_pb2.DappPayload(
        action=payload_pb2.DappPayload.CREATE_STUDENT,
        create_student=action,
        timestamp=timestamp
    )
    payload_bytes = payload.SerializeToString()

    return _make_batch(
        payload_bytes=payload_bytes,
        inputs=inputs,
        outputs=outputs,
        transaction_signer=transaction_signer,
        batch_signer=batch_signer
    )

def make_create_classroom_transaction(
    transaction_signer, batch_signer, timestamp, 
    att_class_id, 
    att_semester, 
    att_status, 
    for_subject_subject_id, 
    for_professor_profess_id, 
    for_result_result_ids
):

    classroom_address = addresser.get_classroom_address(att_class_id)
    
    inputs = [classroom_address]
    outputs = [classroom_address]

    action = payload_pb2.CreateClassroomAction(
        att_class_id=att_class_id,
        att_semester=att_semester,
        att_status=att_status,
        for_subject_subject_id=for_subject_subject_id,
        for_professor_profess_id=for_professor_profess_id,
        for_result_result_ids=for_result_result_ids
    )

    payload = payload_pb2.DappPayload(
        action=payload_pb2.DappPayload.CREATE_CLASSROOM,
        create_classroom=action,
        timestamp=timestamp
    )
    payload_bytes = payload.SerializeToString()

    return _make_batch(
        payload_bytes=payload_bytes,
        inputs=inputs,
        outputs=outputs,
        transaction_signer=transaction_signer,
        batch_signer=batch_signer
    )

def make_create_staff_transaction(
    transaction_signer, batch_signer, timestamp, 
    att_staff_id, 
    att_name, 
    att_email, 
    att_phone, 
    att_address, 
    att_status, 
    att_public_key, 
    for_university_university_id
):

    staff_address = addresser.get_staff_address(att_staff_id)
    
    inputs = [staff_address]
    outputs = [staff_address]

    action = payload_pb2.CreateStaffAction(
        att_staff_id=att_staff_id,
        att_name=att_name,
        att_email=att_email,
        att_phone=att_phone,
        att_address=att_address,
        att_status=att_status,
        att_public_key=att_public_key,
        for_university_university_id=for_university_university_id
    )

    payload = payload_pb2.DappPayload(
        action=payload_pb2.DappPayload.CREATE_STAFF,
        create_staff=action,
        timestamp=timestamp
    )
    payload_bytes = payload.SerializeToString()

    return _make_batch(
        payload_bytes=payload_bytes,
        inputs=inputs,
        outputs=outputs,
        transaction_signer=transaction_signer,
        batch_signer=batch_signer
    )

def make_create_university_transaction(
    transaction_signer, batch_signer, timestamp, 
    att_university_id, 
    att_university_name, 
    att_email, 
    att_phone, 
    att_address, 
    att_status, 
    att_public_key, 
    for_certificate_certi_ids, 
    for_staff_staff_ids, 
    for_professor_profess_ids, 
    for_student_student_ids, 
    for_subject_subject_ids
):

    university_address = addresser.get_university_address(att_university_id)
    
    inputs = [university_address]
    outputs = [university_address]

    action = payload_pb2.CreateUniversityAction(
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

    payload = payload_pb2.DappPayload(
        action=payload_pb2.DappPayload.CREATE_UNIVERSITY,
        create_university=action,
        timestamp=timestamp
    )
    payload_bytes = payload.SerializeToString()

    return _make_batch(
        payload_bytes=payload_bytes,
        inputs=inputs,
        outputs=outputs,
        transaction_signer=transaction_signer,
        batch_signer=batch_signer
    )

def make_create_certificate_transaction(
    transaction_signer, batch_signer, timestamp, 
    att_certi_id, 
    att_cpa, 
    att_type, 
    att_status, 
    for_student_student_id, 
    for_university_university_id
):

    certificate_address = addresser.get_certificate_address(att_certi_id)
    
    inputs = [certificate_address]
    outputs = [certificate_address]

    action = payload_pb2.CreateCertificateAction(
        att_certi_id=att_certi_id,
        att_cpa=att_cpa,
        att_type=att_type,
        att_status=att_status,
        for_student_student_id=for_student_student_id,
        for_university_university_id=for_university_university_id
    )

    payload = payload_pb2.DappPayload(
        action=payload_pb2.DappPayload.CREATE_CERTIFICATE,
        create_certificate=action,
        timestamp=timestamp
    )
    payload_bytes = payload.SerializeToString()

    return _make_batch(
        payload_bytes=payload_bytes,
        inputs=inputs,
        outputs=outputs,
        transaction_signer=transaction_signer,
        batch_signer=batch_signer
    )

def make_update_result_transaction(
    transaction_signer, batch_signer, timestamp, 
    att_result_id, 
    att_middlescore, 
    att_finallscore, 
    for_student_student_id, 
    for_classroom_class_id
):

    result_address = addresser.get_result_address(att_result_id)
    
    inputs = [result_address]
    outputs = [result_address]

    action = payload_pb2.UpdateResultAction(
        att_result_id=att_result_id,
        att_middlescore=att_middlescore,
        att_finallscore=att_finallscore,
        for_student_student_id=for_student_student_id,
        for_classroom_class_id=for_classroom_class_id
    )

    payload = payload_pb2.DappPayload(
        action=payload_pb2.DappPayload.UPDATE_RESULT,
        update_result=action,
        timestamp=timestamp
    )
    payload_bytes = payload.SerializeToString()

    return _make_batch(
        payload_bytes=payload_bytes,
        inputs=inputs,
        outputs=outputs,
        transaction_signer=transaction_signer,
        batch_signer=batch_signer
    )

def make_update_subject_transaction(
    transaction_signer, batch_signer, timestamp, 
    att_subject_id, 
    att_subject_name, 
    att_credit, 
    att_status, 
    for_classroom_class_ids, 
    for_university_university_id
):

    subject_address = addresser.get_subject_address(att_subject_id)
    
    inputs = [subject_address]
    outputs = [subject_address]

    action = payload_pb2.UpdateSubjectAction(
        att_subject_id=att_subject_id,
        att_subject_name=att_subject_name,
        att_credit=att_credit,
        att_status=att_status,
        for_classroom_class_ids=for_classroom_class_ids,
        for_university_university_id=for_university_university_id
    )

    payload = payload_pb2.DappPayload(
        action=payload_pb2.DappPayload.UPDATE_SUBJECT,
        update_subject=action,
        timestamp=timestamp
    )
    payload_bytes = payload.SerializeToString()

    return _make_batch(
        payload_bytes=payload_bytes,
        inputs=inputs,
        outputs=outputs,
        transaction_signer=transaction_signer,
        batch_signer=batch_signer
    )

def make_update_professor_transaction(
    transaction_signer, batch_signer, timestamp, 
    att_profess_id, 
    att_name, 
    att_email, 
    att_phone, 
    att_address, 
    att_status, 
    att_public_key, 
    for_classroom_class_ids, 
    for_university_university_id
):

    professor_address = addresser.get_professor_address(att_profess_id)
    
    inputs = [professor_address]
    outputs = [professor_address]

    action = payload_pb2.UpdateProfessorAction(
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

    payload = payload_pb2.DappPayload(
        action=payload_pb2.DappPayload.UPDATE_PROFESSOR,
        update_professor=action,
        timestamp=timestamp
    )
    payload_bytes = payload.SerializeToString()

    return _make_batch(
        payload_bytes=payload_bytes,
        inputs=inputs,
        outputs=outputs,
        transaction_signer=transaction_signer,
        batch_signer=batch_signer
    )

def make_update_student_transaction(
    transaction_signer, batch_signer, timestamp, 
    att_student_id, 
    att_name, 
    att_phone, 
    att_email, 
    att_address, 
    att_public_key, 
    for_certificate_certi_ids, 
    for_result_result_ids, 
    for_university_university_id
):

    student_address = addresser.get_student_address(att_student_id)
    
    inputs = [student_address]
    outputs = [student_address]

    action = payload_pb2.UpdateStudentAction(
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

    payload = payload_pb2.DappPayload(
        action=payload_pb2.DappPayload.UPDATE_STUDENT,
        update_student=action,
        timestamp=timestamp
    )
    payload_bytes = payload.SerializeToString()

    return _make_batch(
        payload_bytes=payload_bytes,
        inputs=inputs,
        outputs=outputs,
        transaction_signer=transaction_signer,
        batch_signer=batch_signer
    )

def make_update_classroom_transaction(
    transaction_signer, batch_signer, timestamp, 
    att_class_id, 
    att_semester, 
    att_status, 
    for_subject_subject_id, 
    for_professor_profess_id, 
    for_result_result_ids
):

    classroom_address = addresser.get_classroom_address(att_class_id)
    
    inputs = [classroom_address]
    outputs = [classroom_address]

    action = payload_pb2.UpdateClassroomAction(
        att_class_id=att_class_id,
        att_semester=att_semester,
        att_status=att_status,
        for_subject_subject_id=for_subject_subject_id,
        for_professor_profess_id=for_professor_profess_id,
        for_result_result_ids=for_result_result_ids
    )

    payload = payload_pb2.DappPayload(
        action=payload_pb2.DappPayload.UPDATE_CLASSROOM,
        update_classroom=action,
        timestamp=timestamp
    )
    payload_bytes = payload.SerializeToString()

    return _make_batch(
        payload_bytes=payload_bytes,
        inputs=inputs,
        outputs=outputs,
        transaction_signer=transaction_signer,
        batch_signer=batch_signer
    )

def make_update_staff_transaction(
    transaction_signer, batch_signer, timestamp, 
    att_staff_id, 
    att_name, 
    att_email, 
    att_phone, 
    att_address, 
    att_status, 
    att_public_key, 
    for_university_university_id
):

    staff_address = addresser.get_staff_address(att_staff_id)
    
    inputs = [staff_address]
    outputs = [staff_address]

    action = payload_pb2.UpdateStaffAction(
        att_staff_id=att_staff_id,
        att_name=att_name,
        att_email=att_email,
        att_phone=att_phone,
        att_address=att_address,
        att_status=att_status,
        att_public_key=att_public_key,
        for_university_university_id=for_university_university_id
    )

    payload = payload_pb2.DappPayload(
        action=payload_pb2.DappPayload.UPDATE_STAFF,
        update_staff=action,
        timestamp=timestamp
    )
    payload_bytes = payload.SerializeToString()

    return _make_batch(
        payload_bytes=payload_bytes,
        inputs=inputs,
        outputs=outputs,
        transaction_signer=transaction_signer,
        batch_signer=batch_signer
    )

def make_update_university_transaction(
    transaction_signer, batch_signer, timestamp, 
    att_university_id, 
    att_university_name, 
    att_email, 
    att_phone, 
    att_address, 
    att_status, 
    att_public_key, 
    for_certificate_certi_ids, 
    for_staff_staff_ids, 
    for_professor_profess_ids, 
    for_student_student_ids, 
    for_subject_subject_ids
):

    university_address = addresser.get_university_address(att_university_id)
    
    inputs = [university_address]
    outputs = [university_address]

    action = payload_pb2.UpdateUniversityAction(
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

    payload = payload_pb2.DappPayload(
        action=payload_pb2.DappPayload.UPDATE_UNIVERSITY,
        update_university=action,
        timestamp=timestamp
    )
    payload_bytes = payload.SerializeToString()

    return _make_batch(
        payload_bytes=payload_bytes,
        inputs=inputs,
        outputs=outputs,
        transaction_signer=transaction_signer,
        batch_signer=batch_signer
    )

def make_update_certificate_transaction(
    transaction_signer, batch_signer, timestamp, 
    att_certi_id, 
    att_cpa, 
    att_type, 
    att_status, 
    for_student_student_id, 
    for_university_university_id
):

    certificate_address = addresser.get_certificate_address(att_certi_id)
    
    inputs = [certificate_address]
    outputs = [certificate_address]

    action = payload_pb2.UpdateCertificateAction(
        att_certi_id=att_certi_id,
        att_cpa=att_cpa,
        att_type=att_type,
        att_status=att_status,
        for_student_student_id=for_student_student_id,
        for_university_university_id=for_university_university_id
    )

    payload = payload_pb2.DappPayload(
        action=payload_pb2.DappPayload.UPDATE_CERTIFICATE,
        update_certificate=action,
        timestamp=timestamp
    )
    payload_bytes = payload.SerializeToString()

    return _make_batch(
        payload_bytes=payload_bytes,
        inputs=inputs,
        outputs=outputs,
        transaction_signer=transaction_signer,
        batch_signer=batch_signer
    )

def _make_batch(payload_bytes,
                inputs,
                outputs,
                transaction_signer,
                batch_signer):

    transaction_header = transaction_pb2.TransactionHeader(
        family_name=addresser.FAMILY_NAME,
        family_version=addresser.FAMILY_VERSION,
        inputs=inputs,
        outputs=outputs,
        signer_public_key=transaction_signer.get_public_key().as_hex(),
        batcher_public_key=batch_signer.get_public_key().as_hex(),
        dependencies=[],
        payload_sha512=hashlib.sha512(payload_bytes).hexdigest())
    transaction_header_bytes = transaction_header.SerializeToString()

    transaction = transaction_pb2.Transaction(
        header=transaction_header_bytes,
        header_signature=transaction_signer.sign(transaction_header_bytes),
        payload=payload_bytes)

    batch_header = batch_pb2.BatchHeader(
        signer_public_key=batch_signer.get_public_key().as_hex(),
        transaction_ids=[transaction.header_signature])
    batch_header_bytes = batch_header.SerializeToString()

    batch = batch_pb2.Batch(
        header=batch_header_bytes,
        header_signature=batch_signer.sign(batch_header_bytes),
        transactions=[transaction])
    
    batch_list = batch_pb2.BatchList(batches=[batch])
    batch_bytes = batch_list.SerializeToString()

    return batch, batch_bytes