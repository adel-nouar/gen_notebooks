'''
TODOs: 
- Test for copy part: 
        --> folders copied in the jupyter starter and final folders
        --> notebooks copied in the jupyter starter and final folders
        --> other files copied in the jupyter starter and final folders

- Test all code cells in starter notebooks cleared

- Modify the add_header_colab function:
        --> Take GIT_HUB_PATH constant, and concatenate with the folder name (only main folder project name + subfolders (colab/starer and colab/final)).
        
        --> Create a text represent the google colabs link with the constant above.

        --> Create a cell with the previous text.

        --> add the entire notebook to that cell.

        --> save the notebook filename (bye overriding it with the new content).

- Instead of given list of folders in the command arguments:
        --> An input file with the list of all repos to modify
        --> for each repos: 
                            ---> git clone
                            ---> git checkout -b dev
                            ---> performs the actions
                            ---> git push

- When all things work, cleaning the code, and using OOP, each repos will be an object.

'''

from distutils.file_util import copy_file
from genericpath import isfile
import sys
import nbformat as nbf
from os.path import isdir, join
from os import listdir, getcwd
from shutil import copytree


GIT_HUB_PATH = "https://github.com/LearnPythonWithRune/"

current_path:str = ""

jupyter_dir:str = ""
jupyter_final:str = ""
jupyter_starter:str = ""

colab_dir:str = ""
colab_final:str = ""
colab_starter:str = ""

notebooks = []

def fill_paths(folder:str):
    current_path = join(getcwd(), folder)

    jupyter_dir = join(current_path, 'jupyter') 
    jupyter_final = join(jupyter_dir, 'final')
    jupyter_starter = join(jupyter_dir, 'starter')

    colab_dir = join(current_path, 'colab')
    colab_final = join(colab_dir, 'final')
    colab_starter = join(colab_dir, 'starter')


def copy_files(files:list[str]):
    for file in files:
        copy_file(file, jupyter_starter)
        copy_file(file, jupyter_final)

        copy_file(file, colab_starter)
        copy_file(file, colab_final)


def copy_folders(folders:list[str]):
    for folder in folders:
        copytree(folder, jupyter_final)
        copytree(folder, jupyter_starter)


def copy_documents(folder_content:list[str], folders:list[str], notebooks:list[str], other_files:list[str]):
    if len(notebooks) > 0:
        copy_files(notebooks)
    else:
        print('ERROR: No notebooks')
    if len(folders) > 0:
        copy_folders(folders)
    if len(other_files) > 0:
        copy_files(other_files)

def get_inside(folder:str):
    folder_content = listdir(folder)
    
    folders = [d for d in folder_content if isdir(d)]
    
    notebooks = [f_ntbk for f_ntbk in folder_content if isfile(f_ntbk) and f_ntbk[-6:] == '.ipynb' ]
    
    other_files = [f for f in folder_content if isfile(f) and f[-6:] != '.ipynb' ]

    return folder_content, folders, notebooks, other_files


def gen_content(folder:str) -> bool:

    folder_content, folders, notebooks, other_files = get_inside(folder)
    
    if len(notebooks) > 0:
        copy_documents(folder_content, folders, notebooks, other_files)
        return True
    else:
        return False


def generate(folder:str) -> bool:
    if gen_content(folder):
        return True
    else:
        print('ERROR in a specified folder no notebooks')
        return False


def clear_code(notebook):
    ntbk = nbf.read(notebook, nbf.NO_CONVERT)
    new_ntbk = ntbk
    new_ntbk.cells = [cell if cell.cell_type == "markdown" else nbf.v4.new_code_cell() for cell in ntbk.cells ]
    nbf.write(new_ntbk, notebook, version=nbf.NO_CONVERT)


def add_header_colab(notebook):
    ntbk = nbf.read(notebook, nbf.NO_CONVERT)
    text_link = ""
    # code = ""
# %pylab inline
# hist(normal(size=2000), bins=50);"""

    # cells = [nbf.v4.new_markdown_cell(text), nbf.v4.new_code_cell(code)]
    cell_link = nbf.v4.new_markdown_cell(text)
    ntbk['cells'].extend(cells)

    nbf.write(nb, 'eda_new.ipynb')


def clean_notebooks():
    for notebook in notebooks:
        jupyt_strt:str = join(jupyter_starter, notebook)
        clear_code(jupyt_strt)
        
        colb_strt:str = join(colab_starter, notebook)
        colb_finl:str = join(colab_final, notebook)
        clear_code(colb_strt)
        add_header_colab(colb_finl)


if len(sys.argv) >= 2:
    for arg in sys.argv:
        if isdir(arg): 
            fill_paths(arg)
            if generate(arg):
                clean_notebooks()
            # Remove old notebooks
        else:
            print(f'{arg} is not a directory')
else:
    print('Format: ...')