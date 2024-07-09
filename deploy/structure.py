import os

def generate_directory_structure(root_dir, prefix=''):
    structure = ''
    order = ['data', 'preprocess', 'model', 'pages', 'deploy', 'README.md', 'requirements.txt']
    for root, dirs, files in os.walk(root_dir):
        # Sort dirs and files according to the order list
        dirs.sort(key=lambda d: order.index(d) if d in order else len(order))
        files.sort(key=lambda f: order.index(f) if f in order else len(order))
        
        level = root.replace(root_dir, '').count(os.sep)
        indent = '│   ' * level + '├──'
        sub_indent = '│   ' * (level + 1) + '├──'

        if level == 0:
            structure += f'{os.path.basename(root)}/\n'
        else:
            structure += f'{prefix}{indent} {os.path.basename(root)}/\n'

        for f in files:
            file_indent = '│   ' * (level + 1) + '├──'
            structure += f'{prefix}{file_indent} {f}\n'

        for d in dirs:
            dir_indent = '│   ' * (level + 1) + '├──'
            structure += f'{prefix}{dir_indent} {d}\n'
    return structure

# set root directory
root_directory = '/Users/xiaodi/Postgraduate/MDA/Maps/github_version/MDA_Project2024_AED_Optimization'

# generate directory structure
directory_structure = generate_directory_structure(root_directory)

# save the structure to txt
with open('deploy/directory_structure.txt', 'w') as f:
    f.write(directory_structure)
