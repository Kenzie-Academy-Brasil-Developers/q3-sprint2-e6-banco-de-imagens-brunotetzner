from unittest.util import _MAX_LENGTH
from flask import Flask, request
from .kenzie import (
    func_upload_product, 
    func_get_extension_files, 
    func_get_all,func_download_file,
    func_download_zip_file)
import os


app = Flask(__name__)

FILES_DIRECTORY = os.getenv("FILES_DIRECTORY")
MAX_CONTENT_LENGTH = os.getenv("MAX_CONTENT_LENGTH")
ALLOWED_EXTENSIONS = os.getenv("ALLOWED_EXTENSIONS")

app.config['MAX_CONTENT_LENGTH'] = int(MAX_CONTENT_LENGTH)

if not os.path.isdir(FILES_DIRECTORY):
    os.mkdir(FILES_DIRECTORY)
    for item in ALLOWED_EXTENSIONS.split(" "):
        os.system(f"mkdir {FILES_DIRECTORY}/{item}")

@app.post("/upload")
def upload_file():
    
    return func_upload_product()
    

@app.get("/files")
def get_all_files():
 return func_get_all()


@app.get("/files/<extension>")
def get_files_with_that_extension(extension):
    return func_get_extension_files(extension)


@app.get("/download/<file_name>")
def dowload_files(file_name):
    return func_download_file(file_name)


@app.get("/download-zip/query_params")
def dowload_zip_file():
    return func_download_zip_file()
