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
    result_id, 
    middlescore, 
    finallscore, 
    student_student_id, 
    classroom_class_id
):

    result_address = addresser.get_result_address(result_id)
    
    inputs = [result_address]
    outputs = [result_address]

    action = payload_pb2.CreateResultAction(
        result_id=result_id,
        middlescore=middlescore,
        finallscore=finallscore,
        student_student_id=student_student_id,
        classroom_class_id=classroom_class_id
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
    subject_id, 
    subject_name, 
    credit, 
    status, 
    classroom_class_ids, 
    university_university_id
):

    subject_address = addresser.get_subject_address(subject_id)
    
    inputs = [subject_address]
    outputs = [subject_address]

    action = payload_pb2.CreateSubjectAction(
        subject_id=subject_id,
        subject_name=subject_name,
        credit=credit,
        status=status,
        classroom_class_ids=classroom_class_ids,
        university_university_id=university_university_id
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
    profess_id, 
    name, 
    email, 
    phone, 
    address, 
    status, 
    public_key, 
    classroom_class_ids, 
    university_university_id
):

    professor_address = addresser.get_professor_address(profess_id)
    
    inputs = [professor_address]
    outputs = [professor_address]

    action = payload_pb2.CreateProfessorAction(
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
    student_id, 
    name, 
    phone, 
    email, 
    address, 
    public_key, 
    certificate_certi_ids, 
    result_result_ids, 
    university_university_id
):

    student_address = addresser.get_student_address(student_id)
    
    inputs = [student_address]
    outputs = [student_address]

    action = payload_pb2.CreateStudentAction(
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
    class_id, 
    semester, 
    status, 
    subject_subject_id, 
    professor_profess_id, 
    result_result_ids
):

    classroom_address = addresser.get_classroom_address(class_id)
    
    inputs = [classroom_address]
    outputs = [classroom_address]

    action = payload_pb2.CreateClassroomAction(
        class_id=class_id,
        semester=semester,
        status=status,
        subject_subject_id=subject_subject_id,
        professor_profess_id=professor_profess_id,
        result_result_ids=result_result_ids
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
    staff_id, 
    name, 
    email, 
    phone, 
    address, 
    status, 
    public_key, 
    university_university_id
):

    staff_address = addresser.get_staff_address(staff_id)
    
    inputs = [staff_address]
    outputs = [staff_address]

    action = payload_pb2.CreateStaffAction(
        staff_id=staff_id,
        name=name,
        email=email,
        phone=phone,
        address=address,
        status=status,
        public_key=public_key,
        university_university_id=university_university_id
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
    university_id, 
    university_name, 
    email, 
    phone, 
    address, 
    status, 
    public_key, 
    certificate_certi_ids, 
    staff_staff_ids, 
    professor_profess_ids, 
    student_student_ids, 
    subject_subject_ids
):

    university_address = addresser.get_university_address(university_id)
    
    inputs = [university_address]
    outputs = [university_address]

    action = payload_pb2.CreateUniversityAction(
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
    certi_id, 
    cpa, 
    type, 
    status, 
    student_student_id, 
    university_university_id
):

    certificate_address = addresser.get_certificate_address(certi_id)
    
    inputs = [certificate_address]
    outputs = [certificate_address]

    action = payload_pb2.CreateCertificateAction(
        certi_id=certi_id,
        cpa=cpa,
        type=type,
        status=status,
        student_student_id=student_student_id,
        university_university_id=university_university_id
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
    result_id, 
    middlescore, 
    finallscore, 
    student_student_id, 
    classroom_class_id
):

    result_address = addresser.get_result_address(result_id)
    
    inputs = [result_address]
    outputs = [result_address]

    action = payload_pb2.UpdateResultAction(
        result_id=result_id,
        middlescore=middlescore,
        finallscore=finallscore,
        student_student_id=student_student_id,
        classroom_class_id=classroom_class_id
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
    subject_id, 
    subject_name, 
    credit, 
    status, 
    classroom_class_ids, 
    university_university_id
):

    subject_address = addresser.get_subject_address(subject_id)
    
    inputs = [subject_address]
    outputs = [subject_address]

    action = payload_pb2.UpdateSubjectAction(
        subject_id=subject_id,
        subject_name=subject_name,
        credit=credit,
        status=status,
        classroom_class_ids=classroom_class_ids,
        university_university_id=university_university_id
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
    profess_id, 
    name, 
    email, 
    phone, 
    address, 
    status, 
    public_key, 
    classroom_class_ids, 
    university_university_id
):

    professor_address = addresser.get_professor_address(profess_id)
    
    inputs = [professor_address]
    outputs = [professor_address]

    action = payload_pb2.UpdateProfessorAction(
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
    student_id, 
    name, 
    phone, 
    email, 
    address, 
    public_key, 
    certificate_certi_ids, 
    result_result_ids, 
    university_university_id
):

    student_address = addresser.get_student_address(student_id)
    
    inputs = [student_address]
    outputs = [student_address]

    action = payload_pb2.UpdateStudentAction(
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
    class_id, 
    semester, 
    status, 
    subject_subject_id, 
    professor_profess_id, 
    result_result_ids
):

    classroom_address = addresser.get_classroom_address(class_id)
    
    inputs = [classroom_address]
    outputs = [classroom_address]

    action = payload_pb2.UpdateClassroomAction(
        class_id=class_id,
        semester=semester,
        status=status,
        subject_subject_id=subject_subject_id,
        professor_profess_id=professor_profess_id,
        result_result_ids=result_result_ids
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
    staff_id, 
    name, 
    email, 
    phone, 
    address, 
    status, 
    public_key, 
    university_university_id
):

    staff_address = addresser.get_staff_address(staff_id)
    
    inputs = [staff_address]
    outputs = [staff_address]

    action = payload_pb2.UpdateStaffAction(
        staff_id=staff_id,
        name=name,
        email=email,
        phone=phone,
        address=address,
        status=status,
        public_key=public_key,
        university_university_id=university_university_id
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
    university_id, 
    university_name, 
    email, 
    phone, 
    address, 
    status, 
    public_key, 
    certificate_certi_ids, 
    staff_staff_ids, 
    professor_profess_ids, 
    student_student_ids, 
    subject_subject_ids
):

    university_address = addresser.get_university_address(university_id)
    
    inputs = [university_address]
    outputs = [university_address]

    action = payload_pb2.UpdateUniversityAction(
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
    certi_id, 
    cpa, 
    type, 
    status, 
    student_student_id, 
    university_university_id
):

    certificate_address = addresser.get_certificate_address(certi_id)
    
    inputs = [certificate_address]
    outputs = [certificate_address]

    action = payload_pb2.UpdateCertificateAction(
        certi_id=certi_id,
        cpa=cpa,
        type=type,
        status=status,
        student_student_id=student_student_id,
        university_university_id=university_university_id
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