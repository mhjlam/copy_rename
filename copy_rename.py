import argparse
import glob
import os
import shutil
import time

### Example 1: py copy_rename.py -si 1234 DCIM/100CANON photos
### Example 2: py copy_rename.py -cd -p vacay DCIM/100CANON vacay

class Error(Exception):
    pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source')
    parser.add_argument('target')
    meg = parser.add_mutually_exclusive_group()
    meg.add_argument('-cd', '--creation-date', action='store_true')
    meg.add_argument('-ni', '--next-index', action='store_true')
    meg.add_argument('-si', '--set-index', type=int)
    parser.add_argument('-p', '--prefix', type=str)

    args = parser.parse_args()
    source_dir = os.path.abspath(args.source)
    target_dir = os.path.abspath(args.target)

    # Make sure source directory exits
    if not os.path.isdir(source_dir):
        raise Error('Error: source directory \"{}\" does not exist.'.format(source_dir))

    # Create target directory if it does not exist yet
    if not os.path.isdir(target_dir):
        os.mkdir(target_dir)

    # Standard index
    next_index = 0

    # Custom indexing
    if args.set_index:
        try:
            if int(args.set_index) >= 0:
                next_index = args.set_index
        except ValueError:
            raise Error('Error: invalid input index \"{}\".'.format(args.set_index))
        
    # Continue from last index
    elif args.next_index:
        try:
            last_source_file = max(glob.glob('{}/*.jpg'.format(source_dir))) # path of last file in folder
            last_index = os.path.splitext(os.path.basename(last_source_file))[0][-5:]
            next_index = int(last_index) + 1
        except ValueError:
            raise Error('Error: no previous index to continue off.')

    # Copy and rename files from source to target directories
    for source_file in os.listdir(source_dir):
        source_path = '{}\\{}'.format(source_dir, source_file)
        
        # Determine prefix
        prefix = args.prefix or os.path.basename(source_path)[:3]
        
        # Use file creation date
        if args.creation_date:
            creation_date = time.strftime('%Y_%m_%d_%H%M%S', time.gmtime(os.path.getmtime(source_path)))
            target_file = '{}_{}.jpg'.format(prefix, creation_date)
        # Use index
        else:
            target_file = '{}_{:05d}.jpg'.format(prefix, next_index)
            next_index += 1
        
        target_path = '{}\\{}'.format(target_dir, target_file)
        shutil.copyfile(source_path, target_path)
        print('Copied {} to {}'.format(source_path, target_path))

if __name__ == '__main__':
    try:
        main()
    except Error as err:
        print(err)
        os.sys.exit(1)
