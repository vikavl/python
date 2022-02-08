import os
import sys
from pathlib import Path
import shutil

# formats of extensions
formats = {
    "images": ['JPEG', 'PNG', 'JPG', 'SVG'],
    "video": ['AVI', 'MP4', 'MOV', 'MKV'],
    "documents": ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', 'XLS', 'CSV'],
    "audio": ['MP3', 'OGG', 'WAV', 'AMR'],
    "archives": ['ZIP', 'GZ', 'TAR'],
    "others": []
}
# directories to move sorted files
perm_folders = ["images", "documents", "audio", "video", "archives"]

# translation map
CYRILLIC = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
LATIN = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
    "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")
TRANSLIT_DICT = {}
for c, l in zip(CYRILLIC, LATIN):
    TRANSLIT_DICT[ord(c)] = l
    TRANSLIT_DICT[ord(c.upper())] = l.upper()

def normalize(file):
    filename = file.name
    suffix = file.suffix
    filename = filename.removesuffix(suffix).translate(TRANSLIT_DICT)
    result = ""
    for i in filename:
        if i.isalnum():
            result += i
        else:
            result += "_"
    result += suffix
    return Path(str(file.parent) + "\\" + result)

#return folder name; if 'others' - add unknown extensions to list of formats
def sort_file(file, my_dir):

    filename = file.name
    file_suffix = file.suffix[1:].upper()

    for folder, suffixes in formats.items():
        if file_suffix in suffixes:
            if folder != "others" and folder != "archives":
                os.replace(file, Path(str(my_dir) + "\\" + folder + "\\" + filename))
                #print(f"{filename} will move to '{folder}'")
                return folder
            # unpack archives in new directories in 'archive' directory
            elif folder == "archives":
                arch_dir = Path(str(my_dir) + '\\' + "archives" + '\\' + filename.removesuffix(file.suffix))
                if arch_dir.exists() == False:
                    os.mkdir(arch_dir)
                shutil.unpack_archive(file, arch_dir)
                os.remove(file)
                return arch_dir.name

    # add unknown extensions to formats dict
    if file_suffix not in formats["others"] and file_suffix != '':
        formats["others"].append(file_suffix)
        return "others"

# structure of directories
my_struct = {}

def take_out_trash(my_dir):

    print("CURRENT DIRECTORY:", my_dir)
    my_struct[my_dir] = []

    # check if permanent directory exists, otherwise - create
    for folder in perm_folders:
        if Path(str(my_dir)+'\\'+folder).exists() == False:
            os.mkdir(Path(str(my_dir)+'\\'+folder))

    # rename all files in directory to normal and delete empty folders
    for f in my_dir.iterdir():
        if f.is_dir() and len(os.listdir(f)) == 0 and f.name not in perm_folders:
            #print(f.name, "is deleted...")
            os.rmdir(f)
        # remember all directories in current dir
        elif f.is_dir() and f.name not in perm_folders:
            my_struct[my_dir].append(f)
        else:
            os.rename(f, normalize(f))

    # move files to folders
    for f in my_dir.iterdir():
        #print(f.suffix.upper())
        if f.is_dir() and f.name not in perm_folders:
            #print(f"CAN`T SORT. It is not empty directory - '{f.name}'")
            continue
        else:
            sort_file(f, my_dir)

    # check trash into other directories (recursive)
    for folder in my_struct[my_dir]:
        take_out_trash(folder)

take_out_trash(Path(sys.argv[1]))
print("Unknown extensions:", formats["others"])
