from flask import g, current_app
from typing import TypedDict, Optional

from utils.database import get_cursor, commit
from utils.tag import Tag, is_tag, make_tag, find_tag_by_name
from datetime import datetime

class Post(TypedDict):
    post_id : int
    post_creator_id : Optional[int]
    post_media_id : Optional[str]
    post_description : Optional[str]
    post_created_at : Optional[datetime]
    post_updated_at : Optional[datetime]
    post_first_tags: Optional[str]
    post_tags: Optional[str]


def make_post(post: Post) -> bool:
    cur = get_cursor()
    query = "INSERT INTO posts (post_creator_id, post_media_id, post_description) VALUES (:post_creator_id, :post_media_id, :post_description)"
    args = post
    cur.execute(query, args)
    return True if commit() else False

def assign_post_tag(post: Post, tag: Tag) -> bool:
    cur = get_cursor()
    if is_tag(tag):
        tag = find_tag_by_name(tag)
        query = "INSERT INTO tagsofposts (post_id, tag_id) VALUES (?, ?)"
        args = (post['post_id'], tag['tag_id'])
        cur.execute(query, args)

    else:
        make_tag(tag)
        return assign_post_tag(post, tag)

    return True if commit() else False

def remove_post(post: Post) -> bool:
    cur = get_cursor()
    query = "DELETE FROM posts WHERE post_id = :post_id"
    args = post
    cur.execute(query, args)
    return True if commit() else False

def remove_post_tag(post: Post, tag: Tag) -> bool:
    cur = get_cursor()
    query = "DELETE FROM tagsofposts WHERE post_id = ? AND tag_id = ? "
    args = (post.post_id, tag.tag_id)
    cur.execute(query, args)
    return True if commit() else False

def remove_post_all_tags(post: Post) -> bool:
    cur = get_cursor()
    query = "DELETE FROM tagsofposts WHERE post_id = :post_id "
    args = post
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
    posts : Post = result.fetchone()
    return posts

def find_post_tags(post: Post, num_tags=None) -> dict:
    cur = get_cursor()
    if num_tags is not None:
        query = """
        SELECT tags.tag_id, tags.tag_name, tags.tag_namespace
        FROM tags
        INNER JOIN tagsofposts ON tags.tag_id = tagsofposts.tag_id
        WHERE tagsofposts.post_id = :post_id
        LIMIT :tag_limit
        """
        args = post | {"tag_limit": num_tags}
    else:
        query = """
        SELECT tags.tag_id, tags.tag_name, tags.tag_namespace
        FROM tags
        INNER JOIN tagsofposts ON tags.tag_id = tagsofposts.tag_id
        WHERE tagsofposts.post_id = :post_id
        """
        args = post | {"tag_limit": num_tags}

    result = cur.execute(query, args)
    tags: list[Tag] = result.fetchall()
    return tags

def load_post(post: Post) -> Post:
    cur = get_cursor()
    query = """
    SELECT post_id, post_creator_id, post_media_id,
           post_description, post_created_at, post_updated_at FROM posts WHERE post_id = :post_id
    """
    args = post
    result = cur.execute(query, args)
    posts : Post = result.fetchone()
    return posts

def make_posts_data_props(posts: list[Post], num_preview_tags=None) -> list[Post]:
    for post in posts:
        post = post.update( { "post_first_tags": ", ".join(tag['tag_name'] for tag in find_post_tags(post, num_preview_tags)) } )

    return posts

def make_post_data_tagged(post: Post) -> Post:
    post = post | {"tags": ', '.join(tag['tag_name'] for tag in  find_post_tags(post)) }
    return post
