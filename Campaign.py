import psycopg2
import json

class Campaign:
    def __init__(self, name, dm_id=None, players=None):
        self.name = name
        self.dm_id = dm_id
        self.players = players or []

    @staticmethod
    def create_campaign(conn, name, dm_id=None):
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO campaigns (name, dm_id, players) VALUES (%s, %s, %s) RETURNING id;",
                (name, dm_id, json.dumps([]))
            )
            campaign_id = cur.fetchone()[0]
            conn.commit()
            return campaign_id

    @staticmethod
    def get_campaign(conn, campaign_id):
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, dm_id, players FROM campaigns WHERE id = %s;", (campaign_id,))
            row = cur.fetchone()
            if row:
                return Campaign(row[1], row[2], json.loads(row[3]))
            return None

    def add_player(self, conn, player_id):
        if player_id not in self.players:
            self.players.append(player_id)
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE campaigns SET players = %s WHERE name = %s;",
                    (json.dumps(self.players), self.name)
                )
                conn.commit()