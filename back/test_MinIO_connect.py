# file_uploader.py MinIO Python SDK example
from minio import Minio
from minio.error import S3Error


client = Minio("play.min.io",
        access_key="Q3AM3UQ867SPQQA43P2F",
        secret_key="zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG",
    )

found = client.bucket_exists("tmp")
if not found:
        client.make_bucket("tmp")


def getTempMinIO(sesFileName):
    try:
        return client.fget_object("tmp", sesFileName, sesFileName)
    except:
        return False

def setTempMinIO(sesFileName, sourceFile):
    
    try: 
        client.fput_object(
            "tmp", sesFileName, sourceFile,
        )
        return True
    except:
        return False

def delTempMinIO(sesFileName):
    client.remove_object("tmp", sesFileName)

