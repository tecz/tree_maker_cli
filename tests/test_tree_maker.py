import os
import pytest
from tree_maker import generate_tree

def test_generate_tree(tmpdir):
    subdir1 = tmpdir.mkdir('subdir1')
    subsubdir1 = subdir1.mkdir('subsubdir1')
    subdir2 = tmpdir.mkdir('subdir2')
    tmpdir.join('file1.txt').write('Test file 1')
    subdir1.join('file2.txt').write('Test file 2')

    expected_output = f"├── subdir1/\n│   ├── subsubdir1/\n│   └── file2.txt\n├── subdir2/\n├── file1.txt\n"
    assert generate_tree(tmpdir, depth=None, show_hidden=False) == expected_output

def test_generate_tree_with_depth(tmpdir):
    subdir1 = tmpdir.mkdir('subdir1')
    subsubdir1 = subdir1.mkdir('subsubdir1')
    tmpdir.join('file1.txt').write('Test file 1')

    expected_output = f"├── subdir1/\n│   └── subsubdir1/\n├── file1.txt\n"
    assert generate_tree(tmpdir, depth=1, show_hidden=False) == expected_output

def test_hidden_files(tmpdir):
    tmpdir.join('.hiddenfile').write('This is a hidden file')
    tmpdir.mkdir('.hiddendir')
    expected_output_hidden = f"├── .hiddendir/\n├── .hiddenfile\n"
    expected_output_not_hidden = ""
    assert generate_tree(tmpdir, depth=None, show_hidden=True) == expected_output_hidden
    assert generate_tree(tmpdir, depth=None, show_hidden=False) == expected_output_not_hidden

def test_excluded_items(tmpdir):
    tmpdir.join('file_to_exclude.txt').write('This file should be excluded')
    tmpdir.mkdir('dir_to_exclude')
    expected_output = f"├── dir_to_exclude/\n"
    assert generate_tree(tmpdir, depth=None, show_hidden=False, excluded_files=['file_to_exclude.txt']) == expected_output

def test_depth_limitations(tmpdir):
    subdir = tmpdir.mkdir('subdir')
    subsubdir = subdir.mkdir('subsubdir')
    subsubdir.mkdir('subsubsubdir')
    expected_output_depth_2 = f"├── subdir/\n│   └── subsubdir/\n│       └── subsubsubdir/\n"
    assert generate_tree(tmpdir, depth=2, show_hidden=False) == expected_output_depth_2

def test_large_directory_structure(tmpdir):
    for i in range(100):
        tmpdir.join(f'file{i}.txt').write(f'Content of file {i}')
    expected_start = f"├── file0.txt\n├── file1.txt\n"
    output = generate_tree(tmpdir, depth=1, show_hidden=False)
    assert output.startswith(expected_start)

def test_empty_directory(tmpdir):
    tmpdir.mkdir('emptydir')
    expected_output = f"├── emptydir/\n"
    assert generate_tree(tmpdir, depth=None, show_hidden=False) == expected_output

def test_special_characters_in_names(tmpdir):
    tmpdir.join('file_名.txt').write('Content with special characters')
    tmpdir.mkdir('dir_名')
    expected_output = f"├── dir_名/\n├── file_名.txt\n"
    assert generate_tree(tmpdir, depth=None, show_hidden=False) == expected_output