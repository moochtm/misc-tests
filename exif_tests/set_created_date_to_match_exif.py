
# import (1) python built-in, (2) downloaded 3rd party, (3) own

import json, datetime, time, os

import thirdparty.exiftool as exiftool

files = ['test.jpg']

with exiftool.ExifTool() as et:
    json_text = et.get_metadata_batch(files)

if 'EXIF:CreateDate' in json_text[0].keys():
    cd = datetime.datetime.strptime(json_text[0]['EXIF:CreateDate'], "%Y:%m:%d %H:%M:%S")
    createTime = time.mktime(cd.timetuple())
    os.utime(file[0]), (createTime, createTime)
