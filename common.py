import datetime
import pathlib

import markdown

from js import console

from puepy import Component, t
from puepy.core import html


blog_posts = []
current_date = datetime.datetime.now(datetime.UTC)
for year in range(2019, current_date.year+1):
    year_path = pathlib.Path(f"0{year}")
    year_posts = []
    for blog_post in year_path.glob("*.md"):
        year_posts.append(blog_post)
    blog_posts.append({ "year": year, "posts": sorted(year_posts) })
        

@t.component()
class BlogFooter(Component):

    def copyright(self):
        t.span(f"Jeremy Nelson &copy; 2019-{current_date.year}")

    def populate(self):
        
        with t.footer():
            self.copyright()
            latest_blog = blog_posts[-1]
            current_year = latest_blog["year"]
            last_post = latest_blog["posts"][-1]
            t.span(f"Last updated on {current_year}-{last_post.name}")
            

@t.component()
class BlogHeader(Component):

    def populate(self):
        with t.div(class_name="title"):
            t.h1("Garden Reflections", class_name="title")
            t.h2("A Blog by Jeremy Nelson", class_name="subtitle")
            t.a("RSS feed", href="rss.xml", style="color: orange;float: right")
