from exif import Image as ExifImage
from PIL import Image, ImageFilter
from pillow_heif import HeifImagePlugin
import piexif

def getExif(file_bytes):
    # with open(path, "rb") as img_file:
    exif_image = ExifImage(file_bytes)
    if not exif_image.has_exif:
        return ""
    res = exif_image.get_all()
    
    # Обработка данных вспышки, если они есть
    if "flash" in res:
        res["flash"] = {
            "flash_fired": bool(res["flash"].flash_fired),
            "flash_return": str(res["flash"].flash_return),
            "flash_mode": str(res["flash"].flash_mode),
            "flash_function_not_present": bool(res["flash"].flash_function_not_present),
            "red_eye_reduction_supported": bool(res["flash"].red_eye_reduction_supported),
            "reserved": int(res["flash"].reserved)
        }

    return res


def checkHEIC(path="./test_image_files/2.HEIC"):
    heic_image = Image.open(path)
    # print((heic_image.info["exif"]))
    exif_data = heic_image.info.get("exif")
    decoded_exif = piexif.load(exif_data)

    # Пример: печать всех метаданных в читаемом формате
    for ifd, tags in decoded_exif.items():
        print(f"IFD: {ifd}")
        for tag, value in tags.items():
            tag_name = piexif.TAGS[ifd].get(tag, {"name": "Unknown"})["name"]
            print(f"    {tag_name}: {value}")
    
    return decoded_exif


# print("---------------------------------------------------------------------------------------------------------------------------------------")
# print("HEIC")
# print("---------------------------------------------------------------------------------------------------------------------------------------")
# checkHEIC()
