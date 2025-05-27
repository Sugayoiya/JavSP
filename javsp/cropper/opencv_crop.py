import cv2
import numpy as np
from PIL import Image
from javsp.cropper.interface import Cropper, DefaultCropper
from javsp.cropper.utils import get_bound_box_by_face

class OpenCVCropper(Cropper):
    def __init__(self):
        # 初始化人脸检测器
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    def crop_specific(self, fanart: Image.Image, ratio: float) -> Image.Image:
        try:
            # 将 PIL 图像转换为 OpenCV 格式
            opencv_image = cv2.cvtColor(np.array(fanart), cv2.COLOR_RGB2BGR)
            gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
            
            # 检测人脸
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            
            if len(faces) > 0:
                # 选择最大的人脸
                largest_face = max(faces, key=lambda face: face[2] * face[3])
                x, y, w, h = largest_face
                
                # 转换为 (x, y, w, h) 格式，与 slimeface 兼容
                face = (x, y, w, h)
                poster_box = get_bound_box_by_face(face, fanart.size, ratio)
                return fanart.crop(poster_box)
            else:
                # 如果没有检测到人脸，使用默认裁剪
                return DefaultCropper().crop_specific(fanart, ratio)
        except Exception as e:
            # 如果出现任何错误，使用默认裁剪
            return DefaultCropper().crop_specific(fanart, ratio)

if __name__ == '__main__':
    from argparse import ArgumentParser

    arg_parser = ArgumentParser(prog='opencv crop')
    arg_parser.add_argument('-i', '--image', help='path to image to detect')
    args, _ = arg_parser.parse_known_args()

    if args.image is None:
        print("USAGE: opencv_crop.py -i/--image [path]")
        exit(1)

    input_image = Image.open(args.image)
    cropper = OpenCVCropper()
    result = cropper.crop(input_image)
    result.save('output.png') 