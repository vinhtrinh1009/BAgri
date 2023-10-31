import enum
import hashlib


FAMILY_NAME = 'BCERTQUYEN-45C4D'
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


def get_result_address(result_id):
    return NAMESPACE + RESULT_PREFIX + hashlib.sha512(
        result_id.encode('utf-8')).hexdigest()[:62]


def get_subject_address(subject_id):
    return NAMESPACE + SUBJECT_PREFIX + hashlib.sha512(
        subject_id.encode('utf-8')).hexdigest()[:62]


def get_professor_address(profess_id):
    return NAMESPACE + PROFESSOR_PREFIX + hashlib.sha512(
        profess_id.encode('utf-8')).hexdigest()[:62]


def get_student_address(student_id):
    return NAMESPACE + STUDENT_PREFIX + hashlib.sha512(
        student_id.encode('utf-8')).hexdigest()[:62]


def get_classroom_address(class_id):
    return NAMESPACE + CLASSROOM_PREFIX + hashlib.sha512(
        class_id.encode('utf-8')).hexdigest()[:62]


def get_staff_address(staff_id):
    return NAMESPACE + STAFF_PREFIX + hashlib.sha512(
        staff_id.encode('utf-8')).hexdigest()[:62]


def get_university_address(university_id):
    return NAMESPACE + UNIVERSITY_PREFIX + hashlib.sha512(
        university_id.encode('utf-8')).hexdigest()[:62]


def get_certificate_address(certi_id):
    return NAMESPACE + CERTIFICATE_PREFIX + hashlib.sha512(
        certi_id.encode('utf-8')).hexdigest()[:62]


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