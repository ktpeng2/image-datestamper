import datetime
import os
import shutil
from PIL import Image, ExifTags, ImageDraw, ImageFont

#this script is for time stamping sony cybershot dsc wx150 images of default settings

#convert date to return list of [date, time]
def militaryTimeConvert(date):
    if int(date[:2]) >= 12:
        if int(date[:2]) == 12:
            return "12"+date[2:]+"PM"
        else:
            return str(int(date[:2])-12)+date[2:]+"PM"
    else:
        if int(date[:2]) == 0:
            return "12"+date[2:]+"AM"
        else:
            return date+ "AM"
        
#creating the directory where the edited pictures will be
def createDatestampedDir():
    pth = './datestamped'
    try:
        os.mkdir(pth)
        print("Folder %s created!" %pth)
    except FileExistsError:
        print("Folder %s already exists, clearing all files in there" %pth)
        for file in os.scandir('./datestamped'):
            os.remove(file.path)
        print('directory cleared')

#editing the images to apply date and time in bottom right corner
def modifyImages(imgDateDict, origTimeDict):
    cnt = 0
    tot = len(os.listdir('./datestamped'))
    for file in os.listdir('./datestamped'):
        path = './datestamped/'+file
        im = Image.open(path)

        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation]=='Orientation':
                break
        exif = im._getexif()

        #exif[orientation] using this to determine if landscape or portrait in my images
        #anything that isnt 1 is in portrait

        h, w = im.size

        draw = ImageDraw.Draw(im)
        text = imgDateDict[file][0] + " " + imgDateDict[file][1]
        font1 = ImageFont.truetype('RobotoMono-Regular.ttf', 125)
        draw.text((3400,3400), text, font=font1, fill='yellow')
        im.save(path)
        cnt += 1
        print('[%d / %d]' %(cnt, tot))

        #after editing images, change the modify time using the orig img time dictionary
        os.utime(path,(origTimeDict[file].st_atime,origTimeDict[file].st_mtime))

def main():
    createDatestampedDir()

    dirPath = input("Please enter the file path of the directory for images: ")
    entries =  os.listdir(dirPath)
    cnt,prcnt = 0, 0
    imgDateDict = {}
    print('\nCopying files over to new directory to not modify original images')
    origTimeDict = {}
    for i in entries:
        path = dirPath+"\\"+i
        #copying images to newly created folder
        shutil.copy(path, './datestamped')

        #getting time data to put on the image using pillow library
        m_time = os.path.getmtime(path)
        dt_m = datetime.datetime.fromtimestamp(m_time)
        time = militaryTimeConvert(dt_m.strftime("%H:%M"))
        imgDateDict[i] = [dt_m.strftime("%m/%d/%Y"), time]

        #inserting elements into dictionary conisting of [imgName] = [origImgMetaData]
        st = os.stat(path)
        origTimeDict[i] = st

    print('All files copied over, preparing to edit')
    modifyImages(imgDateDict, origTimeDict)
    print('All images completed!')


main()