ALLOWED_EXTENSIONS = ['xlsx']

def retrieve_extension(filename=None):
    if filename is None:
        print(f"ERROR: File object does not have a filename")
        return None

    if not isinstance(filename, str):
        print(f"ERROR: File object does not have a string as filename")
        return None

    exte = '.' in filename and filename.rsplit('.', 1)[1].lower()
    return exte.strip().lower()