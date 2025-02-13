# Snr-Design-IRIS

## Information

### What is IRIS?

### Current Workflow

***Run `install_requirements.py` to get required packages***

***WORK IN PROGRESS***

1. piMain.py
    1. image detection
        1. main script to be ran on pi
        2. get images from `./dirs/images/input`
        3. run roboflow image detection model using API
        4. output images to `./dirs/images/output`
    2. compression
        1. take images from `./dirs/images/output`
        2. compress images to `./dirs/images/compressed_images`
    3. zip folder
        1. zip folder `./dirs/images/compressed_images`
        2. zipped output `./dirs/zipped_data/compressedImages.zip`
    4. encrypt zip file
        1. take zip `./dirs/zipped_data/compressedImages.zip`
        2. encrypt file to `./dirs/zipped_data/compressedImages.zip.enc`
    5. base64 encode to chunks for sending
        1. take `./dirs/zipped_data/compressedImages.zip.enc`
        2. base64 encode folder to `./Dirs/encoded_chunks.txt`

2. ***IR TRANSFER NOT DONE YET***

3. serverMain.py
    1. decode chunks
        1. take `./dirs/encoded_chunks.txt`
        2. decode into zip.enc file `./Dirs/received_file.zip.enc`
    2. decrypt folder
        1. take file `./dirs/received_file.zip.enc`
        2. decrypt to `./dirs/received_file.zip`
    3. unzip file
        1. take file `./dirs/received_file.zip`
        2. unzip to `./Dirs/unzippedFiles`
    4. detect and crop red circles
        1. take `./Dirs/unzippedFiles`
        2. run through all images and detect red circles
        3. crop to red circles
        4. ouput to `./Dirs/circleOutput`

4. send images to server and display ***NOT DONE YET***

5. display website from mobile app ***NOT DONE YET***
