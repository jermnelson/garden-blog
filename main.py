import datetime
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

    def post_nav(self):
        with t.div(class_name="post_nav"):
            t.a(
                f"Home",
                href="/"
            )
            t.span(" >> ")
            t.a(
                f"{self.year}",
                href=f"/garden-blog/#posts/{self.year}"
            )
            t.span(f" >> {self.post_id}")


    def populate(self):
        post_path = pathlib.Path(f"{self.year}/{self.post_id}.md")
        if not post_path.exists():
            raise NotFound()
        t.blog_header()

        with t.div(class_name="wrapper"):
            with t.div(class_name="postings"):
                t.blog_post(post_md=post_path)
            with t.div(class_name="listing"):
                self.post_nav()
        t.blog_footer()


@app.page("/posts/<year>")
class YearBlogPosts(Page):
    props = ["year"]

    def nav_buttons(self):
        current_date = datetime.datetime.now(datetime.UTC)
        year = int(self.year)
        with t.div(class_name="nav"):
            if year < current_date.year:
                t.a(
                    f"<< Next Year",
                    class_name="button",
                    href=f"/#posts/0{year+1}"
                )
            if year > 2019:
                t.a(
                    f"Prior Year >>",
                    class_name="button",
                    href=f"/#posts/0{year-1}"
                )


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
        self.nav_buttons()
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
        with t.div(class_name="nav"):
            t.a(
                f"Prior Year >>",
                class_name="button",
                href=f"/garden-blog/#posts/0{current_year_posts['year']-1}"
            )
            t.br()
        t.blog_footer()


app.mount("#app")