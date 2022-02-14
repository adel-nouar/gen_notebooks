from genericpath import isfile
import sys
import nbformat as nbf
from os.path import isdir
from os import listdir


def clear_code(notebook):
    ntbk = nbf.read(notebook, nbf.NO_CONVERT)
    new_ntbk = ntbk
    new_ntbk.cells = [cell if cell.cell_type == "markdown" else nbf.v4.new_code_cell() for cell in ntbk.cells ]
    nbf.write(new_ntbk, notebook, version=nbf.NO_CONVERT)

def gen_jupyter(folder_content):
    pass


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