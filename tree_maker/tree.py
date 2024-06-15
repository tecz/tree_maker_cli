import os
from .utils import is_hidden
from .config import DEFAULT_EXCLUDED_FILES

def generate_tree(folder, depth, show_hidden, prefix='', excluded_files=None):
  if excluded_files is None:
    excluded_files = []

  excluded_files.extend(DEFAULT_EXCLUDED_FILES)

  folders = []
  files = []

  for item in os.listdir(folder):
    if item in excluded_files or (not show_hidden and is_hidden(item)):
      continue

    if os.path.isdir(os.path.join(folder, item)):
      folders.append(item)
    else:
      files.append(item)

  folders.sort()
  files.sort()

  tree = ''
  total_items = folders + files  # Combine folders and files for unified indexing

  for index, item in enumerate(total_items):
    is_last = (index == len(total_items) - 1)  # Check if the item is the last in the combined list

    if prefix == '':
      if is_last:
        tree += '└── '
        new_prefix = '    '  # Adjust the prefix for the last item
      else:
        tree += '├── '
        new_prefix = '│   '
    else:
      if is_last:
        tree += prefix + '└── '
        new_prefix = prefix + '    '  # Adjust the prefix for the last item
      else:
        tree += prefix + '├── '
        new_prefix = prefix + '│   '

    if os.path.isdir(os.path.join(folder, item)):
      tree += item + '/\n'
      if depth is None or depth > 0:
        tree += generate_tree(os.path.join(folder, item), depth - 1 if depth is not None else None, show_hidden, new_prefix, excluded_files)
    else:
      tree += item + '\n'

  return tree
