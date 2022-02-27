import nbformat as nbf
from os.path import basename
from os import getcwd


GIT_HUB_PATH = "github/LearnPythonWithRune/"


def add_header_colab(notebook):
    colab_base_link = 'https://colab.research.google.com/'

    full_href_link = '"' + colab_base_link + GIT_HUB_PATH + basename(getcwd()) + '"'

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
    # ntbk_new = [cell for cell in ntbk.cells ]
    # cells.append(ntbk.cells)
    all_cells = cells + ntbk.cells
    nb['cells'] = all_cells
# end new added
    # ntbk_name = basename(notebook)
    ntbk_name = basename(notebook)


    with open(ntbk_name, 'w') as f:
        nbf.write(nb, f)

    #     ntbk = nbf.read(notebook, nbf.NO_CONVERT)

#     # code = ""
# # %pylab inline
# # hist(normal(size=2000), bins=50);"""
#     # cells = [nbf.v4.new_markdown_cell(text), nbf.v4.new_code_cell(code)]
#     cell_link = nbf.v4.new_markdown_cell(text_in_markub_cell)
#     ntbk['cells'].extend(text_in_markub_cell)
#     nbf.write(ntbk, 'eda_new.ipynb')


add_header_colab('test1.ipynb')