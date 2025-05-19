import os
import base64

def get_project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_image_path(relative_path):
    return os.path.join(get_project_root(), relative_path)


def get_image_base64(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")
