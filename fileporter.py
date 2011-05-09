import os
import os.path
import sys
import time
import argparse


class FilePorter:
 
    def __init__(self, src="", dst="", pattern='*'):
        self.src = src
        self.dst = dst
        self.pattern = pattern

        if not os.path.exists(dst):
            try:
                os.makedirs(dst)
            except Exception as ex:
                print('create destination dir:', dst)
                raise

    def run(self):
        while True:
            for f in os.listdir(self.src):
                self.move_file(f)
            time.sleep(1)

    def move_file(self, sub_path):
        src_full_path = os.path.join(self.src, sub_path)
        if os.path.isdir(src_full_path):
            for f in os.listdir(src_full_path):
                self.move_file(os.path.join(sub_path, f))
        else:
            dst_full_path = os.path.join(self.dst, sub_path)
            print('move', src_full_path, '=>', dst_full_path)
            try:
                os.renames(src_full_path, dst_full_path)
                time.sleep(1)
            except Exception as ex:
                print('move failed! ex:', ex)
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='File Porter')
    parser.add_argument('--src', dest='src', type=str,
                        required=True, nargs=1,
                        help='source directory')
    parser.add_argument('--dst', dest='dst', type=str,
                        required=True, nargs=1,
                        help='destinaiton directory')
    args = parser.parse_args()
    print(args)
    porter = FilePorter(args.src[0], args.dst[0], '*.ts')
    if porter:
        porter.run()
    sys.exit()

