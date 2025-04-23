# OBS設定ガイド

このアプリケーションを使用するには、OBSに「OSC for OBS」プラグインをインストールし、適切に設定する必要があります。

## 必要条件

1. OBS Studio（バージョン28以上推奨）
2. [OSC for OBS](https://github.com/jshea2/OSC-for-OBS/releases) プラグイン

## インストール手順

1. [OSC for OBS](https://github.com/jshea2/OSC-for-OBS/releases) の最新バージョンをダウンロードします。
2. ダウンロードしたアプリケーションを適切なフォルダに配置します：
   - Mac: アプリケーションフォルダ
   - Windows: Cドライブなどのルートフォルダ

## OSC for OBSの設定

1. OSC for OBSを起動します。
2. 以下の設定を行います：
   - OSC IN:
     - IP: 127.0.0.1
     - Port: 3333（カット番号管理システムのデフォルトポート）
   - 「Connect」ボタンをクリックして接続します。
3. OSC for OBSのコンソールタブを開き、接続が成功したことを確認します。
   - 「Successfully connected to OBS」というメッセージが表示されるはずです。

## 正しいOSCコマンド

OSC for OBSで使用する主なコマンドは以下の通りです：

- `/startRecording` - 録画を開始します
- `/stopRecording` - 録画を停止します
- `/recFileName [filename]` - 録画ファイル名を設定します

## ファイル名設定機能を使用するための設定

カスタムファイル名を使用するには、以下の点を確認してください：

1. OSC for OBSが正常に接続されていることを確認します。
2. OBSの録画設定で、「ファイル名の形式」や「ファイル名のテンプレート」などの設定がある場合は、カスタム設定を使用しないようにします。
3. カット番号管理システムを起動し、録画を開始する前に必要な情報（パート名、シーン名など）を入力します。
4. OSC for OBSのコンソールタブで、送信されたコマンドが正しく受信されていることを確認します。

## トラブルシューティング

ファイル名が正しく設定されない場合：

1. OSC for OBSが正常に接続されていることを確認します。
   - OSC for OBSのコンソールタブで「Successfully connected to OBS」というメッセージが表示されているか確認します。
2. OSC for OBSのコンソールタブでエラーメッセージがないか確認します。
   - 「Invalid OSC command」というエラーが表示される場合は、コマンドが間違っている可能性があります。
   - 「Not connected」というエラーが表示される場合は、OSC for OBSがOBSに接続されていない可能性があります。
3. カット番号管理システムとOSC for OBSの両方を再起動してみてください。
4. OBSの録画設定で、ファイル名の形式が上書きされていないか確認します。

## OSC for OBSのテスト方法

OSC for OBSには「OSC Tester」機能があります：

1. OSC for OBSを起動します。
2. メニューから「File」>「OSC Tester」を選択します。
3. 以下のコマンドをテストしてみてください：
   - `/startRecording`
   - `/stopRecording`
   - `/recFileName "テストファイル名"`

## 参考情報

- [OSC for OBS GitHub](https://github.com/jshea2/OSC-for-OBS)
- [OBS Studio](https://obsproject.com/)
