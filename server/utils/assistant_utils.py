import os, csv
from io import BytesIO
from ..db.models import db

def GPTConfig():
    from server import GPTConfig
    return GPTConfig

def upload_csv_lines_to_openai(filename, lines, vec_storage_id):
    output = BytesIO()
    csv_data = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
    csv_data.writerows(lines)
    file_id = GPTConfig().CLIENT.files.create(
        file=(filename + ".csv", output.getvalue),
        purpose="assistants"
    )
    
    GPTConfig().CLIENT.beta.vector_stores.files.create_and_poll(
        vector_store_id=vec_storage_id,
        file_id=file_id
    )

def upload_files_to_openai(file_blobs):
    file_ids = []
    for file in file_blobs:
        file_ids.append(GPTConfig().CLIENT.files.create(
            file=(file.filename, BytesIO(file.data)),
            purpose="assistants"            
        ).id)
    return file_ids
    
def init_vector_storage(vector_store_name, file_ids):
    if file_ids is None:
        return GPTConfig().CLIENT.beta.vector_stores.create(
            name=vector_store_name
        )
    else:
        return GPTConfig().CLIENT.beta.vector_stores.create(
            name=vector_store_name,
            file_ids=file_ids
        )

def init_assistant(orga):
    if orga.vec_storage_id is not None:
        deleted_store = GPTConfig().CLIENT.beta.vector_stores.delete(vector_store_id=orga.vec_storage_id) 
           
    # dateien hochladen 
    orga_files = list(orga.files)
    # print(orga_files)
    # print(orga.logo())
    if len(orga_files) > 0:
        if orga.logo_id is not None:
            orga_files.remove(orga.logo())
        
    if len(orga_files) != 0:
        file_ids = upload_files_to_openai(orga_files)
        vec_storage = init_vector_storage(orga.name + "_VECTOR_STORE", file_ids)
    else:
        vec_storage = init_vector_storage(orga.name + "_VECTOR_STORE", None)
        
    # neuen Thread erstellen
    thread = GPTConfig().CLIENT.beta.threads.create(
        tool_resources={
            "file_search": {
                "vector_store_ids": [vec_storage.id]
            }
        }
    )
    # assistant mit vector storage verknüpfen
    orga.vec_storage_id = vec_storage.id
    db.session.add(orga)
    db.session.commit()