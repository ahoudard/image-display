import argparse
import os
from imcovi.gui.image_display import ImageAPI

parser = argparse.ArgumentParser()
parser.add_argument('images_folder', help='path to the folder containing the images to compare')
args = parser.parse_args()

if __name__ == "__main__":

    images_list = [f for f in os.listdir(args.images_folder) if f.endswith('.png')]
    API = ImageAPI(args.images_folder,images_list)
    API.mainloop()