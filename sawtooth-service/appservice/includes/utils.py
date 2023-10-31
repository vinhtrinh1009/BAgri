from json.decoder import JSONDecodeError

def gen_file(data, dst, template):
    file = open(dst, "w")
    output = template.render(data=data)
    file.write(output)
    file.close()