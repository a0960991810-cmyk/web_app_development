# 路由設計文件 (ROUTES) - 工作管理系統

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **工作清單主頁** | GET | `/` | `index.html` | 顯示所有任務，支援參數 `?status=` 過濾 |
| **行事曆視圖** | GET | `/calendar` | `calendar.html` | 行事曆模式顯示每日待辦事項 |
| **新增工作** | POST | `/add` | — | 接收並寫入新工作，重導向至 `/` |
| **編輯工作** | POST | `/edit/<int:task_id>` | — | 更新指定任務內容，重導向至 `/` |
| **切換完成狀態** | POST | `/toggle/<int:task_id>` | — | 標記未完成/已完成切換，重導向至 `/` |
| **刪除工作** | POST | `/delete/<int:task_id>` | — | 刪除指定任務，重導向至 `/` |

## 2. 每個路由的詳細說明

### 2.1 工作清單主頁
- **路由**: `GET /`
- **輸入**: URL Parameter `status` (選填，例如 `completed` 或 `pending`)。
- **處理邏輯**: 呼叫 `Task.get_all(conn, status_filter=status)` 根據篩選條件取得資料清單。
- **輸出**: 渲染 `index.html`。
- **錯誤處理**: 無。若傳入無效的狀態篩選字串，預設視同無篩選。

### 2.2 行事曆視圖
- **路由**: `GET /calendar`
- **輸入**: 無。
- **處理邏輯**: 呼叫 `Task.get_all(conn)`，因行事曆通常需讀取全局資料來分派日期。
- **輸出**: 渲染 `calendar.html`。
- **錯誤處理**: 無。

### 2.3 新增工作
- **路由**: `POST /add`
- **輸入**: HTML Form 表單提交，包含 `title` (文字，必填) 與 `due_date` (日期，選填)。
- **處理邏輯**: 呼叫 `Task.create(conn, title, due_date)`。
- **輸出**: 執行完成後 HTTP 302 Redirect 至首頁 `/`。
- **錯誤處理**: 若 `title` 為空或不符規則，回傳 400 Bad Request，或建立 flash 錯誤訊息後重新渲染表單頁面。

### 2.4 編輯工作
- **路由**: `POST /edit/<int:task_id>`
- **輸入**: 
  - URL 路徑參數: `task_id` (任務 ID)
  - HTML Form: `title` (必填) 與 `due_date` (選填)。
- **處理邏輯**: 呼叫 `Task.update(conn, task_id, title, due_date)` 進行更新。
- **輸出**: 執行完成後 HTTP 302 Redirect 至首頁 `/`。
- **錯誤處理**: 若 ID 不存在於資料庫返回 404 Not Found，標題為空則返回 400。

### 2.5 切換完成狀態
- **路由**: `POST /toggle/<int:task_id>`
- **輸入**: URL 路徑參數 `task_id`。
- **處理邏輯**: 呼叫 `Task.toggle_status(conn, task_id)` 將原本的完成狀態反轉。
- **輸出**: 執行完成後 HTTP 302 Redirect 至首頁 `/`。
- **錯誤處理**: 若專案 ID 不存在則回傳 404 Not Found。

### 2.6 刪除工作
- **路由**: `POST /delete/<int:task_id>`
- **輸入**: URL 路徑參數 `task_id`。
- **處理邏輯**: 呼叫 `Task.delete(conn, task_id)` 刪除對應的資料庫記錄。
- **輸出**: 執行完成後 HTTP 302 Redirect 至首頁 `/`。
- **錯誤處理**: 若專案 ID 不存在則回傳 404 Not Found。

## 3. Jinja2 模板清單

所有的模板檔案會放在 `app/templates/` 中。以下是系統將使用的模板架構：

1. **`base.html`**
   - 作為全站的根模板 (Base Template)。
   - 包含通用的 HTML 結構（如 `<head>`）、全局導覽列 (Navbar)，並保留 `{% block content %}{% endblock %}` 供子模板插入各自的邏輯片段。
   
2. **`index.html`**
   - 繼承自 `base.html`。
   - 包含新增工作表單區域、工作清單顯示與篩選器。每個任務項目附帶更新、刪除及狀態切換按鈕。
   
3. **`calendar.html`**
   - 繼承自 `base.html`。
   - 以月曆的網格方式檢視所有含有到期日的工作安排。

## 4. 路由骨架程式碼

路由骨架將儲存在 `app/routes/tasks.py` 之中。由於架構較為輕量，將集中使用 Flask Blueprint 封裝所有與工作任務有關的邏輯，方便後續在主程式掛載。
