from flask import g, current_app
from dataclasses import dataclass

from utils.database import get_cursor, commit

@dataclass
class Account():
    account_id : int
    role: int
    username : str
    password_hash : str

def load_account(account_username: str) -> Account | None:
    try:
        cur = get_cursor()
        query = "SELECT * FROM accounts where account_username = ?"
        args = (account_username)
        cur.execute(query, args)
        data = cur.fetchone()
        account = Account(data['account_id'], data['account_role'], data['account_username'], data['account_password_hash'])
        print(account)
        return account

    except:
        return None

def make_account(account: Account) -> bool:
    cur = get_cursor()
    query = "INSERT INTO accounts (account_username, account_role, account_password_hash) VALUES (?, ?, ?)"
    args = (account.username, account.role, account.password_hash)
    cur.execute(query, args)
    return True if commit() else False

def update_account(account: Account) -> bool:
    cur = get_cursor()
    query = "UPDATE accounts SET account_username = ?, account_password_hash = ? WHERE account_id = ?"
    args = (account.username, account.password_hash, account.account_id)
    cur.execute(query, args)
    return True if commit() else False
