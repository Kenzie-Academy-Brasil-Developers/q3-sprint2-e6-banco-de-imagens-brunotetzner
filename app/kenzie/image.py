from flask import request, send_from_directory
import os
import zipfile

FILES_DIRECTORY = os.getenv("FILES_DIRECTORY")


if "type_files" in os.listdir('/tmp'):
    type_files = os.listdir(f"{FILES_DIRECTORY}")


def func_upload_product():

    arquivo= request.files["file_name"]
    new_type_file = str(arquivo.filename).split('.')[-1]

    if not new_type_file in type_files:
        return {"message": "Esse tipo de arquivo não é suportado"}, 415
    
    elif arquivo.filename in os.listdir(f"{FILES_DIRECTORY}/{new_type_file}"):
        return {"message": "Esse arquivo já existe, carregue outra imagem"}, 409
  
    elif new_type_file in type_files:
         arquivo.save(f"{FILES_DIRECTORY}/{new_type_file}/{arquivo.filename}")
         return {"message":"Arquivo salvo"}, 201
    
    else :
        return {"Error": "Algo deu errado, revise seu dados ou tente novamente mais tarde"},400




def func_get_extension_files(file_name):
    if not file_name in type_files:
          return  {"Error": f"O formato '{file_name}' não é suportado. Por favor, tente outro"}, 415

    files =os.listdir(f'{FILES_DIRECTORY}/{file_name}')
    return {"data": files}
  



def func_get_all():
    
    archives = list()
    for paste in type_files:
        paste_of_images = os.listdir(f'{FILES_DIRECTORY}/{paste}') 
        for image in paste_of_images:
            archives.append(image)
      
    return {"data": archives}, 200
    



def func_download_file(file_name):

    archive_type = str(file_name).split('.')[-1]

    if archive_type in type_files and file_name in os.listdir(f"{FILES_DIRECTORY}/{archive_type}"):
        return send_from_directory(
            directory=f"{FILES_DIRECTORY}/{archive_type}",
            path=file_name, 
            as_attachment=True), 200

    return {"message": f"Esse arquivo não existe na base de dados. Isso provavelmente significa que o formato '{archive_type}' é inválido."}, 404
   


def func_download_zip_file():
  
  file_extension = request.args.get('file_type')
  comprehension_rate = int(request.args.get("compress_tax"))

  if comprehension_rate > 9 or comprehension_rate<0:
      return {'message': f"A Taxa de compressão com valor {comprehension_rate} é inválida. Informe um valor entre 0 e 9"}, 404

  if file_extension in os.listdir(FILES_DIRECTORY):
    list_archives = os.listdir(f"{FILES_DIRECTORY}/{file_extension}")
    new_directory_zip = f'{file_extension}.zip'
    z = zipfile.ZipFile(f'{FILES_DIRECTORY}/{new_directory_zip}', 'w', zipfile.ZIP_DEFLATED, compresslevel=comprehension_rate)

    for image in list_archives:
      z.write((f'{FILES_DIRECTORY}/{file_extension}/{image}'))
    z.close()  

    return send_from_directory(
        directory =FILES_DIRECTORY,
        path=new_directory_zip,
        as_attachment=True
    )

  else: return{"Message": f"A extensão '{file_extension}' não existe"}, 404
