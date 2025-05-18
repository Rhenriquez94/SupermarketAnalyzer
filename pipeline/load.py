from datetime import datetime
import os
from pipeline.save_s3 import upload_file_to_s3

def save_to_csv(df, carpeta, bucket_name=None):
    ruta = f"data/{carpeta}"
    os.makedirs(ruta, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"{carpeta}_{timestamp}.csv"
    full_path = f"{ruta}/{filename}"

    # Guardar localmente
    df.to_csv(full_path, index=False)
    print(f"Archivo CSV guardado localmente como: {full_path}")

    # Subir a S3 si se proporciona un bucket
    if bucket_name:
        upload_file_to_s3(full_path, bucket_name, filename)
