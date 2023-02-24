from flask import g, current_app
from typing import TypedDict, Optional

from utils.database import get_cursor, commit
from utils.tag import Tag, is_tag, make_tag
from datetime import datetime

class Post(TypedDict):
    post_id : int
    post_creator_id : Optional[int]
    post_media_id : Optional[str]
    post_description : Optional[str]
    post_created_at : Optional[datetime]
    post_updated_at : Optional[datetime]


def make_post(post: Post) -> bool:
    cur = get_cursor()
    query = "INSERT INTO posts (post_creator_id, post_media_id, post_description) VALUES (:post_creator_id, :post_media_id, :post_description)"
    args = post
    cur.execute(query, args)
    return True if commit() else False

def assign_post_tag(post: Post, tag: Tag) -> bool:
    cur = get_cursor()
    if is_tag(tag):
        query = "INSERT INTO tagsofposts (post_id, tag_id) VALUES (?, ?)"
        args = (post['post_id'], tag['tag_id'])
        cur.execute(query, args)

    else:
        make_tag(tag)
        return assign_post_tag(post, tag)

    return True if commit() else False

def remove_post_tag(post: Post, tag: Tag) -> bool:
    cur = get_cursor()
    query = "DELETE tagsofposts WHERE post_id = ? AND tag_id = ? "
    args = (post.post_id, tag.tag_id)
    cur.execute(query, args)
    return True if commit() else False


def search_posts_by_tag(tag: Tag) -> list[Post]:
    cur = get_cursor()
    query = """
    SELECT DISTINCT posts.post_id, posts.post_creator_id, posts.post_media_id, posts.post_description, posts.post_updated_at
    FROM posts
    INNER JOIN tagsofposts ON posts.post_id = tagsofposts.post_id
    WHERE tag_id = (SELECT tag_id FROM tags WHERE tag_name = :tag_name)
    """
    args = tag
    result = cur.execute(query, args)
    posts : list[Post] = result.fetchall()
    return posts

def search_post_by_media_id(post: Post) -> Post:
    cur = get_cursor()
    query = """
    SELECT post_id, post_creator_id, post_media_id,
           post_description, post_created_at, post_updated_at FROM posts WHERE post_media_id = :post_media_id
    """
    args = post
    result = cur.execute(query, args)
    posts : Post = result.fetchall()
    return posts

def load_post(post: Post) -> Post:
    cur = get_cursor()
    query = """
    SELECT post_id, post_creator_id, post_media_id,
           post_description, post_created_at, post_updated_at FROM posts WHERE post_id = :post_id
    """
    args = post
    result = cur.execute(query, args)
    posts : Post = result.fetchall()
    return posts
