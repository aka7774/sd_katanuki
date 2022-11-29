# sd_katanuki
Anime Image Background Remover for AUTOMATIC1111

# Install

torch, torchvisionのインストーラーは用意していません。

情報によると、以下のバージョンで動くようです。

- torch==1.12.1+cu113
- torchvision==0.13.1+cu113

以下のバージョンでは動かないようです。

- torch==1.10.2

私の環境では、以下のバージョンを使っています。

- torch==1.12.1+cu116
- torchvision==0.13.1+cu116

# Usage

- GTX 16X0の人は右上のFP32をチェック

## Single

- drop Image

## Directory

Dreamboothのデータセット画像作るのに白背景にする作業の流れ

+ webui直下に katanuki フォルダを作る(名前はなんでもいい)
+ フォルダの中に画像を入れる(この画像が上書きされる)
+ Background で White を選ぶ
+ Directory タブの Input Directory に katanuki と入れて Run
+ 1111で確認したかったら Image Browser 入れて Others の Images directory に katanuki と入れる

## Include anime-segmentation

以下のリポジトリの内容を改変したものが含まれています。

- https://github.com/SkyTNT/anime-segmentation
- https://huggingface.co/skytnt/anime-seg

- git submoduleは1111のExtensionインストーラーが対応していなかった。
- 1111のinstall.pyは経過をリアルタイム表示できないので好きくない。
- 改変はモジュールを相対パスで読み込むように直したのと、型抜きに不要な大きいファイルを削除しただけ。
