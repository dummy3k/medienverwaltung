import os
from optfunc import optfunc

def try_get_files(directory):
    try:
        return os.listdir(directory)
    except OSError, ex:
        return []

def find_dvds(directory):
    if directory[-1:] == '/':
        directory = directory[:-1]

    for item in try_get_files(directory):
        sub_dir = "%s/%s" % (directory, item)
        if os.path.isdir(sub_dir):
            if "VIDEO_TS" in try_get_files(sub_dir):
                print item
            else:
                find_dvds(sub_dir)

def main():
    optfunc.run(find_dvds)
    #~ optfunc.main([find_dvds,])

if __name__ == '__main__':
    main()
