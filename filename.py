#!/usr/bin/python
import os
import sys

def safe_name(input):
    valid_chars = '-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(c for c in input if c in valid_chars)

# def main():
#     for root, dirs, files in os.walk("."):
#         for unsafe in files:
#             safe = safe_name(unsafe)
#             print('mv {} to {}'.format(os.path.join(root,unsafe), safe))
#             if safe != '':
#                 os.rename(os.path.join(root,unsafe), os.path.join(root,safe))
#         for unsafe in dirs:
#             safe = safe_name(unsafe)
#             print('mv {} to {}'.format(os.path.join(root,unsafe), safe))
#             if safe != '':
#                 os.rename(os.path.join(root,unsafe), os.path.join(root,safe))
#     print('main done')

def change_to_safename(dirname, entry, fp):
    safe = safe_name(entry.name)
    fp.write('<li><a href="{0}/{1}" >{1}</a></li>\n'.format(dirname,safe))
    if safe != '' and (not os.path.exists(dirname+'/'+safe)):
        os.rename(entry.path, dirname+'/'+safe)
        return dirname+'/'+safe
    else:
        return entry.path



def recurse(dirname, fp):
    for entry in sorted(os.scandir(dirname), reverse=True, key=lambda x: (x.is_dir(), x.name)):
        if not entry.name.startswith('.'): 
            newName = change_to_safename(dirname,entry,fp)
            if entry.is_dir():
                recurse(newName, fp)

def main():
    assert len(sys.argv) > 1, 'put any argument it doesn\'t matter. Filenames will be changed to windows safe.'
    indexFile = 'index.html'
    with open(indexFile, 'w') as fp:
        fp.write('<html><head><title>Index</title></head><body>\n<ol>')
        recurse('.', fp)
        fp.write('</ol>\n</body></html>')
    print('done')

if __name__ == '__main__':
    main()
