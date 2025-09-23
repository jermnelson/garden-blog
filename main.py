import pathlib

from js import console

from puepy import Application, Page, t
from puepy.router import Router
from puepy.exceptions import NotFound

from common import blog_posts


app = Application()
app.install_router(Router, link_mode=Router.LINK_MODE_HASH)


@app.page("/posts/<year>/<post_id>")
class BlogPost(Page):
    props = ["year", "post_id"]

    def populate(self):
        post_path = pathlib.Path(f"{self.year}/{self.post_id}.md")
        if not post_path.exists():
            raise NotFound()
        t.blog_header()
        with t.div(class_name="wrapper"):
            with t.div(class_name="postings"):
                t.blog_post(post_md=post_path)
            # t.post_listing(year=self.year)
        t.blog_footer()


@app.page("/posts/<year>")
class YearBlogPosts(Page):
    props = ["year"]

    def populate(self):
        posts = []
        for row in blog_posts:
            if f"0{row['year']}" == self.year:
                posts = sorted(row["posts"], reverse=True)
                break

        if len(posts) < 1:
            raise NotFound()

        t.blog_header(year=self.year)

        with t.div(class_name="wrapper"):
            with t.div(class_name="postings"):
                for post in posts:
                    t.blog_post(post_md=post)
            t.post_listing(year=self.year, posts=posts)
        t.blog_footer()


@app.page()
class BlogHome(Page):

    def populate(self):
        t.blog_header()
        current_year_posts = blog_posts[-1]
        with t.div(class_name="wrapper"):
            with t.div(class_name="postings"):
                for post in sorted(current_year_posts["posts"], reverse=True):
                    t.blog_post(post_md=post)
            t.post_listing()
        with t.div(style="margin-botton: .5em;"):
            t.a(
                f"Prior Year >>",
                class_name="button",
                href=f"/#posts/0{current_year_posts['year']-1}"
            )
            t.br()
        t.blog_footer()


app.mount("#app")