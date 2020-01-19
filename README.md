# AutoDevKit
自動化のためのツール、スクリプトとかをまとめます.


# 対応済み

## cui_exec
- 入力が必要なCUiツールの自動化用  
- 成功したときは連鎖的にツールを実行し、  
失敗したときはコマンド実行して終了
    - このコマンドというのは失敗時のログ送信などを想定しています.

## gui_exec
- クリック、キー入力が必要なGUIツールの自動化用
- 左クリック、キー入力を設定として残しそれを使用して自動実行する
    - ESCキー入力で保存


## remo_shell
- Windowsからlinuxのshellコマンドを実行する
- AutoDevKit/remo_shell/remo_shell.tomlの [user name] [host name] [cmd] [password] を置き換える
- チェックはいるはずだけどPuTTYが必要

## notify
- ポップアップまたはバルーン通知を出す

# 未対応

## HTTPリクエスト送受信



## Webからインストーラのダウンロード



