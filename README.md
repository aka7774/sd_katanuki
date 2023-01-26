# sd_katanuki
Anime Image Background Remover for AUTOMATIC1111

# Changelog

- 日本語のファイル名に対応しました(OpenCVのバグ?らしい)
- Expand Canvas機能を追加(いるのかわからんけど)
  - アス比を維持したまま画像の縦横をでかく揃えるのに使えます

# Install

以下のリポジトリ(400MB弱)を別途自動ダウンロードします。

- https://huggingface.co/skytnt/anime-seg

失敗することが結構あるっぽいのでダメそうなら手動で上書きお願いします。

# Requirement

torchは1111推奨のバージョンを使うことにします。

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
+ フォルダの中に画像を入れる
+ Background で White を選ぶ
+ Directory タブの Input Directory に katanuki_input と入れる
+ Directory タブの Output Directory に katanuki_output と入れて Run
+ 1111で確認したかったら Images Browser 入れて Others の Images directory に katanuki_output と入れる

## Include anime-segmentation

以下のリポジトリの内容を改変したものが含まれています。

- https://github.com/SkyTNT/anime-segmentation

- git submoduleは1111のExtensionインストーラーが対応していなかった。
- 1111のinstall.pyは経過をリアルタイム表示できないので好きくない。
- 改変はモジュールを相対パスで読み込むように直したのと、型抜きに不要な大きいファイルを削除しただけ。
