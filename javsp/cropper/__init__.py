from javsp.config import SlimefaceEngine, OpenCVEngine
from javsp.cropper.interface import Cropper, DefaultCropper
from javsp.cropper.slimeface_crop import SlimefaceCropper
from javsp.cropper.opencv_crop import OpenCVCropper

def get_cropper(engine: SlimefaceEngine | OpenCVEngine | None) -> Cropper:
    if engine is None:
        return DefaultCropper()
    if engine.name == 'slimeface':
        return SlimefaceCropper()
    if engine.name == 'opencv':
        return OpenCVCropper()
