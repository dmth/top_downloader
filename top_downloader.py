"""
This software is intended to bulk download maps from
https://www.opengeodata.nrw.de/produkte/geobasis/dtk/

"""

import argparse
import json
import requests
import tempfile
import os


"""
The version-number
"""
version = (0, 0, 1)
__version__ = '.'.join('%d' % p for p in version)

"""
A dict of product names and URLs
"""
__products__ = {
    'dtk50': 'https://www.opengeodata.nrw.de/produkte/geobasis/dtk/dtk50/dtk50pdf/',
    'dtk100': 'https://www.opengeodata.nrw.de/produkte/geobasis/dtk/dtk100/dtk100pdf/',
}


def http_downloader(url: str, mode: str=''):
    """

    Args:
        url: The document which shall be downloaded
        mode: The mode in which the download should take place, can be 'json', defaults to ''

    Returns: The content of the download either as parsed json when mode was 'json' or otherwise.

    """
    r = requests.get(url,  timeout=10)

    if r.status_code != requests.codes.OK:
        # something went wrong.
        raise('Download error. Getting %s returned %s' % (url, r.status_code))

    if mode == 'json':
        return r.json
    if mode == 'text':
        return r.text
    else:
        return r.content


def get_files_from_index_json(index: str):
    """
    Reads the index-file of the map-collection and parses it into a dict.

    Args:
        index: the json-document

    Returns: An Array containing dicts which describe the downloadable file.
             The description consist of: name, size, timestamp

    """
    index_dl = http_downloader(index, 'text')
    j_index = json.loads(index_dl)
    datasets = j_index.get('datasets', None)

    if datasets == None:
        raise ValueError('The index-document does not contain datasets.')

    files = []

    for ds in datasets:
        # iterate the Datesets and add all files to the files
        # this iteration is done, in hope that the it works if multiple datasets
        # occur. With one Dataset the result should be the same as datasets[0].get('files')
        fs = ds.get('files', None)
        if fs:
            for f in fs:
                files.append(f)

    if files is None:
        raise ValueError('The index-document does not contain files.')

    return files


def get_product_url(product: str):
    """
    Args:
        product: The product which should be downloaded, dtk50 or dtk100

    Returns: the URL which is stored in the dict above.

    """
    url = __products__.get(product, None)
    if url is None:
        raise NotImplementedError('Product error: %s is unkown' % (product))
    return url


def create_download_folder(product: str, path: str=None):
    """

    Args:
        product: The name of the product
        path: The path where the download-folder shall be created, defaults to temp

    Returns: The path to the download-folder

    """

    if path is None:
        abs_path_to_folder = tempfile.mkdtemp(suffix=None, prefix=product + '_')
    else:
        raise NotImplementedError('Creating download Directories outside of temp is not supported.')

    return abs_path_to_folder


def file_downloader(files, producturl: str, downloaddir: str):
    """
    Args:
        files: An array containing the file-names
        producturl: The URL of the products
        downloaddir: The direcory where the new files shall be created.

    Returns: None

    """
    # TODO: Replace Print-Outs with a Logger

    print("Downloading %s files." % (files.__len__()))
    dl_ctr = 0
    for f in files:
        fname = f.get('name', None)
        if not fname:
            # Skip files without a name
            continue

        fileurl = producturl + fname
        # now download
        print("Downloading %s." % (fileurl))

        content = http_downloader(fileurl)
        with open(os.path.join(downloaddir, fname), 'w+b') as outfile:
            outfile.write(content)

        dl_ctr+=1
        print("Downloaded %s of %s files." % (dl_ctr , files.__len__()))

    return None

def main():
    # TODO: Replace Print-Outs with a Logger

    parser = argparse.ArgumentParser(description='Bulk-Download DTK-Maps as PDFs from https://www.opengeodata.nrw.de')

    parser.add_argument('--version', action='version', version=('Version %s' % __version__))
    parser.add_argument('--product', nargs='?', choices=__products__.keys(), default='dtk50')

    args = parser.parse_args()

    product = args.product
    product_url = get_product_url(product)

    # Step 1: Parse the Index file into "files"
    files = get_files_from_index_json(product_url + 'index.json')

    # Step 2: Create the Download-Folder
    dlpath = create_download_folder(product)
    print('Data will be downloaded to: %s' % dlpath)

    # Step 3: Iterate "files" and download every file an write it to the Download-folder
    file_downloader(files, product_url, dlpath)

    exit(0)

if __name__ == "__main__":
    main()