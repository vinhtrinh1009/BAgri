import enum
import hashlib


FAMILY_NAME = 'BCERTVERYFINAL-1F654'
FAMILY_VERSION = '1'
NAMESPACE = hashlib.sha512(FAMILY_NAME.encode('utf-8')).hexdigest()[:6]

RESULT_PREFIX = '00'
SUBJECT_PREFIX = '01'
PROFESSOR_PREFIX = '02'
STUDENT_PREFIX = '03'
CLASSROOM_PREFIX = '04'
STAFF_PREFIX = '05'
UNIVERSITY_PREFIX = '06'
CERTIFICATE_PREFIX = '07'


@enum.unique
class AddressSpace(enum.IntEnum):
    RESULT = 0
    SUBJECT = 1
    PROFESSOR = 2
    STUDENT = 3
    CLASSROOM = 4
    STAFF = 5
    UNIVERSITY = 6
    CERTIFICATE = 7
    OTHER_FAMILY = 100


def get_result_address(att_result_id):
    return NAMESPACE + RESULT_PREFIX + hashlib.sha512(
        att_result_id.encode('utf-8')).hexdigest()[:62]


def get_subject_address(att_subject_id):
    return NAMESPACE + SUBJECT_PREFIX + hashlib.sha512(
        att_subject_id.encode('utf-8')).hexdigest()[:62]


def get_professor_address(att_profess_id):
    return NAMESPACE + PROFESSOR_PREFIX + hashlib.sha512(
        att_profess_id.encode('utf-8')).hexdigest()[:62]


def get_student_address(att_student_id):
    return NAMESPACE + STUDENT_PREFIX + hashlib.sha512(
        att_student_id.encode('utf-8')).hexdigest()[:62]


def get_classroom_address(att_class_id):
    return NAMESPACE + CLASSROOM_PREFIX + hashlib.sha512(
        att_class_id.encode('utf-8')).hexdigest()[:62]


def get_staff_address(att_staff_id):
    return NAMESPACE + STAFF_PREFIX + hashlib.sha512(
        att_staff_id.encode('utf-8')).hexdigest()[:62]


def get_university_address(att_university_id):
    return NAMESPACE + UNIVERSITY_PREFIX + hashlib.sha512(
        att_university_id.encode('utf-8')).hexdigest()[:62]


def get_certificate_address(att_certi_id):
    return NAMESPACE + CERTIFICATE_PREFIX + hashlib.sha512(
        att_certi_id.encode('utf-8')).hexdigest()[:62]


def get_address_type(address):
    if address[:len(NAMESPACE)] != NAMESPACE:
        return AddressSpace.OTHER_FAMILY

    infix = address[6:8]

    if infix == '0':
        return AddressSpace.RESULT_PREFIX
    if infix == '0':
        return AddressSpace.SUBJECT_PREFIX
    if infix == '0':
        return AddressSpace.PROFESSOR_PREFIX
    if infix == '0':
        return AddressSpace.STUDENT_PREFIX
    if infix == '0':
        return AddressSpace.CLASSROOM_PREFIX
    if infix == '0':
        return AddressSpace.STAFF_PREFIX
    if infix == '0':
        return AddressSpace.UNIVERSITY_PREFIX
    if infix == '0':
        return AddressSpace.CERTIFICATE_PREFIX

    return AddressSpace.OTHER_FAMILY