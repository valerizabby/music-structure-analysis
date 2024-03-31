def read_file_as_string(filename):
    with open(filename, 'r') as f:
        html_string = f.read()
    return html_string
