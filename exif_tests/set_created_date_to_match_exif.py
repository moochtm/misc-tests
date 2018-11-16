
# import (1) python built-in, (2) downloaded 3rd party, (3) own

import datetime, time, os, json

import thirdparty.exiftool as exiftool
import thirdparty.sortphotos as sortphotos

"""

if 'EXIF:CreateDate' in json_text[0].keys():
    cd = datetime.datetime.strptime(json_text[0]['EXIF:CreateDate'], "%Y:%m:%d %H:%M:%S")
    createTime = time.mktime(cd.timetuple())
    print createTime
    os.utime(files[0], (createTime, createTime))
"""

def main(root_path):

    print '----------------------------------------------------------------'
    print 'starting up exiftool'

    et = exiftool.ExifTool()
    et.start()

    print 'starting to walk from root (%s)' % root_path

    if not os.path.isdir(root_path):
        print 'ERROR root is not folder (%s)' % root_path
        return False

    for dirName, subdirList, fileList in os.walk(root_path):
        for f in fileList:
            file_path = os.path.join(dirName, f)
            print 'file: %s' % file_path
            file_exif = et.get_metadata(file_path)
            _, oldest_date, _ = sortphotos.get_oldest_timestamp(file_exif, [], [])
            if oldest_date is not None:
                oldest_time = time.mktime(oldest_date.timetuple())
                print "writing to file's create date..."
                os.utime(file_path, (oldest_time, oldest_time))

    print 'closing exiftool'

    et.terminate()

    print '----------------------------------------------------------------'


if __name__ == "__main__":

    root_path = '/Users/matt.barr/Pictures/testing/bob/jeff'

    main(root_path)

