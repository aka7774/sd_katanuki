# sd_katanuki
Anime Image Background Remover for AUTOMATIC1111


# Usage

## Single

- drop Image

## Directory

Dreamboothのデータセット画像作るのに白背景作る作業の流れ

+ webui直下に katanuki フォルダを作る(名前はなんでもいい)
+ フォルダの中に画像を入れる(この画像が上書きされる)
+ Background で White を選ぶ
+ Directory タブの Input Directory に katanuki と入れる
+ Generate
+ 1111で確認したかったら Image Browser 入れて Others の Images directory に katanuki と入れる

## Include anime-segmentation

以下のリポジトリの内容を改変したものが含まれています。

- https://github.com/SkyTNT/anime-segmentation
- https://huggingface.co/skytnt/anime-seg

- git submoduleは1111のExtensionインストーラーが対応していなかった。
- 1111のinstall.pyは経過をリアルタイム表示できないので好きくない。
- 改変はモジュールを相対パスで読み込むように直したのと、型抜きに不要な大きいファイルを削除しただけ。
