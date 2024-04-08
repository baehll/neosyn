ALLOWED_LOGO_EXTENSIONS = {"svg", "jpg", "jpeg", "png", "gif"}
ALLOWED_COMPANY_FILE_EXTENSIONS = {"csv", "docx", "doc", "html", "json", "md", "pdf", "pptx", "ppt", "tex", "txt"}

def allowed_logo_extensions(logoname):
    return _allowed_file(logoname, ALLOWED_LOGO_EXTENSIONS)

def allowed_company_file_extensions(filename):
    return _allowed_file(filename, ALLOWED_COMPANY_FILE_EXTENSIONS)
    
def _allowed_file(filename, extensions):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in extensions

def get_file_size(fobj):
    if fobj.content_length:
        return fobj.content_length
    
    try:
        pos = fobj.tell()
        fobj.seek(0, 2)
        size = fobj.tell()
        fobj.seek(pos)
        return size
    except (AttributeError, IOError):
        pass
    
    return 0