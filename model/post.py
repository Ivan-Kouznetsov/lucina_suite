from typing import List


class Comment:
    def __init__(self, text: str, score: int, permalink: str):
        self.text = text
        self.score = score
        self.permalink = permalink

    def __str__(self):
        return self.text


class Post:
    def __init__(
            self, title: str, text: str, score: int, created: int, id_: str, author: str, permalink: str,
            comments: List[Comment] = []):
        self.title = title
        self.text = text
        self.score = score
        # necessary because self.comments = comments results in all instances of Post using the same list instance for comments
        self.comments: List[Comment] = []
        self.created = created
        self.id = id_  # id is a reserved keyword, see also: https://www.python.org/dev/peps/pep-0008/#descriptive-naming-styles
        self.author = author
        self.permalink = permalink

        for comment in comments:
            self.comments.append(Comment(comment.text, comment.score, comment.permalink))

    def add_comment(self, comment: Comment):
        self.comments.append(Comment(comment.text, comment.score, comment.permalink))

    def __str__(self):
        post_as_text = self.title + '\n' + self.text
        for comment in self.comments:
            post_as_text += comment.text

        return post_as_text

    @staticmethod
    def from_object(post_object):
        return Post(title=post_object.title,
                    text=post_object.text,
                    score=post_object.score,
                    created=post_object.created,
                    id_=post_object.id,
                    author=post_object.author,
                    comments=post_object.comments,
                    permalink=post_object.permalink)
