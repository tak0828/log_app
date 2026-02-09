# ローカル実行方法

## 前提条件

1. MySQLコンテナが起動していること
   ```bash
   docker-compose up db -d
   ```

2. 仮想環境が有効化されていること

## 実行方法

### 方法1: スクリプトを使用（推奨）

**Windows (PowerShell):**
```powershell
cd web
.\run_local.ps1
```

**Windows (コマンドプロンプト):**
```cmd
cd web
run_local.bat
```

### 方法2: 手動で環境変数を設定

**PowerShell:**
```powershell
cd web
$env:IS_DOCKER = "false"
$env:DJANGO_SETTINGS_MODULE = "config.settings"
..\venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

**コマンドプロンプト:**
```cmd
cd web
set IS_DOCKER=false
set DJANGO_SETTINGS_MODULE=config.settings
..\venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

### 方法3: VSCodeのデバッグを使用

1. F5キーを押す
2. 「Python: Django (ローカル)」を選択
3. デバッグ開始

## トラブルシューティング

### MySQLに接続できない場合

1. MySQLコンテナが起動しているか確認:
   ```bash
   docker-compose ps
   ```

2. コンテナを起動:
   ```bash
   docker-compose up db -d
   ```

3. ポート3308が使用可能か確認

### その他のエラー

- 仮想環境が有効化されているか確認
- `requirements.txt`のパッケージがインストールされているか確認
- マイグレーションが適用されているか確認: `python manage.py migrate`

