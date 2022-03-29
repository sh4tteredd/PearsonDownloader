# todo:
# a good guide/README
import urllib
from urllib import request
import os
import subprocess
from PIL import Image
from multiprocessing import Process, Pool, cpu_count
import shutil
import platform

def combine2Pdf(folderPath, pdfFilePath):
    files = os.listdir(folderPath)
    pngFiles = []
    sources = []
    for file in files:
        if 'png' in file:
            pngFiles.append(folderPath + file)
    pngFiles.sort()
    output = Image.open(pngFiles[0])
    pngFiles.pop(0)
    for file in pngFiles:
        pngFile = Image.open(file)
        if pngFile.mode == "RGB":
            pngFile = pngFile.convert("RGB")
        sources.append(pngFile)
    output.save(pdfFilePath, "pdf", save_all=True, append_images=sources)

def main():
#    if os.path.exists("BooksCache/"):
#       shutil.rmtree('BooksCache/', ignore_errors=True)
    v = input("verbose (y/N): ")
    v = v.lower()
    if v == "y":
        verbose = 1
    else:
        verbose = 0
    num = input("Product Number: ")
    _id = input("Book ID: ")
    print("That's where to find your cookies: https://imgur.com/a/jj1Y4dS")
    cookies = input("cookies: ")
    pdfFile = num+".pdf"
    pages = int(input("How many pages would you like to download? "))
    print("Downloading page images...")
    path = os.path.join("BooksCache/", _id)
    os.makedirs(path)
    pool = Pool(cpu_count())
    for i in range(0, pages):
        pool.apply_async(get_files, args=(_id, i,num,cookies,verbose))
    pool.close()
    pool.join()
    combine2Pdf("BooksCache/"+_id+"/", num+".pdf")
    shutil.rmtree('BooksCache/', ignore_errors=True)
    if platform.system() == "Darwin":  # macOS
      subprocess.call(('open', pdfFile))
    elif platform.system() == "Windows":  # Windows
      os.startfile(pdfFile)
    else:                                   # linux distros
        subprocess.call(('xdg-open', pdfFile))
def get_files(_id, page, num,cookies,verbose):
    pb = f'https://plus.pearson.com/eplayer/pdfassets/prod1/{num}/{_id}/pages/page{page}?password=&accessToken=null&formMode=true'
    opener = request.build_opener()
    opener.addheaders = [('Cookie', cookies)]
    request.install_opener(opener)
    request.urlretrieve(pb, f'BooksCache/{_id}/{page}.png')
    if verbose == 1: 
        print(f"Downloaded page {page+1}!\n")
        print(opener)

if __name__ == "__main__":
    main()
