from flask import g, current_app
from typing import TypedDict, Optional

from utils.database import get_cursor, commit

class Tag(TypedDict):
    tag_id : Optional[int]
    tag_name : Optional[str]
    tag_namespace: Optional[str]

def make_tag(tag: Tag) -> bool:
    cur = get_cursor()
    query = "INSERT INTO tags (tag_name, tag_namespace) VALUES (:tag_name, :tag_namespace)"
    args = tag
    cur.execute(query, args)
    return True if commit() else False

def update_tag(tag: Tag) -> bool:
    cur = get_cursor()
    query = "UPDATE tags SET tag_name = :tag_name WHERE tag_id = :tag_id"
    args = tag
    cur.execute(query, args)
    return True if commit() else False


def find_tag_by_name(tag: Tag) -> Tag:
    cur = get_cursor()
    query = "SELECT DISTINCT tag_id, tag_name, tag_namespace FROM tags WHERE tag_name = :tag_name"
    args = tag
    result = cur.execute(query, args)
    ans = []

    tag: Tag = result.fetchone()
    return tag

def is_tag(tag: Tag) -> bool:
    return True if find_tag_by_name(tag) else False
