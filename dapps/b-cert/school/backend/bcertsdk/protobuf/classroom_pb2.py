# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protobuf/classroom.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='protobuf/classroom.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x18protobuf/classroom.proto\"\xbf\x01\n\tClassroom\x12\x11\n\ttimestamp\x18\x01 \x01(\x04\x12\x14\n\x0c\x61tt_class_id\x18\x02 \x01(\t\x12\x14\n\x0c\x61tt_semester\x18\x03 \x01(\t\x12\x12\n\natt_status\x18\x04 \x01(\t\x12\x1e\n\x16\x66or_subject_subject_id\x18\x05 \x01(\t\x12 \n\x18\x66or_professor_profess_id\x18\x06 \x01(\t\x12\x1d\n\x15\x66or_result_result_ids\x18\x07 \x03(\t\"1\n\x12\x43lassroomContainer\x12\x1b\n\x07\x65ntries\x18\x01 \x03(\x0b\x32\n.Classroomb\x06proto3')
)




_CLASSROOM = _descriptor.Descriptor(
  name='Classroom',
  full_name='Classroom',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='timestamp', full_name='Classroom.timestamp', index=0,
      number=1, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='att_class_id', full_name='Classroom.att_class_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='att_semester', full_name='Classroom.att_semester', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='att_status', full_name='Classroom.att_status', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='for_subject_subject_id', full_name='Classroom.for_subject_subject_id', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='for_professor_profess_id', full_name='Classroom.for_professor_profess_id', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='for_result_result_ids', full_name='Classroom.for_result_result_ids', index=6,
      number=7, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=29,
  serialized_end=220,
)


_CLASSROOMCONTAINER = _descriptor.Descriptor(
  name='ClassroomContainer',
  full_name='ClassroomContainer',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='entries', full_name='ClassroomContainer.entries', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=222,
  serialized_end=271,
)

_CLASSROOMCONTAINER.fields_by_name['entries'].message_type = _CLASSROOM
DESCRIPTOR.message_types_by_name['Classroom'] = _CLASSROOM
DESCRIPTOR.message_types_by_name['ClassroomContainer'] = _CLASSROOMCONTAINER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Classroom = _reflection.GeneratedProtocolMessageType('Classroom', (_message.Message,), {
  'DESCRIPTOR' : _CLASSROOM,
  '__module__' : 'protobuf.classroom_pb2'
  # @@protoc_insertion_point(class_scope:Classroom)
  })
_sym_db.RegisterMessage(Classroom)

ClassroomContainer = _reflection.GeneratedProtocolMessageType('ClassroomContainer', (_message.Message,), {
  'DESCRIPTOR' : _CLASSROOMCONTAINER,
  '__module__' : 'protobuf.classroom_pb2'
  # @@protoc_insertion_point(class_scope:ClassroomContainer)
  })
_sym_db.RegisterMessage(ClassroomContainer)


# @@protoc_insertion_point(module_scope)