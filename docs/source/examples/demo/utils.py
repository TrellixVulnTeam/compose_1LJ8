import os
import requests
import tarfile
from tqdm import tqdm
from zipfile import ZipFile


def download(url, output='data'):
    response = requests.get(url, stream=True)
    assert response.status_code == 200, "unable to download data"
    content_type = response.headers['Content-Type']
    content = response.iter_content(chunk_size=int(1e+6))
    bar_format = "Downloaded: {n}MB / {total}MB -{rate_fmt}, "
    bar_format += "Elapsed: {elapsed}, Remaining: {remaining}, Progress: {l_bar}{bar}"
    total = round(int(response.headers.get('content-length', 0)) / 1e+6)
    content = tqdm(content, total=total, unit="MB", bar_format=bar_format)
    extract(content, content_type, output)
    response.close()


def extract(content, content_type, output):
    if content_type == 'application/zip': extract_zip(content, output)
    elif content_type == 'application/x-gzip': extract_tarball(content, output)
    else: raise TypeError(f'"{content_type}" not supported')


def extract_tarball(content, output):
    with open('data.tar.gz', 'wb') as file:
        for chunk in content:
            file.write(chunk)

    with tarfile.open('data.tar.gz', "r:gz") as file:
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(file, output)

    os.remove('data.tar.gz')


def extract_zip(content, output):
    with open('data.zip', 'wb') as file:
        for chunk in content:
            file.write(chunk)

    with ZipFile('data.zip', 'r') as file:
        file.extractall(output)

    os.remove('data.zip')
