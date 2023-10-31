from logging import Logger
import os

from jinja2 import Environment, FileSystemLoader

from constants import BASE_DIR
from includes import utils
from proto.protogen import make_protobuf
from config.logging_config import get_logger

_LOGGER = get_logger(__name__)


def gen_code(data, dst_folder):

    # create foler
    proto_folder = os.path.join(
                BASE_DIR,
                f"{dst_folder}/{data['basic_info']['dapp_name']}/protos/")

    if not os.path.exists(proto_folder):
        os.makedirs(proto_folder)

    file_loader = FileSystemLoader(os.path.join(BASE_DIR, 'templates/protos'))
    env = Environment(loader=file_loader, autoescape=True)
    env.trim_blocks = True
    env.lstrip_blocks = True
    env.rstrip_blocks = True

    # for entity in data['entities']:
    #     destination_file = f'{proto_folder}/{entity["name"]}.proto'
    #     entity_template = env.get_template('entity_template.jinja2')
    #     utils.gen_file(data=entity, dst=destination_file, template=entity_template)

    for entity in data['protobufs']:
        destination_file = f'{proto_folder}/{entity["name"]}.proto'
        entity_template = env.get_template('entity_template.jinja2')
        utils.gen_file(data=entity, dst=destination_file, template=entity_template)
    
    payload_destination_file = f'{proto_folder}/payload.proto'
    payload_template = env.get_template('payload_template.jinja2')
    utils.gen_file(data=data['functions'], dst=payload_destination_file, template=payload_template)
    #
    # # Generate user proto
    # validator_destination_file = f'{proto_folder}/validator.proto'
    # validator_template = env.get_template('validator_template.jinja2')
    # utils.gen_file(data=data, dst=validator_destination_file, template=validator_template)
    #
    # # Generate user proto
    # transaction_destination_file = f'{proto_folder}/transaction.proto'
    # transaction_template = env.get_template('transaction_template.jinja2')
    # utils.gen_file(data=data, dst=transaction_destination_file, template=transaction_template)
    #
    # # Generate user proto
    # client_batch_submit_destination_file = f'{proto_folder}/client_batch_submit.proto'
    # client_batch_submit_template = env.get_template('client_batch_submit_template.jinja2')
    # utils.gen_file(data=data, dst=client_batch_submit_destination_file, template=client_batch_submit_template)
    #
    # # Generate user proto
    # batch_destination_file = f'{proto_folder}/batch.proto'
    # batch_template = env.get_template('batch_template.jinja2')
    # utils.gen_file(data=data, dst=batch_destination_file, template=batch_template)
    
    # payload = proto_folder + "payload.proto"
    # record = proto_folder + "record" + ".proto"

    # payload_template = env.get_template("payload_template.jinja2")
    # record_template = env.get_template("record_proto_template.jinja2")

    # utils.GenFile(data=data, dst=record, template=record_template)

    # Generate payload proto
    # utils.GenFile(data=data, dst=payload, template=payload_template)

    top_dir = os.path.join(
        BASE_DIR, "{0}/{1}/".format(dst_folder, data['basic_info']['dapp_name'])
    )
    _LOGGER.debug(top_dir)
    make_protobuf(
        data['basic_info']['dapp_name'] + 'sdk',
        'protobuf',
        top_dir,
        proto_folder,
    )
    make_protobuf(
        data['basic_info']['dapp_name'] + 'processor',
        'protobuf',
        top_dir,
        proto_folder,
    )
    # cmd = "rm -rf " + proto_folder
    # os.system(cmd)
