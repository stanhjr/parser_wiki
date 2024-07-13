import sqlite3

from schemas import PoliticianRecord


def create_parse_info_table():
    conn = sqlite3.connect("politicians.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Paginationv3 (
            id INTEGER PRIMARY KEY,
            limit_value INTEGER,
            offset_value INTEGER
        )
    """
    )
    cursor.execute(
        "INSERT OR IGNORE INTO Paginationv3 (id, limit_value, offset_value) VALUES (1, 1000, 0)"
    )
    conn.commit()
    conn.close()


def get_pagination_params() -> tuple[int, int]:
    conn = sqlite3.connect("politicians.db")
    c = conn.cursor()
    c.execute("SELECT limit_value, offset_value FROM Paginationv3 WHERE id = 1")
    row = c.fetchone()
    conn.close()
    if row:
        limit_value, offset_value = row
    else:
        limit_value, offset_value = 1000, 0
    return limit_value, offset_value


def update_pagination_params(limit_value, offset_value):
    conn = sqlite3.connect("politicians.db")
    c = conn.cursor()
    c.execute(
        "UPDATE Paginationv3 SET limit_value = ?, offset_value = ? WHERE id = 1",
        (limit_value, offset_value),
    )
    conn.commit()
    conn.close()


def create_politicians_table():
    conn = sqlite3.connect("politicians_v2.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS politicians (
            id TEXT PRIMARY KEY,
            label TEXT,
            literal TEXT,
            uri TEXT,
            politicianLabel TEXT,
            positionLabel TEXT,
            countryLabel TEXT,
            partyLabel TEXT,
            twitter TEXT,
            instagram TEXT,
            facebook TEXT,
            is_update INTEGER DEFAULT 0  -- New field `is_update` with default value 0
        )
        """
    )
    conn.commit()
    conn.close()


def add_politician(record: PoliticianRecord):
    conn = sqlite3.connect("politicians_v2.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO politicians (id, label, literal, uri, politicianLabel, positionLabel, countryLabel, partyLabel, twitter, instagram, facebook)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            label=excluded.label,
            literal=excluded.literal,
            uri=excluded.uri,
            politicianLabel=excluded.politicianLabel,
            positionLabel=excluded.positionLabel,
            countryLabel=excluded.countryLabel,
            partyLabel=excluded.partyLabel,
            twitter=excluded.twitter,
            instagram=excluded.instagram,
            facebook=excluded.facebook
    """,
        (
            record.id,
            record.label,
            record.literal,
            record.uri,
            record.politicianLabel,
            record.positionLabel,
            record.countryLabel,
            record.partyLabel,
            record.twitter,
            record.instagram,
            record.facebook,
        ),
    )
    conn.commit()
    conn.close()


def get_politician_count(is_update: int = 0) -> int:
    conn = sqlite3.connect("politicians_v2.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM politicians WHERE is_update=?", (is_update,))
    return cursor.fetchone()[0]


def update_politician(politician: PoliticianRecord):
    conn = sqlite3.connect("politicians_v2.db")
    cursor = conn.cursor()

    params = (
        politician.label,
        politician.literal,
        politician.uri,
        politician.politicianLabel,
        politician.positionLabel,
        politician.countryLabel,
        politician.partyLabel,
        politician.twitter,
        politician.instagram,
        politician.facebook,
        politician.id,
    )
    sql = """
    UPDATE politicians 
    SET 
        label = ?,
        literal = ?,
        uri = ?,
        politicianLabel = ?,
        positionLabel = ?,
        countryLabel = ?,
        partyLabel = ?,
        twitter = ?,
        instagram = ?,
        facebook = ?,
        is_update = 1
    WHERE id = ?
    """

    cursor.execute(sql, params)
    conn.commit()
    conn.close()


def get_politicians(
    offset: int = 0, limit: int = 10, is_update: int = 0
) -> list[PoliticianRecord]:
    conn = sqlite3.connect("politicians_v2.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM politicians WHERE is_update = ? ORDER BY id LIMIT ? OFFSET ?",
        (is_update, limit, offset),
    )

    politicians = []
    for row in cursor.fetchall():
        politician = PoliticianRecord(
            id=row[0],
            label=row[1],
            literal=row[2],
            uri=row[3],
            politicianLabel=row[4],
            positionLabel=row[5],
            countryLabel=row[6],
            partyLabel=row[7],
            twitter=row[8],
            instagram=row[9],
            facebook=row[10],
        )
        politicians.append(politician)
    conn.close()
    return politicians


if __name__ == "__main__":
    print(get_politician_count(is_update=0))
    # for p in get_politicians(is_update=1, limit=1000, offset=10):
    #     print(p)
    # for i in get_politicians(is_update=1, limit=500):
    #     print(i)
