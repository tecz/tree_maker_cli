import argparse
import os
from tree_maker.tree import generate_tree

def main():
  parser = argparse.ArgumentParser(description='Generate a tree structure of a folder.')
  parser.add_argument('folder_path', metavar='folder_path', type=str, nargs='?', default='.', help='Path to the folder for generating the tree structure (default: current folder)')
  parser.add_argument('--depth', type=int, help='Maximum depth of the tree structure (default: unlimited)')
  parser.add_argument('--exclude', nargs='*', default=[], help='Additional files to exclude from the tree structure')
  parser.add_argument('--show-hidden', action='store_true', help='Show hidden files in the tree structure')
  parser.add_argument('--output', '-o', type=str, help='Output file path')
  parser.add_argument('--clipboard', '-c', action='store_true', help='Copy the tree to the clipboard')

  args = parser.parse_args()

  folder_path = args.folder_path
  depth = args.depth
  excluded_files = args.exclude
  show_hidden = args.show_hidden

  tree_structure = generate_tree(folder_path, depth, show_hidden, excluded_files=excluded_files)
  root_folder_name = os.path.basename(os.path.abspath(folder_path))

  output = f"{root_folder_name}\n{tree_structure}"

  if args.output:
    with open(args.output, 'w') as file:
      file.write(output)
    print(f"Tree saved to {args.output}")
  elif args.clipboard:
    try:
      import pyperclip
      pyperclip.copy(output)
      print("Tree copied to the clipboard")
    except Exception as e:
      print(f"Error copying tree to clipboard: {e}")
  else:
    print(output)

if __name__ == '__main__':
  main()
