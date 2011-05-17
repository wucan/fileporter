# file porter
#
# porter files from one directory to another with patterns and more


__version__ = "0.3"


import os
import os.path
import sys
import time
import argparse
import shutil
import fnmatch


class FilePorter:
 
    def __init__(self, src="", dst="", pattern=['*']):
        self.src = src
        self.dst = dst
        self.pattern = pattern

        self.src = os.path.realpath(src)
        self.dst = os.path.realpath(dst)
        print('source:', self.src)
        print('destination:', self.dst)

    def run(self):
        while True:
            try:
                for f in os.listdir(self.src):
                    self.move_file(f)
            except Exception as ex:
                print(ex)
            time.sleep(1)

    def move_file(self, sub_path):
        src_full_path = os.path.join(self.src, sub_path)
        if os.path.isdir(src_full_path):
            for f in os.listdir(src_full_path):
                self.move_file(os.path.join(sub_path, f))
        else:
            match = False
            for pat in self.pattern:
                if fnmatch.fnmatch(os.path.basename(src_full_path), pat):
                    match = True
                    break;
            if not match:
                return
            if self.is_file_busying(src_full_path):
                return
            dst_full_path = os.path.join(self.dst, sub_path)
            print('move', src_full_path, '=>', os.path.dirname(dst_full_path), end=' ... ')
            sys.stdout.flush()
            try:
                #os.rename() will kill the src dir on windows!
                #os.renames(src_full_path, dst_full_path)

                #shutil.move() failed to already exist dst files in windows
                if not os.path.exists(os.path.dirname(dst_full_path)):
                    os.makedirs(os.path.dirname(dst_full_path))
                if os.path.exists(dst_full_path):
                    os.remove(dst_full_path)
                shutil.move(src_full_path, dst_full_path)
                print('Done.')
                time.sleep(0.01)
            except Exception as ex:
                print('Failed!')
                #print('move failed! ex:', ex)

    def is_file_busying(self, path):
        try:
            f = open(path, 'a')
            f.close()
            return False
        except IOError as err:
            return True

    def makedirs(self, path):
        dirs = path.split(os.path.sep)
        print(dirs)
        full_dir = ""
        for d in dirs:
            full_dir = os.path.join(full_dir, d)
            if not os.path.exists(full_dir):
                print('use os.makedirs() to create dir', full_dir)
                os.mkdir(full_dir)

    def makedirs_1(self, path):
        dirs = path.split(os.path.sep)
        print(dirs)
        rootdir = os.path.abspath(os.curdir)
        print('rootdir is', rootdir)
        parent_dir = rootdir
        for d in dirs:
            print('chdir() to dir', parent_dir)
            os.chdir(parent_dir)
            if not os.path.exists(d):
                print('use os.makedirs() to create dir', d)
                os.mkdir(d)
            parent_dir = os.path.join(parent_dir, d)
        os.chdir(rootdir)
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='File Porter')
    parser.add_argument('--src', dest='src', type=str,
                        required=True, nargs=1,
                        help='source directory')
    parser.add_argument('--dst', dest='dst', type=str,
                        required=True, nargs=1,
                        help='destinaiton directory')
    parser.add_argument('--pat', dest='pattern', type=str,
                        required=False, nargs='+',
                        help='file pattern')
    args = parser.parse_args()
    print(args)
    porter = FilePorter(args.src[0], args.dst[0], args.pattern)
    if porter:
        porter.run()
    sys.exit()

