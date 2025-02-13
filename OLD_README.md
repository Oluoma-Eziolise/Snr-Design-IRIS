# Snr-Design-IRIS

## Information

### What is IRIS?

### Current Workflow

***Run `install_requirements.py` to get required packages***

***WORK IN PROGRESS***

1. workflow.py
    1. get images from folder `./dirs/images/input`
    2. use api call to roboflow to identfy Death Star Images and send to `./dirs/images/output`
2. compress.py
    1. Grab images from `./dirs/images/output`***need to move to server side***
    2. compress images and output to `./dirs/images/compressed_images`
3. zipEncrypt.py
    1. get compressed images folder `./testImages/compressed_images`
    2. copy folder and contents to `./zipped_data/compressed_images`
    3. zip folder into `./zipped_data/compressedImages.zip`
    4. encrypt folder using password and store as `./zipped_data/compressedImages.zip.enc`
4. encode.py
    1. encode `./zipped_data/compressedImages.zip.enc` into base64 chunks
    2. save as `encoded_chunks.txt`
5. transfer over IR
    1. ***NOT DONE YET***
6. decode.py
    1. take `encoded_chunks.txt` and decode it into `received_file.zip.enc`
7. decrypt.py
    1. take `received_file.zip.enc` and decrypt using password
    2. store decrypted zip as `received_file.zip`
8. unzip.py
    1. take `received_file.zip` and unzip file
    2. verify all images are present
