# 流程圖與路徑設計 (Flowchart) - 工作管理系統

## 1. 使用者流程圖（User Flow）

這張圖展示了使用者進入系統後，所有可能的操作與路線：

```mermaid
flowchart LR
    A([使用者開啟系統網頁]) --> B(主畫面：工作清單)
    
    B --> C{選擇檢視或操作？}
    
    %% 檢視與篩選
    C -->|切換視圖| D[行事曆視圖]
    C -->|依狀態篩選| E[已過濾的工作清單<br/>全部/未完成/已完成]
    D -.->|返回| B
    E -.->|清除篩選| B

    %% 新增、修改、刪除與狀態切換
    C -->|新增| F[填寫新增工作表單並送出]
    C -->|編輯| G[點擊編輯，修改內容並送出]
    C -->|切換狀態| H[點擊勾選或取消勾選完成狀態]
    C -->|刪除| I[點擊刪除按鈕]
    
    F --> J([重新導向/更新畫面])
    G --> J
    H --> J
    I --> J
    
    J -.-> B
```

## 2. 系統序列圖（Sequence Diagram）

這張圖透過「新增工作」的範例，說明了前、後端與資料庫之間是如何互動。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器 (HTML/JS)
    participant Flask as Flask (後端)
    participant DB as SQLite (資料庫)
    
    %% 使用者觸發
    User->>Browser: 填寫「新增任務」欄位並點擊送出
    
    %% 發送請求
    Browser->>Flask: POST /add-task (包含標題、日期等資料)
    
    %% 後端處理與資料庫互動
    Flask->>Flask: 驗證接收到的資料
    Flask->>DB: INSERT INTO tasks (寫入新資料)
    DB-->>Flask: 寫入成功
    
    %% 重新導向與渲染畫面
    Flask-->>Browser: Redirect (302) 回到主畫面路徑 /
    Browser->>Flask: GET / (請求取得主畫面)
    Flask->>DB: SELECT * FROM tasks (撈取最新任務)
    DB-->>Flask: 回傳所有任務資料
    Flask->>Flask: 使用 Jinja2 組合資料與 HTML 模板
    Flask-->>Browser: 回傳已渲染的首頁 HTML
    
    %% 介面顯示
    Browser->>User: 顯示已更新的任務清單
```

## 3. 功能清單對照表

以下整理了系統中所有主要功能的存取路徑，對應的 HTTP 方法，以及該行為執行的目的。這個對照表有助於接下來建立 Flask 的路由。

| 功能項目 | 路徑 (URL Endpoint) | HTTP 請求方法 | 說明 |
| --- | --- | --- | --- |
| **首頁/目前清單** | `/` | `GET` | 顯示所有或根據 GET 參數（如 `?status=done`）篩選過的工作清單 |
| **行事曆視圖** | `/calendar` | `GET` | 顯示行事曆介面的工作排程 |
| **新增工作** | `/add` | `POST` | 接收表單提交資料建立新工作，完成後重導向回首頁 |
| **編輯工作** | `/edit/<task_id>` | `POST` | 接收表單提交資料更新指定工作，完成後重導向回首頁 |
| **切換完成狀態** | `/toggle/<task_id>` | `POST` | 將指定任務切換為「完成」或「未完成」，完成後重導向回首頁 |
| **刪除工作** | `/delete/<task_id>` | `POST` | 刪除與 URL 參數對應的指定任務，完成後重導向回首頁 |

> 註：在不依賴進階前端框架下（全後端渲染），編輯、切換狀態及刪除皆建議使用 `POST` 方法搭配網頁表單發送，可避免瀏覽器對 HTTP PUT 或 DELETE 方法支援程度的問題。
