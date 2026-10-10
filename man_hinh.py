import hashlib
import os
import random
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk


DB_PATH = os.path.join(os.path.dirname(__file__), "app_data.db")
ADMIN_ACCESS_CODE = "ADMIN2026"


def hash_password(password: str) -> str:
    return hashlib.sha256(password.strip().encode("utf-8")).hexdigest()


def init_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL
        )
        """
    )
    cursor.execute(
        "SELECT COUNT(*) FROM users WHERE username = ?",
        ("admin",),
    )
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO users (username, password, full_name) VALUES (?, ?, ?)",
            ("admin", hash_password("admin123"), "Quản trị viên"),
        )
    conn.commit()
    conn.close()


init_database()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Smart App")
        self.geometry("1200x760")
        self.minsize(1000, 650)
        self.configure(bg="#f3f6fb")

        self.current_user = "Khách"
        self.target_number = random.randint(1, 100)
        self.guess_count = 0
        self.topic_data = {
            "Biến": {
                "content": "Biến là nơi lưu trữ dữ liệu trong Python.\n\nVí dụ:\nname = \"Alice\"\nage = 20\nprint(name, age)",
                "code": "name = \"Alice\"\nage = 20\nprint(name, age)",
            },
            "Vòng lặp": {
                "content": "Vòng lặp giúp lặp lại công việc nhiều lần.\n\nfor i in range(3):\n    print(i)",
                "code": "for i in range(3):\n    print(i)",
            },
            "Hàm": {
                "content": "Hàm giúp tách logic thành các khối code dễ dùng lại.\n\nVí dụ:\ndef xin_chao():\n    print(\"Xin chào!\")",
                "code": "def xin_chao():\n    print(\"Xin chào!\")\n\nxin_chao()",
            },
            "List": {
                "content": "List là kiểu dữ liệu chứa nhiều phần tử.\n\nfruits = ['Táo', 'Cam', 'Nho']\nprint(fruits[0])",
                "code": "fruits = ['Táo', 'Cam', 'Nho']\nprint(fruits[0])",
            },
        }

        self.setup_style()

        self.container = tk.Frame(self, bg="#f3f6fb")
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        self.frames = {}
        self.current_role = "user"
        self.create_login_screen()
        self.create_register_screen()
        self.create_admin_screen()
        self.create_home_screen()
        self.create_game_screen()
        self.create_sales_screen()
        self.create_learning_screen()

        self.show_screen("login")

    def setup_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Primary.TButton", background="#2563eb", foreground="#ffffff", font=("Arial", 10, "bold"), padding=(18, 10))
        style.map("Primary.TButton", background=[("active", "#1d4ed8")])
        style.configure("Secondary.TButton", background="#e2e8f0", foreground="#0f172a", font=("Arial", 10, "bold"), padding=(18, 10))
        style.configure("Card.TFrame", background="#ffffff")

    def create_login_screen(self):
        frame = tk.Frame(self.container, bg="#eef4ff")
        self.frames["login"] = frame

        left = tk.Frame(frame, bg="#1d4ed8", padx=40, pady=40)
        left.place(relx=0, rely=0, relwidth=0.5, relheight=1)

        logo = tk.Label(left, text="🚀", font=("Arial", 54), bg="#1d4ed8")
        logo.pack(pady=(20, 10))

        title = tk.Label(left, text="Smart App", font=("Arial", 34, "bold"), fg="white", bg="#1d4ed8")
        title.pack()

        subtitle = tk.Label(
            left,
            text="Nền tảng quản lý, học tập và giải trí",
            font=("Arial", 13),
            fg="#dbeafe",
            bg="#1d4ed8",
            wraplength=320,
            justify="center",
        )
        subtitle.pack(pady=20)

        info = tk.Label(
            left,
            text="✅ Đăng nhập bảo mật\n✅ Giao diện hiện đại\n✅ Học Python hiệu quả",
            font=("Arial", 12),
            fg="white",
            bg="#1d4ed8",
            justify="left",
            anchor="w",
        )
        info.pack(pady=20, padx=20, anchor="w")

        right = tk.Frame(frame, bg="#ffffff")
        right.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

        form = tk.Frame(right, bg="#ffffff", padx=40, pady=50)
        form.pack(expand=True)

        tk.Label(form, text="Đăng nhập", font=("Arial", 28, "bold"), bg="#ffffff", fg="#0f172a").pack(pady=(0, 25))

        tk.Label(form, text="Tên đăng nhập", bg="#ffffff", font=("Arial", 11, "bold"), anchor="w").pack(fill="x")
        self.username_entry = ttk.Entry(form, width=30, font=("Arial", 11))
        self.username_entry.pack(fill="x", pady=(6, 18))

        tk.Label(form, text="Mật khẩu", bg="#ffffff", font=("Arial", 11, "bold"), anchor="w").pack(fill="x")
        self.password_entry = ttk.Entry(form, width=30, show="*", font=("Arial", 11))
        self.password_entry.pack(fill="x", pady=(6, 18))

        tk.Label(form, text="Mã admin", bg="#ffffff", font=("Arial", 11, "bold"), anchor="w").pack(fill="x")
        self.admin_code_entry = ttk.Entry(form, width=30, show="*", font=("Arial", 11))
        self.admin_code_entry.pack(fill="x", pady=(6, 22))

        ttk.Button(form, text="Đăng nhập", style="Primary.TButton", command=self.login).pack(fill="x")
        ttk.Button(form, text="Đăng ký tài khoản mới", style="Secondary.TButton", command=lambda: self.show_screen("register")).pack(fill="x", pady=(10, 0))
        ttk.Button(form, text="Thoát", style="Secondary.TButton", command=self.destroy).pack(fill="x", pady=(10, 0))

    def fill_demo_login(self):
        self.admin_code_entry.delete(0, tk.END)
        self.admin_code_entry.insert(0, ADMIN_ACCESS_CODE)

    def create_register_screen(self):
        frame = tk.Frame(self.container, bg="#f8fafc")
        self.frames["register"] = frame

        panel = tk.Frame(frame, bg="#ffffff", padx=35, pady=35)
        panel.pack(expand=True, padx=220, pady=80)

        tk.Label(panel, text="Đăng ký tài khoản", font=("Arial", 28, "bold"), bg="#ffffff", fg="#0f172a").pack(pady=(0, 20))

        fields = [
            ("Họ và tên", "full_name"),
            ("Tên đăng nhập", "register_username"),
            ("Mật khẩu", "register_password"),
            ("Xác nhận mật khẩu", "confirm_password"),
        ]

        self.register_entries = {}

        for label_text, key in fields:
            tk.Label(panel, text=label_text, bg="#ffffff", font=("Arial", 11, "bold"), anchor="w").pack(fill="x", pady=(12, 5))
            entry = ttk.Entry(panel, width=35, font=("Arial", 11))
            if "password" in key:
                entry.configure(show="*")
            entry.pack(fill="x")
            self.register_entries[key] = entry

        ttk.Button(panel, text="Đăng ký", style="Primary.TButton", command=self.register_account).pack(fill="x", pady=(18, 10))
        ttk.Button(panel, text="Quay lại đăng nhập", style="Secondary.TButton", command=lambda: self.show_screen("login")).pack(fill="x")

    def create_admin_screen(self):
        frame = tk.Frame(self.container, bg="#0f172a")
        self.frames["admin"] = frame

        top = tk.Frame(frame, bg="#111827", padx=24, pady=18)
        top.pack(fill="x")
        tk.Label(top, text="🛡️ Trang quản trị Admin", font=("Arial", 26, "bold"), bg="#111827", fg="white").pack(anchor="w")
        self.admin_title_var = tk.StringVar(value="Xin chào, Quản trị viên!")
        tk.Label(top, textvariable=self.admin_title_var, font=("Arial", 14), bg="#111827", fg="#93c5fd").pack(anchor="w", pady=(8, 0))
        tk.Button(top, text="Đăng xuất", bg="#ef4444", fg="white", font=("Arial", 10, "bold"), bd=0, width=12, command=self.logout).pack(anchor="e", pady=(10, 0))

        content = tk.Frame(frame, bg="#0f172a", padx=20, pady=20)
        content.pack(fill="both", expand=True)

        summary = tk.Frame(content, bg="#111827", padx=20, pady=20)
        summary.pack(fill="x")

        self.admin_stat_values = []
        for title, value, color in [
            ("Tổng tài khoản", "0", "#60a5fa"),
            ("Tổng người dùng", "0", "#34d399"),
            ("Trạng thái", "Hoạt động", "#fbbf24"),
        ]:
            card = tk.Frame(summary, bg="#1f2937", padx=18, pady=18)
            card.pack(side="left", expand=True, padx=8)
            tk.Label(card, text=title, font=("Arial", 11), bg="#1f2937", fg="#dbeafe").pack(anchor="w")
            label = tk.Label(card, text=value, font=("Arial", 20, "bold"), bg="#1f2937", fg=color)
            label.pack(anchor="w", pady=(10, 0))
            self.admin_stat_values.append(label)

        table_frame = tk.Frame(content, bg="#111827", padx=20, pady=20)
        table_frame.pack(fill="both", expand=True, pady=(20, 0))
        tk.Label(table_frame, text="Danh sách tài khoản", font=("Arial", 16, "bold"), bg="#111827", fg="white").pack(anchor="w", pady=(0, 10))

        action_bar = tk.Frame(table_frame, bg="#111827")
        action_bar.pack(fill="x", pady=(0, 10))

        self.admin_search_var = tk.StringVar()
        ttk.Entry(action_bar, textvariable=self.admin_search_var, width=30).pack(side="left")
        ttk.Button(action_bar, text="Tìm kiếm", command=self.search_admin_users).pack(side="left", padx=(8, 0))
        ttk.Button(action_bar, text="Làm mới", command=lambda: self.load_admin_users(self.admin_search_var.get().strip())).pack(side="left", padx=(8, 0))
        ttk.Button(action_bar, text="Xóa người dùng", command=self.delete_selected_user).pack(side="right")

        columns = ("id", "username", "full_name")
        self.admin_table = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        self.admin_table.heading("id", text="ID")
        self.admin_table.heading("username", text="Tên đăng nhập")
        self.admin_table.heading("full_name", text="Họ tên")
        self.admin_table.column("id", width=60, anchor="center")
        self.admin_table.column("username", width=200, anchor="center")
        self.admin_table.column("full_name", width=260, anchor="center")
        self.admin_table.pack(fill="both", expand=True)

        self.load_admin_users()

    def update_admin_dashboard(self, users):
        if len(self.admin_stat_values) >= 3:
            self.admin_stat_values[0].configure(text=str(len(users)))
            self.admin_stat_values[1].configure(text=str(sum(1 for user in users if user[1] != "admin")))
            self.admin_stat_values[2].configure(text="Hoạt động")

    def load_admin_users(self, keyword=""):
        if not hasattr(self, "admin_table"):
            return
        for item in self.admin_table.get_children():
            self.admin_table.delete(item)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        if keyword:
            pattern = f"%{keyword}%"
            cursor.execute(
                "SELECT id, username, full_name FROM users WHERE username LIKE ? OR full_name LIKE ? ORDER BY id",
                (pattern, pattern),
            )
        else:
            cursor.execute("SELECT id, username, full_name FROM users ORDER BY id")
        users = cursor.fetchall()
        conn.close()

        for user in users:
            self.admin_table.insert("", tk.END, values=user)

        self.update_admin_dashboard(users)
        self.admin_table.update_idletasks()

    def search_admin_users(self):
        keyword = self.admin_search_var.get().strip()
        self.load_admin_users(keyword)

    def delete_selected_user(self):
        selected = self.admin_table.selection()
        if not selected:
            messagebox.showwarning("Thông báo", "Vui lòng chọn tài khoản cần xóa.")
            return

        item = self.admin_table.item(selected[0], "values")
        if not item:
            return

        user_id, username, full_name = item
        if username == "admin":
            messagebox.showerror("Lỗi", "Không thể xóa tài khoản admin gốc.")
            return

        confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa tài khoản {username} ({full_name})?")
        if not confirm:
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()

        self.load_admin_users(self.admin_search_var.get().strip())
        messagebox.showinfo("Thành công", "Đã xóa tài khoản thành công.")

    def register_account(self):
        full_name = self.register_entries["full_name"].get().strip()
        username = self.register_entries["register_username"].get().strip()
        password = self.register_entries["register_password"].get().strip()
        confirm = self.register_entries["confirm_password"].get().strip()

        if not full_name or not username or not password or not confirm:
            messagebox.showwarning("Thông báo", "Vui lòng điền đầy đủ thông tin.")
            return

        if password != confirm:
            messagebox.showerror("Lỗi", "Mật khẩu xác nhận không khớp.")
            return

        if len(password) < 4:
            messagebox.showwarning("Thông báo", "Mật khẩu phải có ít nhất 4 ký tự.")
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            conn.close()
            messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại.")
            return

        cursor.execute(
            "INSERT INTO users (username, password, full_name) VALUES (?, ?, ?)",
            (username, hash_password(password), full_name),
        )
        conn.commit()
        conn.close()

        self.register_entries["full_name"].delete(0, tk.END)
        self.register_entries["register_username"].delete(0, tk.END)
        self.register_entries["register_password"].delete(0, tk.END)
        self.register_entries["confirm_password"].delete(0, tk.END)

        messagebox.showinfo("Đăng ký thành công", f"Tài khoản {username} đã được tạo. Bạn có thể đăng nhập ngay.")
        self.show_screen("login")

    def create_home_screen(self):
        frame = tk.Frame(self.container, bg="#f3f6fb")
        self.frames["home"] = frame

        top = tk.Frame(frame, bg="#ffffff", padx=20, pady=18)
        top.pack(fill="x")
        tk.Label(top, text="🏠 Trang chủ", font=("Arial", 26, "bold"), bg="#ffffff", fg="#0f172a").pack(anchor="w")

        self.home_name_var = tk.StringVar(value="Xin chào!")
        tk.Label(top, textvariable=self.home_name_var, font=("Arial", 14), bg="#ffffff", fg="#2563eb").pack(anchor="w", pady=(8, 0))

        tk.Button(top, text="Đăng xuất", bg="#ef4444", fg="white", font=("Arial", 10, "bold"), bd=0, width=12, command=self.logout).pack(anchor="e", pady=(10, 0))

        cards = tk.Frame(frame, bg="#f3f6fb")
        cards.pack(fill="both", expand=True, padx=10, pady=20)

        card_data = [
            ("🎮 Game", "Vui chơi", "7 bài tập", "#f59e0b"),
            ("🛒 Bán hàng", "Quản lý đơn", "120 khách", "#22c55e"),
            ("📚 Học Python", "Bài học mới", "4 chủ đề", "#3b82f6"),
            ("📊 Thống kê", "Hiệu suất", "Tốt", "#a855f7"),
        ]

        for i, (title, subtitle, info, color) in enumerate(card_data):
            card = tk.Frame(cards, bg="#ffffff", padx=18, pady=18, bd=1, relief="flat")
            card.grid(row=i // 2, column=i % 2, padx=15, pady=15, sticky="nsew")
            card.configure(highlightbackground="#e2e8f0", highlightthickness=1)
            tk.Label(card, text=title, font=("Arial", 18, "bold"), bg="#ffffff", fg=color).pack(anchor="w")
            tk.Label(card, text=subtitle, font=("Arial", 11), bg="#ffffff", fg="#475569").pack(anchor="w", pady=(8, 0))
            tk.Label(card, text=info, font=("Arial", 10, "bold"), bg="#ffffff", fg="#0f172a").pack(anchor="w", pady=(10, 0))

        nav = tk.Frame(frame, bg="#f3f6fb")
        nav.pack(fill="x", padx=10, pady=(0, 10))
        for text, page in [("Game", "game"), ("Bán hàng", "sales"), ("Học Python", "learning")]:
            tk.Button(
                nav,
                text=text,
                width=18,
                height=2,
                bg="#2563eb",
                fg="white",
                bd=0,
                font=("Arial", 11, "bold"),
                command=lambda p=page: self.show_screen(p),
            ).pack(side="left", padx=10)

    def create_game_screen(self):
        frame = tk.Frame(self.container, bg="#fff7ed")
        self.frames["game"] = frame

        panel = tk.Frame(frame, bg="#ffffff", padx=30, pady=30)
        panel.pack(expand=True, padx=90, pady=40)

        tk.Label(panel, text="🎯 Game Đoán Số", font=("Arial", 28, "bold"), bg="#ffffff", fg="#9a5b00").pack(pady=(0, 18))
        tk.Label(panel, text="Đoán số từ 1 đến 100", font=("Arial", 13), bg="#ffffff", fg="#475569").pack()

        self.guess_entry = ttk.Entry(panel, width=30, font=("Arial", 13))
        self.guess_entry.pack(pady=20)

        self.game_result_var = tk.StringVar(value="Chưa có kết quả")
        tk.Label(panel, textvariable=self.game_result_var, font=("Arial", 12, "bold"), bg="#ffffff", fg="#b45309").pack(pady=10)

        action = tk.Frame(panel, bg="#ffffff")
        action.pack(pady=15)
        ttk.Button(action, text="Kiểm tra", style="Primary.TButton", command=self.check_guess).pack(side="left", padx=10)
        ttk.Button(action, text="Reset", style="Secondary.TButton", command=self.reset_game).pack(side="left", padx=10)
        ttk.Button(action, text="Về Trang Chủ", style="Secondary.TButton", command=lambda: self.show_screen("home")).pack(side="left", padx=10)

    def create_sales_screen(self):
        frame = tk.Frame(self.container, bg="#f0fdf4")
        self.frames["sales"] = frame

        heading = tk.Label(frame, text="🛒 Giao diện Bán Hàng", font=("Arial", 28, "bold"), bg="#f0fdf4", fg="#166534")
        heading.pack(pady=20)

        products = [
            ("Bánh mì", 15000),
            ("Cà phê", 20000),
            ("Trà sữa", 30000),
            ("Bánh ngọt", 12000),
            ("Nước cam", 25000),
        ]
        self.sale_vars = {}

        product_frame = tk.Frame(frame, bg="#f0fdf4")
        product_frame.pack(pady=10)

        for name, price in products:
            var = tk.BooleanVar(value=False)
            self.sale_vars[name] = var
            row = tk.Frame(product_frame, bg="#ffffff", padx=18, pady=12)
            row.pack(fill="x", pady=6)
            tk.Checkbutton(row, variable=var, text=f"{name} - {price:,.0f}đ", bg="#ffffff", font=("Arial", 11, "bold")).pack(anchor="w")

        self.total_var = tk.StringVar(value="Tổng: 0đ")
        tk.Label(frame, textvariable=self.total_var, font=("Arial", 18, "bold"), bg="#f0fdf4", fg="#14532d").pack(pady=20)

        btns = tk.Frame(frame, bg="#f0fdf4")
        btns.pack()
        ttk.Button(btns, text="Tính tiền", style="Primary.TButton", command=self.calculate_total).pack(side="left", padx=12)
        ttk.Button(btns, text="Về Trang Chủ", style="Secondary.TButton", command=lambda: self.show_screen("home")).pack(side="left", padx=12)

    def create_learning_screen(self):
        frame = tk.Frame(self.container, bg="#eef2ff")
        self.frames["learning"] = frame

        title = tk.Label(frame, text="📚 Học Python", font=("Arial", 28, "bold"), bg="#eef2ff", fg="#312e81")
        title.pack(pady=(25, 15))

        topic_frame = tk.Frame(frame, bg="#eef2ff")
        topic_frame.pack(fill="x", padx=20, pady=10)

        self.topic_var = tk.StringVar(value="Biến")
        for topic in self.topic_data.keys():
            tk.Button(
                topic_frame,
                text=topic,
                width=12,
                height=2,
                bg="#6366f1",
                fg="white",
                bd=0,
                font=("Arial", 10, "bold"),
                command=lambda t=topic: self.show_topic(t),
            ).pack(side="left", padx=6)

        content = tk.Text(frame, height=18, width=100, font=("Courier New", 10), wrap="word")
        content.pack(padx=20, pady=10)
        self.lesson_text = content

        btns = tk.Frame(frame, bg="#eef2ff")
        btns.pack(pady=15)
        ttk.Button(btns, text="Xem ví dụ", style="Primary.TButton", command=self.run_demo).pack(side="left", padx=10)
        ttk.Button(btns, text="Về Trang Chủ", style="Secondary.TButton", command=lambda: self.show_screen("home")).pack(side="left", padx=10)

        self.show_topic("Biến")

    def show_screen(self, name):
        for key, frame in self.frames.items():
            if key == name:
                frame.pack(fill="both", expand=True)
            else:
                frame.pack_forget()
        if name == "home":
            self.home_name_var.set(f"Xin chào, {self.current_user}!")
        if name == "admin":
            self.admin_title_var.set(f"Xin chào, {self.current_user}!")
            self.load_admin_users()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        admin_code = self.admin_code_entry.get().strip()

        if admin_code and admin_code == ADMIN_ACCESS_CODE:
            self.current_user = "Quản trị viên"
            self.current_role = "admin"
            self.admin_title_var.set(f"Xin chào, {self.current_user}!")
            messagebox.showinfo("Đăng nhập thành công", "Chào mừng Quản trị viên!")
            self.show_screen("admin")
            return

        if not username or not password:
            messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ tài khoản và mật khẩu.")
            return

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT full_name FROM users WHERE username = ? AND password = ?",
            (username, hash_password(password)),
        )
        result = cursor.fetchone()
        conn.close()

        if result is None:
            messagebox.showerror("Lỗi đăng nhập", "Tài khoản hoặc mật khẩu không đúng.")
            return

        self.current_user = result[0]
        self.current_role = "user"
        self.home_name_var.set(f"Xin chào, {self.current_user}!")
        messagebox.showinfo("Đăng nhập thành công", f"Chào mừng {self.current_user}!")
        self.show_screen("home")

    def logout(self):
        self.current_user = "Khách"
        self.current_role = "user"
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.admin_code_entry.delete(0, tk.END)
        self.show_screen("login")

    def check_guess(self):
        try:
            guess = int(self.guess_entry.get())
        except ValueError:
            self.game_result_var.set("Vui lòng nhập số hợp lệ.")
            return

        self.guess_count += 1
        if guess == self.target_number:
            self.game_result_var.set(f"Đúng rồi! Bạn đoán {self.guess_count} lần.")
            self.guess_entry.delete(0, tk.END)
        elif guess < self.target_number:
            self.game_result_var.set("Số bạn đoán quá nhỏ, thử lớn hơn nhé!")
        else:
            self.game_result_var.set("Số bạn đoán quá lớn, thử nhỏ hơn nhé!")

    def reset_game(self):
        self.target_number = random.randint(1, 100)
        self.guess_count = 0
        self.guess_entry.delete(0, tk.END)
        self.game_result_var.set("Chưa có kết quả")

    def calculate_total(self):
        products = {
            "Bánh mì": 15000,
            "Cà phê": 20000,
            "Trà sữa": 30000,
            "Bánh ngọt": 12000,
            "Nước cam": 25000,
        }
        total = 0
        for name, value in products.items():
            if self.sale_vars.get(name, tk.BooleanVar()).get():
                total += value
        self.total_var.set(f"Tổng: {total:,.0f}đ")
        messagebox.showinfo("Tổng đơn hàng", f"Tổng tiền: {total:,.0f}đ")

    def show_topic(self, topic):
        self.topic_var.set(topic)
        self.lesson_text.delete("1.0", tk.END)
        self.lesson_text.insert(tk.END, self.topic_data[topic]["content"])

    def run_demo(self):
        topic = self.topic_var.get()
        code = self.topic_data[topic]["code"]
        self.lesson_text.delete("1.0", tk.END)
        self.lesson_text.insert(tk.END, f"Chủ đề: {topic}\n\n")
        self.lesson_text.insert(tk.END, f"Mã nguồn:\n{code}\n\n")
        self.lesson_text.insert(tk.END, "Kết quả: \n")
        self.lesson_text.insert(tk.END, "print('Xin chào Python!')\n")


if __name__ == "__main__":
    app = App()
    app.mainloop()
