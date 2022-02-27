'''
TODOs:
- Test for copy part:
        --> folders copied in the jupyter starter and final folders : KO
        --> notebooks copied in the jupyter starter and final folders : OK
        --> other files copied in the jupyter starter and final folders : OK

- Test all code cells in starter notebooks cleared : OK

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
import sys
import nbformat as nbf
import os
from os.path import isdir, isfile, join, basename, splitext
from os import listdir, getcwd, makedirs
from shutil import copytree


GIT_HUB_PATH = "github/LearnPythonWithRune/"


current_path:str = ""

jupyter_dir:str = ""
jupyter_final:str = ""
jupyter_starter:str = ""

colab_dir:str = ""
colab_final:str = ""
colab_starter:str = ""

notebooks:list[str] = []

def fill_paths(folder:str):
    global current_path, jupyter_dir, jupyter_final, jupyter_starter, colab_dir, colab_final, colab_starter
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
        # copy_folders(folders)
        pass
    if len(other_files) > 0:
        copy_files(other_files)


def get_inside(folder:str):
    folder_content =  [folder+'/'+elt for elt in listdir(folder)]
    folders = [d for d in folder_content if isdir(d)]
    # notebooks = [f_ntbk for f_ntbk in folder_content if isfile(f_ntbk) and f_ntbk[-6:] == '.ipynb' ]
    notebooks = [f_ntbk for f_ntbk in folder_content if isfile(f_ntbk) and splitext(f_ntbk)[1] == '.ipynb' ]
    # other_files = [f for f in folder_content if isfile(f) and f[-6:] != '.ipynb' ]
    other_files = [f for f in folder_content if isfile(f) and splitext(f)[1] != '.ipynb' ]

    return folder_content, folders, notebooks, other_files


def create_folders():
    try:
        makedirs(jupyter_starter)
        makedirs(jupyter_final)
        makedirs(colab_starter)
        makedirs(colab_final)
    except:
        pass


def gen_content(folder:str) -> bool:
    global notebooks
    folder_content, folders, notebooks, other_files = get_inside(folder)
    if len(notebooks) > 0:
        create_folders()
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
    colab_base_link = 'https://colab.research.google.com/'
    full_main_from_colab = colab_base_link + GIT_HUB_PATH
    full_repo = full_main_from_colab + basename(current_path)
    sub_repo_and_filenane = "/".join(notebook.split(os.sep)[-3:])
    full_link = full_repo + '/blob/main/' + sub_repo_and_filenane

    # full_href_link = '"' + colab_base_link + GIT_HUB_PATH + basename(current_path) + '/blob/main/' + basename(notebook) +'"'
    full_href_link = '"' + full_link +'"'

    # filename = full_github_path + '/' + notebook
    # print(filename)
    name_file = '<a \n href=' + full_href_link + '\n'
    target = 'target="_parent">' + '\n'

    colab_img_link = '"' + colab_base_link + 'assets/colab-badge.svg' + '"'
    image = '<img \n src=' + colab_img_link + '\n' + 'alt="Open In Colab"/>'
    text_in_markup_cell = name_file + ' ' + target + image + '\n' + '</a>'
    cells = []

    nb = nbf.v4.new_notebook()
    
    cell_link = nbf.v4.new_markdown_cell(text_in_markup_cell)
    cells.append(cell_link)
    # nb["cells"] = cells
# New added
    ntbk = nbf.read(notebook, nbf.NO_CONVERT)
    all_cells = cells + ntbk.cells
    nb['cells'] = all_cells
# end new added
    nbf.write(nb, notebook, version=nbf.NO_CONVERT)
    # ntbk_name = basename(notebook)
    # with open(ntbk_name, 'w') as f:
    #     nbf.write(nb, f)


def clean_notebooks():
    for notebook in notebooks:

        jupyt_strt:str = join(jupyter_starter, basename(notebook))
        clear_code(jupyt_strt)

        colb_strt:str = join(colab_starter, basename(notebook))
        clear_code(colb_strt)
        add_header_colab(colb_strt)

        colb_finl:str = join(colab_final, basename(notebook))
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