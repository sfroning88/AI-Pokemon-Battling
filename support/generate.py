def generate_code(filename=None):
    if filename is None:
        print(f"ERROR: File object does not have a filename")
        return None

    if not isinstance(filename, str):
        print(f"ERROR: File object does not have a string as filename")
        return None
    
    return str(abs(hash(filename)) % 1000000).zfill(6)