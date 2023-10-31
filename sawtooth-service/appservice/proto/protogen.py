from glob import glob
import os
import re
import tempfile

from grpc.tools.protoc import main as _protoc
from config.logging_config import get_logger

_LOGGER = get_logger(__name__)


def make_protobuf(path, pkg_name, top_dir, src_dir):
    out_dir = os.path.join(top_dir, path, pkg_name)
    os.makedirs(out_dir, exist_ok=True)

    init_py = os.path.join(out_dir, "__init__.py")

    if not os.path.exists(init_py):
        with open(init_py, mode="w"):
            pass

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_pkg_dir = os.path.join(tmp_dir, pkg_name)
        os.makedirs(tmp_pkg_dir)

        cwd = os.getcwd()
        os.chdir(src_dir)
        proto_files = glob("*.proto")
        os.chdir(cwd)
        for proto in proto_files:
            src = os.path.join(src_dir, proto)
            dst = os.path.join(tmp_pkg_dir, proto)
            with open(src, encoding="utf-8") as fin:
                with open(dst, "w", encoding="utf-8") as fout:
                    src_contents = fin.read()
                    fixed_contents = fix_import(src_contents, pkg_name)
                    fout.write(fixed_contents)

        _protoc(
            [
                __file__,
                "-I=%s" % tmp_dir,
                "--python_out=%s" % os.path.join(top_dir, path),
            ]
            + glob("%s/*.proto" % tmp_pkg_dir)
        )
        _LOGGER.debug("Generated protobuf file: {}".format(out_dir))


def fix_import(contents, pkg, sub_dir=False):
    pattern = r'^import "(.*)\.proto\"'
    if sub_dir:
        template = r'import "%s/\1_pb2/\1.proto"'
    else:
        template = r'import "%s/\1.proto"'

    return re.sub(
        pattern,
        lambda match: match.expand(template) % pkg,
        contents,
        flags=re.MULTILINE,
    )
