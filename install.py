import os
import pathlib
import git

from launch import git_clone

p = pathlib.Path(__file__).parts[-3:-1]

name = 'anime-seg'
dir = f"{p[0]}/{p[1]}/{name}"
if os.path.exists(dir):
    git.cmd.Git(dir).pull()
else:
    url = 'https://huggingface.co/skytnt/anime-seg'
    git_clone(url, dir, name)
