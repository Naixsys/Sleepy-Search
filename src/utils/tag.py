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
    query = "UPDATE tags SET tag_name = ? WHERE tag_id = ?"
    args = (tag.tag_name, tag.tag_id)
    cur.execute(query, args)
    return True if commit() else False


def find_tag_id_by_name(tag: Tag) -> list[Tag]:
    cur = get_cursor()
    query = "SELECT DISTINCT tag_id FROM tags WHERE tag_name = ?"
    args = (tag.tag_name,)
    result = cur.execute(query, args)
    ans = []
    for tags in result.fetchall():
        ans.append(Tag
                   (
                       tags['tag_id'],
                       tags['tag_name']
                    )
                   )

    return ans

def is_tag(tag: Tag) -> bool:
    return True if find_tag_id_by_name(tag) else False
