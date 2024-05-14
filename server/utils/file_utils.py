import os, re, shutil, json

ALLOWED_LOGO_EXTENSIONS = {"svg", "jpg", "jpeg", "png", "gif"}
ALLOWED_COMPANY_FILE_EXTENSIONS = {"csv", "docx", "doc", "html", "json", "md", "pdf", "pptx", "ppt", "tex", "txt"}
CORRECTED_FILE_NAME = "CORRECTED_MESSAGES_{id}.csv"
CORRECTED_FILE_NAME_PATTERN = re.compile(r"CORRECTED_MESSAGES_\d+\.csv")
FILE_SIZE_LIMIT = 50*1024*1024 # 50 MB

def allowed_logo_extensions(logoname):
    return _allowed_file(logoname, ALLOWED_LOGO_EXTENSIONS)

def allowed_company_file_extensions(filename):
    return _allowed_file(filename, ALLOWED_COMPANY_FILE_EXTENSIONS.union(ALLOWED_LOGO_EXTENSIONS))
    
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

def save_corrected_messages(old_msg, new_msg, folder):
    # TODO in Tabelle umwandeln
    current_id = 0
    current_file = folder + CORRECTED_FILE_NAME.format(id = current_id)
    if os.path.isfile(folder + current_file):
        size = get_file_size(current_file)
        if size > FILE_SIZE_LIMIT:
            # current file nach id + 1 kopieren
            for filename in os.listdir(folder):
                if CORRECTED_FILE_NAME_PATTERN.match(filename):
                    current_id += 1
            shutil.copy(current_file, folder + CORRECTED_FILE_NAME.format(id = current_id))
    with open(folder + CORRECTED_FILE_NAME.format(id=0), "a", encoding="utf-8") as f:
        f.write(old_msg + ";" + new_msg)
