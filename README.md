# Snr-Design-IRIS

## Information

### What is IRIS?

### Folder Structure

### Pi side structure

```
Dirs/
├─ zipped_data/
├─ piMain.py
├─ circleOutput/
├─ images/
│  ├─ input/
│  ├─ output/
│  ├─ compressed_images/
```

### Serevr Side structure

```
Dirs/
├─ unzippedFiles/
├─ circleOutput/
```

### Current Workflow

***Run `install_requirements.py` to get required packages***

***WORK IN PROGRESS***

1. piMain.py
    1. image detection
        1. main script to be ran on pi
        2. get images from `./dirs/images/input`
        3. run roboflow image detection model using API
        4. output images to `./dirs/images/output`
        5. hold for user verification
    2. compression
        1. take images from `./dirs/images/output`
        2. compress images to `./dirs/images/compressed_images`
    3. zip folder
        1. zip folder `./dirs/images/compressed_images`
        2. zipped output `./dirs/zipped_data/compressedImages.zip`

2. ***IR TRANSFER NOT DONE YET***

3. serverMain.py
    1. unzip file
        1. take file `./dirs/received_file.zip`
        2. unzip to `./Dirs/unzippedFiles`
    2. detect and crop red circles
        1. take `./Dirs/unzippedFiles`
        2. run through all images and detect red circles
        3. crop to red circles
        4. ouput to `./Dirs/circleOutput`
    3. git commit and push images to github

4. send images to server and display ***NOT DONE YET***
    1. ex: ![circle_1](https://github.com/Oluoma-Eziolise/Snr-Design-IRIS/blob/main/Dirs/circleOutput/circle_1.png)
    2. ![Circle_2](https://github.com/Oluoma-Eziolise/Snr-Design-IRIS/blob/main/Dirs/circleOutput/circle_2.png)
    3. ![Circle_3](https://github.com/Oluoma-Eziolise/Snr-Design-IRIS/blob/main/Dirs/circleOutput/circle_3.png)

5. display website from mobile app ***NOT DONE YET***
