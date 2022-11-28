# sd_katanuki
Anime Image Background Remover for AUTOMATIC1111


## Include anime-segmentation

以下のリポジトリの内容を改変したものが含まれています。

- https://github.com/SkyTNT/anime-segmentation
- https://huggingface.co/skytnt/anime-seg

git submoduleは1111のExtensionインストーラーが対応していなかった。
1111kのinstall.pyは経過をリアルタイム表示できないので好きくない。
改変はモジュールを相対パスで読み込むように直したのと、
型抜きに不要な大きいファイルを削除しただけ。
