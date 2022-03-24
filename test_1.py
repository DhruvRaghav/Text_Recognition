# coding: utf-8
import tr
import sys, cv2, time, os
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import shutil
import os
import io

_BASEDIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(_BASEDIR)

directory1 = "Garbage"
directory2 = "Text_Image"
# Parent Directory path
parent_dir = "/mnt/vol2/Dhruv_Raghav/tr-master"

# Path
path1 = os.path.join(parent_dir, directory1)
path2 = os.path.join(parent_dir, directory2)
print("garbage",path1)
print("text_folder",path2)

'''---------------------------------------------------------------------------------------'''

try:

    os.makedirs(path1, exist_ok=True)
    os.makedirs(path2, exist_ok=True)

    print("Directory '%s' created successfully" % directory1)
    print("Directory '%s' created successfully" % directory2)
except OSError as error:
    print("Directory '%s' can not be created" % directory1)
    print("Directory '%s' can not be created" % directory2)


def test(File_path):
    for j in os.listdir(File_path):

        print("filename", j)

        try:
            # print("recognize", tr.recognize("/home/ceinfo/Desktop/LCOM54510122021073400 (1).jpg"))

            # img_path = "/mnt/vol2/Dhruv_Raghav/text_detection/Text_Results/LCOM60801042021082608.jpg"
            img_path = f'{File_path}/' + j
            print("image_path", img_path)

            img_pil = Image.open(img_path)
            try:
                if hasattr(img_pil, '_getexif'):
                    # from PIL import ExifTags
                    # for orientation in ExifTags.TAGS.keys():
                    #     if ExifTags.TAGS[orientation] == 'Orientation':
                    #         break
                    orientation = 274
                    exif = dict(img_pil._getexif().items())
                    if exif[orientation] == 3:
                        img_pil = img_pil.rotate(180, expand=True)
                    elif exif[orientation] == 6:
                        img_pil = img_pil.rotate(270, expand=True)
                    elif exif[orientation] == 8:
                        img_pil = img_pil.rotate(90, expand=True)
            except:
                pass

            MAX_SIZE = 1600
            if img_pil.height > MAX_SIZE or img_pil.width > MAX_SIZE:
                scale = max(img_pil.height / MAX_SIZE, img_pil.width / MAX_SIZE)

                new_width = int(img_pil.width / scale + 0.5)
                new_height = int(img_pil.height / scale + 0.5)
                img_pil = img_pil.resize((new_width, new_height), Image.ANTIALIAS)

            color_pil = img_pil.convert("RGB")
            gray_pil = img_pil.convert("L")

            img_draw = ImageDraw.Draw(color_pil)
            colors = ['red', 'green', 'blue', "purple"]

            t = time.time()
            n = 1
            for _ in range(n):
                tr.detect(gray_pil, flag=tr.FLAG_RECT)
            # print("time", (time.time() - t) / n)

            results = tr.run(gray_pil, flag=tr.FLAG_ROTATED_RECT)
            #print(results)

            for i, rect in enumerate(results):
                cx, cy, w, h, a = tuple(rect[0])
                print(i, "\t", rect[1], rect[2])
                box = cv2.boxPoints(((cx, cy), (w, h), a))
                box = np.int0(np.round(box))

                for p1, p2 in [(0, 1), (1, 2), (2, 3), (3, 0)]:
                    img_draw.line(xy=(box[p1][0], box[p1][1], box[p2][0], box[p2][1]), fill=colors[i % len(colors)],
                                  width=2)

            # color_pil.show()


            if len(results) > 1:
                # print("length",len(results))
                target = '/mnt/vol2/Dhruv_Raghav/tr-master/Text_Image/'+j
                shutil.copyfile(img_path, target)
                #cv2.imwrite("/mnt/vol2/Dhruv_Raghav/tr-master/Text_Image", img_pil)

            else:
                garbage = '/mnt/vol2/Dhruv_Raghav/tr-master/Garbage/'+j
                shutil.copyfile(img_path, garbage)
        except:
            pass


if __name__ == "__main__":

    test("/mnt/vol2/Dhruv_Raghav/text_detection/L")
