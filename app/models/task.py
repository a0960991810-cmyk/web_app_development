import sqlite3

class Task:
    def __init__(self, id, title, due_date, is_completed, created_at):
        self.id = id
        self.title = title
        self.due_date = due_date
        self.is_completed = bool(is_completed)
        self.created_at = created_at

    @staticmethod
    def _row_to_obj(row):
        return Task(
            id=row['id'],
            title=row['title'],
            due_date=row['due_date'],
            is_completed=row['is_completed'],
            created_at=row['created_at']
        )

    @classmethod
    def create(cls, conn, title, due_date=None):
        """新增一筆工作任務"""
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO tasks (title, due_date) VALUES (?, ?)',
            (title, due_date)
        )
        conn.commit()
        return cursor.lastrowid

    @classmethod
    def get_all(cls, conn, status_filter=None):
        """取得所有任務，可依狀態進行過濾"""
        cursor = conn.cursor()
        if status_filter == 'completed':
            cursor.execute('SELECT * FROM tasks WHERE is_completed = 1 ORDER BY created_at DESC')
        elif status_filter == 'pending':
            cursor.execute('SELECT * FROM tasks WHERE is_completed = 0 ORDER BY created_at DESC')
        else:
            cursor.execute('SELECT * FROM tasks ORDER BY created_at DESC')
            
        rows = cursor.fetchall()
        return [cls._row_to_obj(row) for row in rows]

    @classmethod
    def get_by_id(cls, conn, task_id):
        """根據 ID 取得單一任務"""
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
        row = cursor.fetchone()
        if row:
            return cls._row_to_obj(row)
        return None

    @classmethod
    def update(cls, conn, task_id, title, due_date):
        """更新工作任務的標題與日期"""
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE tasks SET title = ?, due_date = ? WHERE id = ?',
            (title, due_date, task_id)
        )
        conn.commit()
        return cursor.rowcount > 0

    @classmethod
    def delete(cls, conn, task_id):
        """刪除指定的工作任務"""
        cursor = conn.cursor()
        cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        return cursor.rowcount > 0

    @classmethod
    def toggle_status(cls, conn, task_id):
        """切換工作的完成狀態"""
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE tasks SET is_completed = CASE WHEN is_completed = 1 THEN 0 ELSE 1 END WHERE id = ?',
            (task_id,)
        )
        conn.commit()
        return cursor.rowcount > 0
