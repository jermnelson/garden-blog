__author__ = "Jeremy Nelson"

import datetime
import os

from bs4 import BeautifulSoup
import markdown

with open("index-template.html") as fo:
    index = BeautifulSoup(fo)

postings = index.find("div", class_="postings")
latest = index.find("ul", class_="latest")
footer = index.find("footer")
timestamp = index.new_tag("span")
timestamp.string = f"Last updated on {datetime.datetime.utcnow().isoformat()}"
footer.append(timestamp)
years_walk = next(os.walk(os.path.abspath("posts/")))
years = years_walk[1]
for year in years:
    posts_walk = next(os.walk(os.path.abspath(f"posts/{year}")))
    posts = posts_walk[-1]
    for post in posts:
        div_container = index.new_tag("div")
        div_container['class'] = "blog-post"
        blog_ident = f"{year}/{post[0:5]}"
        blog_label = f"{post[0:5]}-{year}"
        blog_date = index.new_tag("h2", id=blog_ident)
        blog_date.string = blog_label
        li_blog = index.new_tag("li")
        li_blog_a = index.new_tag("a", href=f"#{blog_ident}")
        li_blog_a.string = blog_label
        li_blog.append(li_blog_a)
        latest.append(li_blog)
        div_container.append(blog_date)
        with open(os.path.abspath(f"posts/{year}/{post}")) as fo:
            post_html = markdown.markdown(fo.read())
            post_soup = BeautifulSoup(post_html)
            body = post_soup.find('body')
            div_container.append(body)
        postings.append(div_container)
with open("index.html", "w+") as fo:
    fo.write(index.prettify())
