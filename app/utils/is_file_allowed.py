ALLOWED_EXTENSIONS = {'midi', 'mid', 'png', 'jpg', 'jpeg', 'gif'}


def is_file_allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
