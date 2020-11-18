from typing import Final, List

import config
import praw

from model.post import Comment, Post

default_time_filter: Final = "week"
default_max_comments: Final = 5
default_max_posts: Final = 5

reddit = praw.Reddit(client_id=config.REDDIT_CLIENT_ID,
                     client_secret=config.REDDIT_CLIENT_SECRET,
                     user_agent=config.APP_NAME,
                     username=config.REDDIT_USER,
                     password=config.REDDIT_PASSWORD)


def __has_term_from_list__(text: str, string_list: List[str]) -> bool:
    """
    Check if a string contains an item in a list
    """
    for item in string_list:
        if item in text:
            return True

    return False


def __submissions_to_post_list__(
        submissions: list, max_comments: int,
        comment_exclude_terms: List[str] = ["I am a bot", "this action was performed automatically"],
        excluded_subreddit_keywords:List[str] = []) -> List[Post]:
    """
    Converts an iterable object of praw submissions to a list of Posts, ignores stickied posts
    """
    # praw type submission: https://praw.readthedocs.io/en/latest/code_overview/models/submission.html

    posts: Final[List[Post]] = []
    for post in submissions:
       
        if (post.stickied or any(keyword in post.subreddit.display_name.lower() for keyword in excluded_subreddit_keywords)):
            continue
        posts.append(Post(post.title,
                          post.selftext,
                          post.score,
                          post.created,
                          post.id,
                          post.author.name,
                          post.permalink))
        comment_count = 1
        for comment in post.comments:
            if (comment_count >= max_comments):
                break
            if (not __has_term_from_list__(comment.body, comment_exclude_terms)):
                posts[-1].add_comment(Comment(comment.body, comment.score, comment.permalink))
                comment_count += 1

    return posts


def fetch_top_posts(subreddit_name: str,
                    max_posts: int = default_max_posts,
                    max_comments: int = default_max_comments,
                    time_range: str = default_time_filter):
    """
    Gets the top posts along with top comments
    """
    subreddit: Final = reddit.subreddit(subreddit_name)
    top_subreddit: Final = subreddit.top(
        limit=max_posts, time_filter=default_time_filter)

    # top_subreddit is a list of praw submission objects

    return __submissions_to_post_list__(top_subreddit, max_comments)


def search(query: str,
           max_posts: int = default_max_posts,
           max_comments: int = default_max_comments,
           time_range: str = default_time_filter,
           excluded_subreddit_keywords: List[str] = []):
    """
    searches all subreddits for a string
    """
    return __submissions_to_post_list__(reddit.subreddit("all").search(
        query=query, time_filter=time_range, limit=max_posts),
        max_comments,excluded_subreddit_keywords=excluded_subreddit_keywords)
