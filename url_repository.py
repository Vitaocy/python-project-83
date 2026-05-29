import psycopg2
from psycopg2.extras import DictCursor


class UrlRepository:
    def __init__(self, db_url):
        self.db_url = db_url

    def get_connection(self):
        return psycopg2.connect(self.db_url)

    def get_content(self):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                query = '''
                SELECT DISTINCT ON (urls.id)
                                urls.id, 
                                urls.name, 
                                url_checks.checked_at AS last_check, 
                                url_checks.code AS status_code
                            FROM urls
                            LEFT JOIN url_checks ON urls.id = url_checks.url_id
                            ORDER BY urls.id, url_checks.id DESC;
                '''
                cur.execute(query)
                return [dict(row) for row in cur]

    def find(self, id):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
                row = cur.fetchone()
                return dict(row) if row else None

    def save(self, url):
        if "id" in url and url["id"]:
            self._update(url)
        else:
            self._create(url)

    def _update(self, url):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE urls SET name = %s WHERE id = %s",
                    (url["name"], url["id"]),
                )
            conn.commit()

    def _create(self, url):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO urls (name) VALUES (%s) RETURNING *",
                    (url["name"],),
                )
                result = cur.fetchone()
                if result:
                    url["id"] = result[0]
                    url["created_at"] = result[2] 
                else:
                    raise Exception("Failed to create url")
            conn.commit()
    
    def destroy(self, id):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM urls WHERE id = %s", (id,))
            conn.commit()

    def add_check(self, url_id):
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO url_checks (url_id) VALUES (%s)", (url_id,))
            conn.commit()

    def get_checks(self, url_id):
        with self.get_connection() as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute("SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC", (url_id,))
                return [dict(row) for row in cur]