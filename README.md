# ChatRAGify

---
ChatRAGify 是一個專案，專注於實現 RAG（Retrieval-Augmented Generation）相關功能，並整合資料庫、檔案管理、以及對話生成的能力。

## 專案目錄結構

---

```plaintext
ChatRAGify/
├── .venv/                 # 虛擬環境
├── chat/                  # 聊天相關功能的模組
├── ChatRAGify/            # 主專案目錄
├── DB/                    # 資料庫相關配置與初始化
│   ├── init.sql           # 資料庫初始化 SQL 腳本
│   └── docker-compose.yml # 資料庫的 Docker Compose 配置
├── ollama/                # Ollama 模組相關配置
│   └── docker-compose.yml # Ollama 的 Docker Compose 配置
├── templates/             # 前端模板檔案
├── transport/             # 資料傳輸相關功能模組
├── vector_query/          # 向量查詢相關功能模組
├── manage.py              # Django 管理腳本
├── testinfo.md            # 轉換後md資料
└── testinfo.png           # 測試原始文件
```

## 功能介紹

---

### 1. Chat 模組

- 負責實現聊天功能，包括與外部服務整合的 API。
- 提供互動式對話生成。

### 2. DB 資料庫模組

- 使用 init.sql 進行資料庫初始化。
- 支援以 Docker Compose 部署資料庫環境。

### 3. Ollama 模組

- 用於整合與模型相關的外部服務。
- 以 Docker Compose 配置執行環境。

### 4. Transport 模組

- 用於處理資料傳輸相關邏輯。
- 支援多種協議和傳輸方式。

### 5. Vector Query 模組

- 提供向量化查詢的功能。
- 適用於文件檢索和語意相關的應用場景。

## 安裝與使用

---

### 1. 環境準備

- 確保安裝以下必要工具：
- Python 3.9+
- Docker & Docker Compose
- Virtualenv

### 2. 設置虛擬環境

```
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

```pip install -r requirements.txt```

### 3. 啟動資料庫與服務

- 啟動資料庫

```
cd DB
docker-compose up -d
```

- 啟動 Ollama 服務

```
cd ollama
docker-compose up -d
```
注意需要進入 ollama 容器，安裝llama3.2的模型
```
docker exec -it ollama bash
ollama run llama3.2
```

### 4. 啟動開發伺服器

運行 Django 開發伺服器

```python manage.py runserver```

## License

---
此專案採用 MIT 授權條款。



