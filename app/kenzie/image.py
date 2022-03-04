from http import HTTPStatus
from flask import request, send_from_directory
import os
from werkzeug.datastructures import FileStorage

FILES_DIRECTORY = os.getenv("FILES_DIRECTORY")
MAX_CONTENT_LENGTH = os.getenv("MAX_CONTENT_LENGTH")
ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS")


def func_upload_product():

    arquivo= request.files["file_name"]
    new_type_file = str(arquivo.filename).split('.')[-1]
    type_files = os.listdir(f"{FILES_DIRECTORY}")

    if not new_type_file in type_files:
        return {"message": "Esse tipo de arquivo não é suportado"}, 415
    
    elif arquivo.filename in os.listdir(f"{FILES_DIRECTORY}/{new_type_file}"):
        return {"message": "Esse arquivo já existe, carregue outra imagem"}, 409
  
    elif new_type_file in type_files:
         arquivo.save(f"{FILES_DIRECTORY}/{new_type_file}/{arquivo.filename}")
         return {"message":"Arquivo salvo"}, 201
    
    else :
        return {"Error": "Algo deu errado, revise seu dados ou tente novamente mais tarde"}



def func_get_extension_files(file_name):

    type_files = os.listdir(f"{FILES_DIRECTORY}")

    if not file_name in type_files:
          return  {"Error": f"O formato '{file_name}' não é suportado. Por favor, tente outro"}, 415

    files =os.listdir(f'{FILES_DIRECTORY}/{file_name}')
    return {"data": files}
  

def func_get_all():

    type_files = os.listdir(f'{FILES_DIRECTORY}')
    
    archives = list()
    for paste in type_files:
        paste_of_images = os.listdir(f'{FILES_DIRECTORY}/{paste}') 
        for image in paste_of_images:
            archives.append(image)
      
    return {"data": archives}, 200
    


def func_download_file(file_name):
    type_files = os.listdir(f"{FILES_DIRECTORY}")
    archive_type = str(file_name).split('.')[-1]

    if archive_type in type_files and file_name in os.listdir(f"{FILES_DIRECTORY}/{archive_type}"):
        return send_from_directory(
            directory=f"{FILES_DIRECTORY}/{archive_type}",
            path=file_name, 
            as_attachment=True), 200

    return {"message": "Esse arquivo não existe na base de dados"}
   
def func_download_zip_file(nome, compress):
    return {"message":"we are testing"}
