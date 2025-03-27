import hashlib
import os


def allowed_file(filename):
    """
    Checks if the format for the file received is acceptable. For this
    particular case, we must accept only image files. This is, files with
    extension ".png", ".jpg", ".jpeg" or ".gif".

    Parameters
    ----------
    filename : str
        Filename from werkzeug.datastructures.FileStorage file.

    Returns
    -------
    bool
        True if the file is an image, False otherwise.
    """
    allowed_extensions = {".png", ".jpg", ".jpeg", ".gif"}
    file_extension = os.path.splitext(filename)[1].lower()
    
    return file_extension in allowed_extensions


async def get_file_hash(file):
    """
    Returns a new filename based on the file content using MD5 hashing.
    It uses hashlib.md5() function from Python standard library to get
    the hash.

    Parameters
    ----------
    file : werkzeug.datastructures.FileStorage
        File sent by user.

    Returns
    -------
    str
        New filename based in md5 file hash.
    """
    # TODO: Implement the get_file_hash function
    # Current implementation will return the original file name.

    # Read file content and generate md5 hash (Check: https://docs.python.org/3/library/hashlib.html#hashlib.md5)
    hash_md5 = hashlib.md5()
    
    file_content = await file.read()
    hash_md5.update(file_content)

    # Return file pointer to the beginning
    file.seek(0)

    # Add original file extension
    _, file_extension = os.path.splitext(file.filename)

    # Generar el nuevo nombre con el hash
    return f"{hash_md5.hexdigest()}{file_extension.lower()}"
    
