import glob
import argparse
import os

parser = argparse.ArgumentParser(description='Png Counter',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--input-path', type=str, help='the dataset input path')
args = parser.parse_args()

png_path = os.path.join(args.input_path,"*.png") #"/media/bou02/6TB_3/"
cntr=0
for i in glob.glob(png_path):
	cntr+=1
	print(cntr)
