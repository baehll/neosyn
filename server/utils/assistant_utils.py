import os
def GPTConfig():
    from server import GPTConfig
    return GPTConfig

def upload_files_to_openai(upload_folder, filenames):
    file_ids = []
    for file in filenames:
        file_ids.append(GPTConfig().CLIENT.files.create(
            file=open(os.path.join(upload_folder, file),"rb"),
            purpose="assistants"            
        ).id)
    return file_ids
    
def init_vector_storage(vector_store_name, file_ids):
    return GPTConfig().CLIENT.beta.vector_stores.create(
        name=vector_store_name,
        file_ids=file_ids
    )

def init_assistant(upload_folder, filenames, orga):
    if orga.vec_storage_id != "":
        deleted_store = GPTConfig().CLIENT.beta.vector_stores.delete(vector_store_id=orga.vec_storage_id)    
    
    # dateien hochladen 
    file_ids = upload_files_to_openai(os.path.join(upload_folder, orga.folder_path), filenames)
    vec_storage = init_vector_storage(orga.folder_path + "_VECTOR_STORE", file_ids)
    # neuen assistant erstellen
    assistant = GPTConfig().CLIENT.beta.assistants.create(
        name="",
        instructions="",
        model=GPTConfig().GPT_MODEL,
        tools=[{"type":"file_search"}],
        tool_resources={
            "file_search": {
                "vector_store_ids": [vec_storage.id]
            }
        }
    )
    # assistant mit vector storage verknüpfen
    orga.assistant_id = assistant.id
    orga.vec_storage_id = vec_storage.id
    

def generate_response_from_assistant(assistant_id):
    pass
