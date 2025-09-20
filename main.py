from puepy import Application, Page, t
from puepy.router import Router

from common import blog_posts

app = Application()
app.install_router(Router, link_mode=Router.LINK_MODE_HASH)

@app.page("/<year>")
class YearBlogPosts(Page):
    props = ["year"]

    

@app.page()
class BlogHome(Page):

    def populate(self):
        t.blog_header()
        with t.div(class_name="wrapper"):
            with t.div(class_name="postings"):
                current_year_posts = blog_posts[-1]
                for post in sorted(current_year_posts["posts"], reverse=True):
                
        t.blog_footer()

