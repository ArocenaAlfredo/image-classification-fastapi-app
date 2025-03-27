import os
from typing import List

from app import db
from app import settings as config
from app import utils
from app.auth.jwt import get_current_user
from app.model.schema import PredictRequest, PredictResponse
from app.model.services import model_predict
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

router = APIRouter(tags=["Model"], prefix="/model")


@router.post("/predict")
async def predict(file: UploadFile, current_user=Depends(get_current_user)):
    rpse = {"success": False, "prediction": None, "score": None, "image_file_name": None}
    # To correctly implement this endpoint you should:
    #   1. Check a file was sent and that file is an image, see `allowed_file()` from `utils.py`.
    #   2. Store the image to disk, calculate hash (see `get_file_hash()` from `utils.py`) before
    #      to avoid re-writing an image already uploaded.
    #   3. Send the file to be processed by the `model` service, see `model_predict()` from `services.py`.
    #   4. Update and return `rpse` dict with the corresponding values
    # If user sends an invalid request (e.g. no file provided) this endpoint
    # should return `rpse` dict with default values HTTP 400 Bad Request code
    # TODO
    # 1. Verificar si se envió un archivo y si es una imagen
    if not file or not utils.allowed_file(file.filename):
        raise HTTPException(status_code=400, detail="File type is not supported.")

    # 2. Obtener el hash del archivo para evitar duplicados
    file_hash = await utils.get_file_hash(file)
    file_path = os.path.join(config.UPLOAD_FOLDER, file_hash)

    # Guardar la imagen en el servidor
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # 3. Enviar la imagen al servicio de ML y obtener la predicción
    prediction, score = await model_predict(file_hash)

    # 4. Verificar si la predicción fue exitosa y actualizar la respuesta
    if prediction is None or score is None:
        raise HTTPException(status_code=400, detail="File type is not supported.")
    rpse["success"] = True
    rpse["prediction"] = prediction
    rpse["score"] = score
    rpse["image_file_name"] = file_hash

    return PredictResponse(**rpse)
