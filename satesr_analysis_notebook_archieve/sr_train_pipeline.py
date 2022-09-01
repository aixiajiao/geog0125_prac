#!/usr/bin/env python
# coding: utf-8

# In[ ]:

#download data

import os
os.system("python -m pip install --upgrade pip")
os.system('pip install requests')
os.system('pip install tqdm')
import requests
from tqdm import tqdm
import zipfile


def download(url: str, fname: str, chunk_size=1024):
    resp = requests.get(url, stream=True)
    total = int(resp.headers.get('content-length', 0))
    with open(fname, 'wb') as file, tqdm(
        desc=fname,
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=chunk_size):
            size = file.write(data)
            bar.update(size)


url = 'https://onedrive.live.com/download?cid=1FBE8A2F75A20AE8&resid=1FBE8A2F75A20AE8%21196320&authkey=AE9zYgs-aHn555o'
fname='photoset.zip'
train_url =  'https://onedrive.live.com/download?cid=1FBE8A2F75A20AE8&resid=1FBE8A2F75A20AE8%21196325&authkey=AKqUIe0hw419j9w'
fname1='train_satesr.zip'

if not os.path.exists('photoset'):
    download(url,fname)
    try:
        with zipfile.ZipFile(fname) as z:
            z.extractall()
            print("Data Extracted as photoset")
    except:
        print("Extraction Failed")

if not os.path.exists('satesr'):
    download(train_url,fname1)
    try:
        with zipfile.ZipFile(fname1) as z:
            z.extractall()
            print("train data extracted")
    except:
        print("Extraction Failed")

# In[1]:


os.system('conda install pytorch torchvision torchaudio cudatoolkit=11.6 -c pytorch -c conda-forge')
os.system('pip install basicsr')

# In[ ]:


os.system('python satesr/realesrgan/train.py -opt satesr/options/finetune_realesrgan_x4plus.yml --auto_resume')


# In[ ]:


os.system('zip -r ft_model.zip satesr/experiments')

