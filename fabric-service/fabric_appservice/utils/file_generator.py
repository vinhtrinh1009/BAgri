import os


def gen_file(data, dst, template, **kwargs):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    file = open(dst, "w")
    output = template.render(data=data, **kwargs)
    file.write(output)
    file.close()
