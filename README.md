# sd_katanuki
Anime Image Background Remover for AUTOMATIC1111

# Install

以下のリポジトリ(400MB弱)を別途自動ダウンロードします。

- https://huggingface.co/skytnt/anime-seg

失敗することが結構あるっぽいのでダメそうなら手動で上書きお願いします。

torch, torchvisionのインストーラーは用意していません。

# Requirement

***画像のファイル名に日本語とか入れないようにお願いします(動かないらしい)***

情報によると、以下のバージョンで動くようです。

- torch==1.12.1+cu113
- torchvision==0.13.1+cu113

私の環境では、以下のバージョンを使っています。

- torch==1.12.1+cu116
- torchvision==0.13.1+cu116

残念ながらCPUでは動作しないようです。

# Usage

- GTX 16X0の人は右上のFP32をチェック

## Alt mode

- Whiteのときに変な色になる(GとBが逆になる)場合はチェックを外してみてください
- Transparentでチェックを外すと少し計算方法が変わります

## Single

- drop Image

## Directory

例: Dreamboothのデータセット画像作るのに白背景にする作業の流れ

+ webui直下に katanuki_input と katanuki_output フォルダを作る(名前はなんでもいい)
+ フォルダの中に画像を入れる(この画像が上書きされる)
+ Background で White を選ぶ
+ Directory タブの Input Directory に katanuki_input と入れる
+ Directory タブの Output Directory に katanuki_output と入れて Run
+ 1111で確認したかったら Image Browser 入れて Others の Images directory に katanuki_output と入れる

## Include anime-segmentation

以下のリポジトリの内容を改変したものが含まれています。

- https://github.com/SkyTNT/anime-segmentation

- git submoduleは1111のExtensionインストーラーが対応していなかった。
- 1111のinstall.pyは経過をリアルタイム表示できないので好きくない。
- 改変はモジュールを相対パスで読み込むように直したのと、型抜きに不要な大きいファイルを削除しただけ。
