import sys
import os
# Python does not support importing modules from parent directory in scripts
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)))

import unittest
from util.text_helper import pre_process_text, delete_all
from model.post import Post, Comment
from reddit_words import lemmatize_words
from service.text_analysis import remove_special_chars, remove_hashtags_mentions, remove_links

class TestPost(unittest.TestCase):

    def test_add_comment(self):
        post = Post("Title", "", 10, 999, "myid", "Test", "http://")
        for x in range(0, 5):
            post.add_comment(Comment(str(x), x,"http://"))

        self.assertEqual(post.comments[0].text, "0")
        self.assertEqual(post.comments[1].text, "1")
        self.assertEqual(post.comments[2].text, "2")
        self.assertEqual(post.comments[3].text, "3")
        self.assertEqual(post.comments[4].text, "4")

    def test_add_comment_when_post_is_in_a_list(self):
        post = [Post("Title", "", 10, 999, "myid", "Test", "http://"),
                Post("Post 2", "", 10, 999, "myid", "AAA", "http://")]
        for x in range(0, 5):
            post[-1].add_comment(Comment(str(x), x,"http://"))

        self.assertEqual(len(post[0].comments), 0)

        self.assertEqual(post[1].comments[0].text, "0")
        self.assertEqual(post[1].comments[1].text, "1")
        self.assertEqual(post[1].comments[2].text, "2")
        self.assertEqual(post[1].comments[3].text, "3")
        self.assertEqual(post[1].comments[4].text, "4")

    def test_pre_process_text(self):
        text = "hello [this is a thing] world"
        processed_text = pre_process_text(text)

        self.assertEqual(processed_text, "hello  world")

    def test_remove_urls(self):
        text = "[Common bug with multiple solutions](https://answers.ea.com/t5/Origin-Client-Web-Technical/We-re-sorry-but-we-re-having-some-technical-difficulties-Please/td-p/8295143)"
        processed_text = pre_process_text(text)

        self.assertFalse("http" in processed_text)

    def test_delete_all(self):
        text = "hello [this is a thing] world"
        text = delete_all(r"\[.*\]",text)

        self.assertEqual(text, "hello  world")

    def test_lemmatize_words(self):
        text = "dogs pies cats bikes"
        lemmatized_words = lemmatize_words(text)

        self.assertEqual(lemmatized_words, ['dog', 'pie', 'cat', 'bike'])

    def test_get_score(self):
        s = "@mainvolume Thats dead! #Da #T #ea  https://t.co/7iEHxtlYPA"
        s = remove_special_chars(s)
        s = remove_links(s)
        s = remove_hashtags_mentions(s)
        s = s.strip()

        self.assertEqual(s, "Thats dead!")

if __name__ == '__main__':
    unittest.main()
