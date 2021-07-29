from PIL import Image
import PIL
PIL.Image.MAX_IMAGE_PIXELS = 9000000000
import argparse
import os
import glob
parser = argparse.ArgumentParser(description='Png2Tiff convertor',formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('--input-dir', type=str, help='the dataset input path')
parser.add_argument('--output-dir', type=str,help='sequence length for training')

args = parser.parse_args()

jpg_path = os.path.join(args.input_dir,"*.png")


for i in glob.glob(jpg_path):
	im = Image.open(i)
	try:
		tiff_name_0 = i.split("/")[-1].split(".")[:-1]
		tiff_name_1 = tiff_name_0[-2]+"."+tiff_name_0[-1]
		tiff_path = os.path.join(args.output_path,tiff_name_1+".tiff") 
		print(tiff_path)
		im.save(tiff_path)
	except:
		tiff_name_1 = i.split("/")[-1].split(".")[-2]
		tiff_path = os.path.join(args.output_dir,tiff_name_1+".tiff") 
		print(tiff_path)
		im.save(tiff_path)
