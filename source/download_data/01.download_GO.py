import pandas as pd
import os
import requests

# URL of the file to download
url = 'https://purl.obolibrary.org/obo/go/go-basic.obo'

# Ensure the data directory exists
os.makedirs('../../data', exist_ok=True)

# Stream the download to avoid loading it all into memory at once
response = requests.get(url, stream=True)
response.raise_for_status()

# Write to file in chunks
outfile = os.path.join('../../data', 'go-basic.obo')
with open(outfile, 'wb') as f:
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            f.write(chunk)

print(f'Download complete: {outfile}')

# Download Annotations for 2025-04-28 release
# https://current.geneontology.org/products/pages/downloads.html



url = 'https://current.geneontology.org/annotations/goa_human.gaf.gz'


response = requests.get(url, stream=True)
response.raise_for_status()

outfile = os.path.join('../../data', 'goa_human.gaf.gz')
with open(outfile, 'wb') as f:
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            f.write(chunk)

print(f'Download complete: {outfile}')

# UNZIP the GAF file
import gzip
gaf_file = os.path.join('../../data', 'goa_human.gaf.gz')
with gzip.open(gaf_file, 'rb') as f_in:
    with open(os.path.join('../../data', 'goa_human.gaf'), 'wb') as f_out:
        f_out.write(f_in.read())
print(f'Unzipped GAF file: {os.path.join("../../data", "goa_human.gaf")}')