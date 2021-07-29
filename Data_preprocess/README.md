# AI-FFPE Data Process

For the dataset processing steps build the environment by running:

```bash
sudo apt-get install openslide-tools
conda env create -n AIFFPE_preprocess -f requirements.yaml
conda activate AIFFPE_preprocess
```

#### Create Patches

 One can start to create patches in .h5 format by following commend:

```bash
python create_patches.py --source DIR_TO_WSI --save-dir DIR_TO_PATCHES
```

#### Create Patches in the format that is Processable by AI-FFPE Networks

Convert ".h5" formatted paatches into ".png" :

```bash
python h52png.py  --dataset-dir DIR_TO_TEST_DATASET --output-dir DIR_TO_RESULTS
```

By skipping the above step, one can directly run the following to create a training and testing dataset consisting of patches in .png format by considering the patient identity:

```bash
python patch_discriminator.py  --frozen-dir DIR_TO_FROZEN_H5 --ffpe-dir DIR_TO_FFPE_H5 --train-thresh TRAIN_SPLIT_RATIO --test-thresh TEST_SPLIT_RATIO --output-dir DIR_TO_PATCHES
```

As a result, you are supposed to have the dataset in following structure:

#### Datasets
The data used for training are expected to be organized as follows:
```bash
Data_Path                # DIR_TO_TRAIN_DATASET
 ├──  trainA
 |      ├── 1.png     
 |      ├── ...
 |      └── n.png
 ├──  trainB     
 |      ├── 1.png     
 |      ├── ...
 |      └── m.png
 ├──  valA
 |      ├── 1.png     
 |      ├── ...
 |      └── j.png
 └──  valB     
        ├── 1.png     
        ├── ...
        └── k.png

```

To convert the frozen patches into AI-FFPE patches with a pretrained model:

```bash
python ../test.py DIR_TO_WSI --results-dir DIR_TO_PATCHES
```

To stitch-back the AI-FFPE patches as AI-FFPE WSI:

```bash
python stitiching.py --h5-inpath DIR_TO_H5 --down-ratio DOWN_SCALE  --preds-path DIR_TO_PREDICTED_PATCHES --output-dir DIR_TO_STITCHED_IMAGE
```
To visualize the stitched ".png" in the QuPath or similar application, one need to change the format of the file as ".tiff":

```bash
python png2tiff.py --input-dir DIR_TO_PNG --output-dir DIR_TO_TIFF  
```

