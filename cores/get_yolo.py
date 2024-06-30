from ultralytics import YOLOv10

import os
import shutil
import glob

DATA_PATH = r"data/358131089_1598284357678845_8367029803511623159_n.jpg"
FOLDER_PATH = "data/"

CONF_THRESHOLD = 0.5
IMG_SIZE = 640


SAVE_FOLDER = "save/"

model = YOLOv10("./models/best.pt")


if os.path.exists(SAVE_FOLDER):
    shutil.rmtree(SAVE_FOLDER)

os.mkdir(SAVE_FOLDER)


def scan(img_path, is_save=True):
    """
        return result {

            "Person": [[boundingBox1],[boundingBox2],[boundingBox3]]  ,
            ...
        }
    """
    results = model(source=img_path,
                    save=False,
                    conf=CONF_THRESHOLD)

    result_dict = {}

    for i in results[0].boxes:
        class_name = categorycal[int(i.cls)]

        if result_dict.get(class_name) == None:
            result_dict[class_name] = []

        result_dict.get(class_name).append(list(i.xywh.to("cpu")[0].numpy()))
    if is_save:
        results[0].save(f"{SAVE_FOLDER}temp.jpg")

    return result_dict


def scan_folder():
    """
        return result {

            "Person": [[boundingBox1],[boundingBox2],[boundingBox3]]  ,
            ...
        }
        if you want to statistics class name and counting Person -> len(result["Person"])
    """
    results = {}
    for path in glob.glob(F"{FOLDER_PATH}/*.jpg"):
        results.update(scan(path))

    return results


categorycal = model.names

if __name__ == "__main__":

    model.to("cuda")
    results = model(source=DATA_PATH,
                    save=True,
                    conf=CONF_THRESHOLD)

    result_dict = {}

    for i in results[0].boxes:

        class_name = categorycal[int(i.cls)]
        print(F'Class name: {categorycal[int(i.cls)]}')
        print(i.xywh.to("cpu")[0])
        if result_dict.get(class_name) == None:
            result_dict[class_name] = []

        result_dict.get(class_name).append(
            list(i.xywh.to("cpu")[0].numpy()))

        print('a')

    results[0].save(f"{SAVE_FOLDER}{os.path.basename(DATA_PATH)}")
    print("pause")
