import aiosqlite
from datetime import datetime
from pathlib import Path
from bot.config import DB_PATH


class Database:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = str(db_path)

    async def init_db(self):
        """Ma'lumotlar bazasi jadvallarini yaratish"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("PRAGMA foreign_keys = ON")

            # 1. Users jadvali
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    telegram_id INTEGER PRIMARY KEY,
                    full_name TEXT NOT NULL,
                    username TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            # 2. Orders jadvali
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    service_type TEXT NOT NULL,
                    project_name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    budget TEXT NOT NULL,
                    deadline TEXT NOT NULL,
                    contact TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (telegram_id) ON DELETE CASCADE
                )
                """
            )

            # 3. Portfolio jadvali
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS portfolio (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    category TEXT NOT NULL,
                    description TEXT NOT NULL,
                    link TEXT,
                    image_url TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            # Boshlang'ich portfolio ma'lumotlarini kiritish (agar bo'sh bo'lsa)
            async with db.execute("SELECT COUNT(*) FROM portfolio") as cursor:
                count = (await cursor.fetchone())[0]

            if count == 0:
                initial_portfolios = [
                    (
                        "Nexora Shop Bot",
                        "bot",
                        "Telegram orqali to'liq avtomatlashtirilgan internet do'koni. Click & Payme to'lovlari, savatcha va buyurtmalar admin paneli bilan jihozlangan.",
                        "https://t.me/NEXORA712",
                        None,
                    ),
                    (
                        "FastFood Delivery Bot",
                        "bot",
                        "Restoran va kafelar uchun yetkazib berish xizmati boti. Geolokatsiya aniqlash, chek chiqarish va kuryer bildirishnomalari mavjud.",
                        "https://t.me/NEXORA712",
                        None,
                    ),
                    (
                        "Kompaniya Korporativ Sayti",
                        "website",
                        "Zamonaviy dizayn, SEO optimallashtirilgan, mobil va planshetlarga to'liq moslashuvchan korporativ veb-sayt.",
                        "https://t.me/NEXORA712",
                        None,
                    ),
                    (
                        "Kripto & Moliya Landing Page",
                        "website",
                        "Interaktiv 3D animatsiyalar, dark cyber uslubi va yuqori konversiyali zamonaviy landing sahifa.",
                        "https://t.me/NEXORA712",
                        None,
                    ),
                ]
                await db.executemany(
                    """
                    INSERT INTO portfolio (title, category, description, link, image_url)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    initial_portfolios,
                )

            await db.commit()

    # ------------------ USERS ------------------
    async def add_user(self, telegram_id: int, full_name: str, username: str | None = None) -> bool:
        """Foydalanuvchini bazaga qo'shish yoki ma'lumotlarini yangilash"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                """
                INSERT INTO users (telegram_id, full_name, username)
                VALUES (?, ?, ?)
                ON CONFLICT(telegram_id) DO UPDATE SET
                    full_name = excluded.full_name,
                    username = excluded.username
                """,
                (telegram_id, full_name, username),
            )
            await db.commit()
            return True

    async def get_user(self, telegram_id: int) -> dict | None:
        """Foydalanuvchi ma'lumotlarini olish"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)
            ) as cursor:
                row = await cursor.fetchone()
                return dict(row) if row else None

    async def get_all_users(self) -> list[dict]:
        """Barcha foydalanuvchilar ro'yxati (xabar tarqatish uchun)"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT * FROM users") as cursor:
                rows = await cursor.fetchall()
                return [dict(r) for r in rows]

    async def get_users_count(self) -> int:
        """Jami foydalanuvchilar soni"""
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT COUNT(*) FROM users") as cursor:
                row = await cursor.fetchone()
                return row[0] if row else 0

    # ------------------ ORDERS ------------------
    async def create_order(
        self,
        user_id: int,
        service_type: str,
        project_name: str,
        description: str,
        budget: str,
        deadline: str,
        contact: str,
    ) -> int:
        """Yangi buyurtma yaratish va ID sini qaytarish"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                """
                INSERT INTO orders (user_id, service_type, project_name, description, budget, deadline, contact, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'pending')
                """,
                (user_id, service_type, project_name, description, budget, deadline, contact),
            )
            await db.commit()
            return cursor.lastrowid

    async def get_order(self, order_id: int) -> dict | None:
        """Buyurtmani ID bo'yicha to'liq olish (foydalanuvchi ma'lumotlari bilan)"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                """
                SELECT o.*, u.full_name as user_full_name, u.username as user_username
                FROM orders o
                LEFT JOIN users u ON o.user_id = u.telegram_id
                WHERE o.id = ?
                """,
                (order_id,),
            ) as cursor:
                row = await cursor.fetchone()
                return dict(row) if row else None

    async def get_orders(self, status: str | None = None, limit: int = 20, offset: int = 0) -> list[dict]:
        """Buyurtmalar ro'yxatini olish (status bo'yicha filtr bilan)"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            if status and status != "all":
                query = """
                    SELECT o.*, u.full_name as user_full_name, u.username as user_username
                    FROM orders o
                    LEFT JOIN users u ON o.user_id = u.telegram_id
                    WHERE o.status = ?
                    ORDER BY o.id DESC
                    LIMIT ? OFFSET ?
                """
                params = (status, limit, offset)
            else:
                query = """
                    SELECT o.*, u.full_name as user_full_name, u.username as user_username
                    FROM orders o
                    LEFT JOIN users u ON o.user_id = u.telegram_id
                    ORDER BY o.id DESC
                    LIMIT ? OFFSET ?
                """
                params = (limit, offset)

            async with db.execute(query, params) as cursor:
                rows = await cursor.fetchall()
                return [dict(r) for r in rows]

    async def get_user_orders(self, user_id: int) -> list[dict]:
        """Bitta foydalanuvchining barcha buyurtmalarini olish"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT * FROM orders WHERE user_id = ? ORDER BY id DESC",
                (user_id,),
            ) as cursor:
                rows = await cursor.fetchall()
                return [dict(r) for r in rows]

    async def update_order_status(self, order_id: int, new_status: str) -> bool:
        """Buyurtma holatini yangilash"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "UPDATE orders SET status = ? WHERE id = ?",
                (new_status, order_id),
            )
            await db.commit()
            return True

    # ------------------ STATISTICS ------------------
    async def get_stats(self) -> dict:
        """Statistika hisobotini tayyorlash"""
        async with aiosqlite.connect(self.db_path) as db:
            # 1. Jami foydalanuvchilar
            async with db.execute("SELECT COUNT(*) FROM users") as cur:
                total_users = (await cur.fetchone())[0]

            # 2. Jami buyurtmalar
            async with db.execute("SELECT COUNT(*) FROM orders") as cur:
                total_orders = (await cur.fetchone())[0]

            # 3. Bugungi buyurtmalar (DATE(created_at) = DATE('now', 'localtime'))
            async with db.execute(
                "SELECT COUNT(*) FROM orders WHERE DATE(created_at, 'localtime') = DATE('now', 'localtime')"
            ) as cur:
                today_orders = (await cur.fetchone())[0]

            # 4. Shu oylik buyurtmalar
            async with db.execute(
                "SELECT COUNT(*) FROM orders WHERE strftime('%Y-%m', created_at, 'localtime') = strftime('%Y-%m', 'now', 'localtime')"
            ) as cur:
                month_orders = (await cur.fetchone())[0]

            # 5. Xizmat turi bo'yicha
            async with db.execute(
                "SELECT COUNT(*) FROM orders WHERE service_type LIKE '%bot%'"
            ) as cur:
                bot_orders = (await cur.fetchone())[0]

            async with db.execute(
                "SELECT COUNT(*) FROM orders WHERE service_type LIKE '%sayt%' OR service_type LIKE '%veb%'"
            ) as cur:
                site_orders = (await cur.fetchone())[0]

            # 6. Holatlar bo'yicha
            async with db.execute("SELECT COUNT(*) FROM orders WHERE status = 'pending'") as cur:
                pending_orders = (await cur.fetchone())[0]

            async with db.execute("SELECT COUNT(*) FROM orders WHERE status = 'in_progress'") as cur:
                in_progress_orders = (await cur.fetchone())[0]

            async with db.execute("SELECT COUNT(*) FROM orders WHERE status = 'completed'") as cur:
                completed_orders = (await cur.fetchone())[0]

            async with db.execute("SELECT COUNT(*) FROM orders WHERE status = 'rejected'") as cur:
                rejected_orders = (await cur.fetchone())[0]

            return {
                "total_users": total_users,
                "total_orders": total_orders,
                "today_orders": today_orders,
                "month_orders": month_orders,
                "bot_orders": bot_orders,
                "site_orders": site_orders,
                "pending_orders": pending_orders,
                "in_progress_orders": in_progress_orders,
                "completed_orders": completed_orders,
                "rejected_orders": rejected_orders,
            }

    # ------------------ PORTFOLIO ------------------
    async def get_portfolios(self, category: str | None = None) -> list[dict]:
        """Portfolio loyihalarini olish"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            if category and category != "all":
                query = "SELECT * FROM portfolio WHERE category = ? ORDER BY id DESC"
                params = (category,)
            else:
                query = "SELECT * FROM portfolio ORDER BY id DESC"
                params = ()

            async with db.execute(query, params) as cursor:
                rows = await cursor.fetchall()
                return [dict(r) for r in rows]

    async def add_portfolio(
        self, title: str, category: str, description: str, link: str | None = None, image_url: str | None = None
    ) -> int:
        """Yangi portfolio loyihasini qo'shish"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute(
                """
                INSERT INTO portfolio (title, category, description, link, image_url)
                VALUES (?, ?, ?, ?, ?)
                """,
                (title, category, description, link, image_url),
            )
            await db.commit()
            return cursor.lastrowid


# Yagona ma'lumotlar bazasi obyekti
db = Database()
