BLOG_LIST_CACHE_KEY = "posts:blog_list"


def post_detail_cache_key(post_id: int) -> str:
    return f"posts:post:{post_id}"
