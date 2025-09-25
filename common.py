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
        t.span(f"Jeremy Nelson")
        t(html(" &copy;")) 
        t.span(f"2019-{current_date.year}")

    def populate(self):
        
        with t.footer():
            self.copyright()
            latest_blog = blog_posts[-1]
            current_year = latest_blog["year"]
            last_post = latest_blog["posts"][-1]
            t.span(f"  Last updated on {current_year}-{last_post.stem}")
            

@t.component()
class BlogHeader(Component):
    props = ["year"]

    def populate(self):
        with t.div(class_name="title"):
            title = "Garden Reflections"
            if self.year:
                title = f"{title} - {self.year}"
            t.h1(title, class_name="title")
            t.h2("A Blog by Jeremy Nelson", class_name="subtitle")
            t.a("RSS feed", href="rss.xml", style="color: orange;float: right")



@t.component()
class BlogPost(Component):
    props = ["post_md"]
        
    def populate(self):
        year = self.post_md.parent.name
        self.raw_html = markdown.markdown(self.post_md.read_text())
        self.id = f"{year}/{self.post_md.stem}"
        self.post_date = f"{self.post_md.stem}-{year}"
        with t.div(class_name="blog-post"):
            t.h2(self.post_date, id=self.id)
            t(html(self.raw_html))


@t.component()
class PostListing(Component):
    props = ["year", "posts"]

    def link(self, year: str, post_name: str):
        if not str(year).startswith("0"):
            year = f"0{year}"
        return t.a(
            post_name,
            href=f"/#posts/{year}/{post_name}"
        )

    def single_year(self):
        for post in self.posts:
            with t.li():
                self.link(self.year, post.stem)

    def listing(self):
        with t.ul(class_name="latest"):
            if self.year:
                self.single_year()
            else:
                for row in sorted(self.posts, key=lambda x: x['year'], reverse=True):
                    with t.li(class_name="year"):
                        t.a(
                            str(row["year"]), 
                            href=f"/#posts/0{row['year']}"
                        )
                    for post in sorted(row["posts"], reverse=True):
                        with t.li():
                            self.link(row['year'], post.stem)



    def populate(self):
        with t.div(class_name="listing"):
            if not self.posts:
                self.posts = blog_posts
            if self.year:
                t.h3(f"{self.year} Posts", class_name="post-listing")
            else:
                t.h3("Latest", class_name="post-listing")
            self.listing()



