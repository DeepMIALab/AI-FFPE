# AI-FFPE Data Process

For the dataset processing steps build the environment by running:

```bash
pip install requirements.txt
```

#### Create Patches

 One can start to create patches by following commend:

```bash
python create_patches.py DIR_TO_WSI --results-dir DIR_TO_PATCHES
```

#### Create Patches in the format that is Processable by AI-FFPE Networks

Convert .h5 into ".png" :

```bash
python h52png.py  --pretrained-posenet DIR_TO_PRETRAINED_MODEL --dataset-dir DIR_TO_TEST_DATASET --output-dir DIR_TO_RESULTS
```

To creaate a training and testing dataset by considering the patient identity:

As a result, you are supposed to have the training dataset in following structure:

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
 |      └── k.png
 └──  valB     
        ├── 1.png     
        ├── ...
        └── l.png

```

To convert the frozen patches into AI-FFPE patches with a pretrained model:

```bash
python test.py DIR_TO_WSI --results-dir DIR_TO_PATCHES
```

To stitch-back the AI-FFPE patches as AI-FFPE WSI:

```bash
python stitiching.py --h5-path DIR_TO_H5  --results-dir DIR_TO_PATCHES
```




