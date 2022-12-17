import os
import pathlib
import urllib.request
import git

from launch import git_clone
from modules.devices import get_optimal_device

p = pathlib.Path(__file__).parts[-3:-1]

# 1. git clone
dst = os.path.join(p[0], p[1], 'anime-seg', 'isnetis.ckpt')
if not os.path.exists(dst):
    name = 'anime-seg'
    dir = f"{p[0]}/{p[1]}/{name}"
    url = 'https://huggingface.co/skytnt/anime-seg'
    git_clone(url, dir, name)

# 2. check ckpt
checked_path = os.path.join(p[0], p[1], 'isnetis.ckpt.checked')
if not os.path.exists(checked_path):
    try:
        device = get_optimal_device()
        class Opt(object):
            def __init__(self):
                self.net = 'isnet_is'
                self.ckpt = f"{p[0]}/{p[1]}/anime-seg/isnetis.ckpt"
                self.device = str(device)
        opt = Opt()

        import importlib
        train = importlib.import_module(f"{p[0]}.{p[1]}.anime-segmentation.train")
        AnimeSegmentation = getattr(train, 'AnimeSegmentation')
        model = AnimeSegmentation.try_load(opt.net, opt.ckpt, opt.device)
        pathlib.Path(checked_path).write_text('1')
    except:
# 3. direct download
        url = 'https://huggingface.co/skytnt/anime-seg/resolve/main/isnetis.ckpt'
        dst_dir = os.path.join(p[0], p[1], 'anime-seg')
        dst = dst_dir + "/isnetis.ckpt"
        pathlib.Path(dst_dir).mkdir(parents=True,exist_ok=True)
        urllib.request.urlretrieve(url, dst)
        print(f"Downloaded {url}")
