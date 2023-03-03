from typing import TypedDict, Optional
from datetime import datetime

from utils.database import get_cursor, commit

class Account(TypedDict):
    account_id : int
    account_username : Optional[str]
    account_password : Optional[str]
    account_role : Optional[int]
    account_created_at: Optional[datetime]
    account_api_key : Optional[str]
    account_locked : Optional[bool]


def load_account(account: Account) -> Account | None:
    try:
        cur = get_cursor()
        query = "SELECT account_id, account_role, account_username, account_password, account_api_key, account_created_at FROM accounts where account_username = ?"
        args = (account['account_username'],)
        cur.execute(query, args)
        account: Account = cur.fetchone()
        return account

    except:
        return None

def make_account(account: Account) -> bool:
    cur = get_cursor()
    query = "INSERT INTO accounts (account_username, account_role, account_password) VALUES (:account_username, :account_role, :account_password)"
    args = account
    cur.execute(query, args)
    return True if commit() else False

def update_account(account: Account) -> bool:
    cur = get_cursor()
    query = "UPDATE accounts SET account_username = :account_username, account_password = :account_password WHERE account_id = :account_id"
    args = account
    cur.execute(query, args)
    return True if commit() else False

def is_logged_in(session) -> bool:
    return True if 'user_info' in session else False
