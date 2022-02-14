from genericpath import isfile
import sys
import nbformat as nbf
from os.path import isdir
from os import listdir



def gen_jupyter(folder_content):
    pass

def gen_colab(folder_content):
    pass


def copy_documents(folder_content, folders, notebooks, other_files):
    pass


def get_inside(folder):
    folder_content = listdir(folder)
    
    folders = [d for d in folder_content if isdir(d)]
    
    notebooks = [f_ntbk for f_ntbk in folder_content if isfile(f_ntbk) and f_ntbk[-6:] == '.ipynb' ]
    
    other_files = [f for f in folder_content if isfile(f) and f[-6:] != '.ipynb' ]

    return folder_content, folders, notebooks, other_files


def gen_content(folder:str):

    folder_content, folders, notebooks, other_files = get_inside(folder)
    
    copy_documents(folder_content, folders, notebooks, other_files)





def generate(folder:str):
    gen_content(folder)
    gen_header(folder)
    clear_code_starter(folder)




if len(sys.argv) >= 2:
    for arg in sys.argv:
        if isdir(arg): 
            print('YES')
            generate(arg)
            # Remove old notebooks
        else:
            print(f'{arg} is not a directory')
else:
    print('Format: ...')