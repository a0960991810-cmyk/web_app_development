import sqlite3
import os

def get_db_connection():
    """
    建立 sqlite3 資料庫連線並回傳
    路徑對應 instance/database.db
    設定 row_factory 讓查詢結果能以字典形式 (欄位名稱) 存取
    """
    # task.py 位於 app/models 內，故需要退回兩層來到根目錄，再進入 instance
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'instance', 'database.db'))
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

class Task:
    @classmethod
    def create(cls, title, due_date=None):
        """
        新增一筆工作紀錄。
        
        :param title: 任務標題 (字串)
        :param due_date: 預期完成日 (字串或 None)
        :return: 成功時回傳新紀錄的 id，失敗時回傳 None
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO tasks (title, due_date) VALUES (?, ?)',
                    (title, due_date)
                )
                conn.commit()
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Database error in create: {e}")
            return None

    @classmethod
    def get_all(cls, status_filter=None):
        """
        取得所有紀錄。
        
        :param status_filter: 狀態篩選，可為 'completed' (已完成) 或 'pending' (未完成)，預設 None (全取)
        :return: 回傳 sqlite3.Row 的列表。若失敗回傳空陣列 []
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                if status_filter == 'completed':
                    cursor.execute('SELECT * FROM tasks WHERE is_completed = 1 ORDER BY created_at DESC')
                elif status_filter == 'pending':
                    cursor.execute('SELECT * FROM tasks WHERE is_completed = 0 ORDER BY created_at DESC')
                else:
                    cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')
                return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Database error in get_all: {e}")
            return []

    @classmethod
    def get_by_id(cls, task_id):
        """
        取得單筆特定紀錄。
        
        :param task_id: 欲查詢的任務 ID
        :return: 回傳一個 sqlite3.Row，若無資料或發生錯誤則回傳 None
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
                return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Database error in get_by_id: {e}")
            return None

    @classmethod
    def update(cls, task_id, title, due_date):
        """
        更新特定記錄內容 (標題、日期)。
        
        :param task_id: 要更新的任務 ID
        :param title: 新的任務標題
        :param due_date: 新的預期完成日
        :return: 更新成功時回傳 True，若失敗或影響行數為 0 回傳 False
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'UPDATE tasks SET title = ?, due_date = ? WHERE id = ?',
                    (title, due_date, task_id)
                )
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error in update: {e}")
            return False

    @classmethod
    def delete(cls, task_id):
        """
        刪除指定紀錄。
        
        :param task_id: 要刪除的任務 ID
        :return: 成功回傳 True，發生錯誤或行數為 0 回傳 False
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error in delete: {e}")
            return False

    @classmethod
    def toggle_status(cls, task_id):
        """
        切換任務的狀態 (已完成/未完成自動互換)。
        
        :param task_id: 要切換狀態的任務 ID
        :return: 成功切換回傳 True，失敗回傳 False
        """
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'UPDATE tasks SET is_completed = CASE WHEN is_completed = 1 THEN 0 ELSE 1 END WHERE id = ?',
                    (task_id,)
                )
                conn.commit()
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Database error in toggle_status: {e}")
            return False
