# カット番号管理システム (Cut Numbering Manager)

アニメ制作現場でのカット番号管理を自動化するPyQt5アプリケーションです。OBSとOSC通信を行い、録画ファイルの命名規則を自動化します。

## 機能

- カット番号の自動管理
- ファイル命名規則の自動適用: `{パート名}_{シーン名}_{カット番号}_{バージョン名}`
- OBSとのOSC連携による録画制御
- バージョン管理の自動化

## 必要条件

### ソフトウェア要件
- **OBS Studio**: バージョン27.2.4
  - [ダウンロードリンク](https://github.com/obsproject/obs-studio/releases/tag/27.2.4)
- **OSC for OBS**: バージョン2.7.1
  - [ダウンロードリンク](https://github.com/jshea2/OSC-for-OBS/releases/tag/v2.7)
- **OBS WebSocket**: バージョン4.9.1（obs-websocket-4.9.1-compat-○○をダウンロード）
  - [ダウンロードリンク](https://github.com/obsproject/obs-websocket/releases/tag/5.0.1)

### Python要件
- Python 3.x
- PyQt5
- python-osc

## インストール

1. このリポジトリをクローンします
2. 必要なパッケージをインストールします:

```bash
pip install -r requirements.txt
```

## 使用方法

1. OBS Studio v27.2.4とOSC for OBS v2.7.1, OBS WebSocketをインストールします
2. アプリケーションを起動します:

```bash
python main.py
```

3. メインタブでパート名、シーン名、カット番号、バージョンを入力します
4. 設定タブでOSCの設定を確認します（デフォルト: 127.0.0.1:3333）
5. RECボタンを押して録画を開始し、STOPボタンで録画を停止します
6. 録画停止時に自動的にカット番号がインクリメントされます

## OBSの設定サンプルの使い方
動作確認のため、OBSの設定サンプルを同梱しています。
sample_videos/で設定サンプルを用いて録画したデータがご覧いただけます。

### 設定サンプル
1. OBSのメニューからプロファイル>インポートを選択
2. sample_OBS_settings/Profile_Sample_cut-numbering-managerを読み込む
3. OBSのメニューからプロファイル>Profile_Sample_cut-numbering-managerを選択

### サンプルシーン
1. OBSのメニューからシーンコレクション>インポートを選ぶ
2. sample_OBS_settings/scene-collection_cut-numbering-manager.jsonを読み込む
3. OBSのメニューからシーンコレクション>cut-numbering-managerを選択
