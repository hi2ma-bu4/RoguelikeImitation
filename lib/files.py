# coding: utf-8
"""
ファイル読み書き用のライブラリ
"""

from typing import Any, List, Dict, Union
from csv import reader, writer
from json import dump, load
from sqlite3 import connect, Connection


class File:
    def __init__(self, path: str = "") -> None:
        """
        使用ファイルパス
        """
        self.path = path


class FileCSV(File):
    def set(self, lst: List[List[str]]) -> None:
        try:
            with open(self.path, "w", newline="") as f:
                writer(f).writerows(lst)
        except Exception as e:
            print(e)
            input("PAUSE")

    def get(self) -> Union[List[List[str]], List[Any]]:
        try:
            with open(self.path, "r") as f:
                return [r for r in reader(f)]
        except:
            return []


class FileJSON(File):
    def set(self, dic: dict) -> None:
        try:
            with open(self.path, "w", newline="") as f:
                dump(dic, f)
        except Exception as e:
            print(e)
            input("PAUSE")

    def get(self) -> dict:
        try:
            with open(self.path, "r", encoding="utf-8_sig") as f:
                return load(f)
        except:
            return dict()


class SqlManager:
    def __init__(self, db_path: str, table_name: str, initTable: str = "") -> None:
        self.db_path = db_path
        self.table_name = table_name

        if initTable != "":
            with sqliteOpen(self.db_path) as db:
                db.execute(fr"""
CREATE TABLE
    IF NOT EXISTS {self.table_name} (
        {initTable}
    )
""")

    def select(self, *, select: str = "*", where: str = "") -> List[List[Any]]:
        sql = fr"SELECT {select} FROM {self.table_name}"
        if where:
            sql += fr" WHERE {where}"

        with sqliteOpen(self.db_path) as db:
            cur = db.cursor()

            cur.execute(sql)
            lst = cur.fetchall()

            cur.close()
        return lst

    def insert(self, tup: tuple) -> None:
        quest = ",".join(["?"]*len(tup))
        with sqliteOpen(self.db_path) as db:
            db.execute(fr"INSERT INTO {self.table_name} VALUES ({quest})", tup)
            db.commit()

    def update(self, data: Dict[str, Any], where: str = "") -> None:
        updData = [f"{name}='{value}'" for name, value in data.items()]

        sql = fr"UPDATE {self.table_name} SET {','.join(updData)}"
        if where:
            sql += fr" WHERE {where}"

        with sqliteOpen(self.db_path) as db:
            db.execute(sql)
            db.commit()

    def delete(self, where: str = "") -> None:
        sql = fr"DELETE FROM {self.table_name}"
        if where:
            sql += fr" WHERE {where}"

        with sqliteOpen(self.db_path) as db:
            db.execute(sql)
            db.commit()


class sqliteOpen(object):
    def __init__(self, db_path: str) -> None:
        self._db_path = db_path

    def __enter__(self) -> Connection:
        try:
            self.con = connect(self._db_path)
        except Exception as e:
            raise RuntimeError("接続失敗", e)
        return self.con

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.con.close()
