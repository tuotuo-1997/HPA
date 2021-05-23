import io
import os
import requests
import pathlib
import gzip
import sys
import imageio
import pandas as pd
from tqdm import tqdm
from multiprocessing import Pool

def tif_gzip_to_png(tif_path):
    '''Function to convert .tif.gz to .png and put it in the same folder
    Eg. for working in local work station
    '''
    png_path = pathlib.Path(tif_path.replace('.tif.gz','.jpg'))
    tf = gzip.open(tif_path).read()
    img = imageio.imread(tf, 'tiff')
    imageio.imwrite(png_path, img)
    
def download_and_convert_tifgzip_to_png(url, target_path):    
    '''Function to convert .tif.gz to .png and put it in the same folder
    Eg. in Kaggle notebook
    '''
    r = requests.get(url)
    f = io.BytesIO(r.content)
    tf = gzip.open(f).read()
    # img = imageio.imread(tf, 'tiff')
    img = imageio.imread(url)
    imageio.imwrite(target_path, img)

# All label names in the public HPA and their corresponding index. 
all_locations = dict({
    "Nucleoplasm": 0,
    "Nuclear membrane": 1,
    "Nucleoli": 2,
    "Nucleoli fibrillar center": 3,
    "Nuclear speckles": 4,
    "Nuclear bodies": 5,
    "Endoplasmic reticulum": 6,
    "Golgi apparatus": 7,
    "Intermediate filaments": 8,
    "Actin filaments": 9,
    "Focal adhesion sites": 9,
    "Microtubules": 10,
    "Mitotic spindle": 11,
    "Centrosome": 12,
    "Centriolar satellite": 12,
    "Plasma membrane": 13,
    "Cell Junctions": 13,
    "Mitochondria": 14,
    "Aggresome": 15,
    "Cytosol": 16,
    "Vesicles": 17,
    "Peroxisomes": 17,
    "Endosomes": 17,
    "Lysosomes": 17,
    "Lipid droplets": 17,
    "Cytoplasmic bodies": 17,
    "No staining": 18
})

def add_label_idx(df, all_locations):
    '''Function to convert label name to index
    '''
    df["Label_idx"] = None
    for i, row in df.iterrows():
        labels = row.Label.split(',')
        idx = []
        for l in labels:
            if l in all_locations.keys():
                idx.append(str(all_locations[l]))
        if len(idx)>0:
            df.loc[i,"Label_idx"] = "|".join(idx)
            
        print(df.loc[i,"Label"], df.loc[i,"Label_idx"])
    return df


def download_images(save_dir, df, pid, start_idx, end_idx):
    df = df[start_idx:end_idx]
    for i in tqdm(range(len(df)), postfix=pid):
        row = df.iloc[i]
        try:
            img = row.Image
            for color in colors:
                img_url = f'{img}_{color}.jpg'
                img_url = img_url.replace('https', 'http')
                save_path = os.path.join(save_dir,  f'{os.path.basename(img)}_{color}.jpg')
                response = requests.get(img_url, allow_redirects=True)
                open(save_path, "wb").write(response.content)
                # print(f'Downloaded {img_url} as {save_path}')    
        except:
            print(f'failed to download: {img}')


def run_proc(save_dir, df, name, start_idx, end_idx):
    """Handle one mp process."""
    print(
        "Run child process %s (%s) start:%d end: %d"
        % (name, os.getpid(), start_idx, end_idx)
    )
    download_images(save_dir, df, name, start_idx, end_idx)
    print("Run child process %s done" % (name))


def download_hpa(save_dir, df, process_num=30):
    os.makedirs(save_dir, exist_ok=True)
    print("Parent process %s." % os.getpid())
    list_len = len(df)
    pool = Pool(process_num)
    for i in range(process_num):
        pool.apply_async(
            run_proc,
            args=(
                save_dir,
                df,
                str(i),
                int(i * list_len / process_num),
                int((i + 1) * list_len / process_num),
            ),
        )
    print("Waiting for all subprocesses done...")
    pool.close()
    pool.join()
    print("All subprocesses done.")

public_hpa_df = pd.read_csv('./kaggle_2021.tsv')
# Remove all images overlapping with Training set
public_hpa_df = public_hpa_df[public_hpa_df.in_trainset == False]

# Remove all images with only labels that are not in this competition
public_hpa_df = public_hpa_df[~public_hpa_df.Label_idx.isna()]

colors = ['blue', 'red', 'green', 'yellow']
celllines = ['A-431', 'A549', 'EFO-21', 'HAP1', 'HEK 293', 'HUVEC TERT2', 'HaCaT', 'HeLa', 'PC-3', 'RH-30', 'RPTEC TERT1', 'SH-SY5Y', 'SK-MEL-30', 'SiHa', 'U-2 OS', 'U-251 MG', 'hTCEpi']
public_hpa_df_17 = public_hpa_df[public_hpa_df.Cellline.isin(celllines)]
len(public_hpa_df), len(public_hpa_df_17)

download_hpa('./HPA_Public/', public_hpa_df)




