import urllib.request

url = "https://ftp.ncbi.nih.gov/gene/DATA/mim2gene_medgen"
output_file = "mim2gene_medgen"
urllib.request.urlretrieve(url, output_file)
print("File downloaded successfully!")