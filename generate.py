__author__ = "Jeremy Nelson"

import datetime
import os

from bs4 import BeautifulSoup
import markdown

with open("index.html") as fo:
    index = BeautifulSoup(fo)

postings = index.find("div", class_="postings")
latest = index.find("ul", class_="latest")
years_walk = next(os.walk(os.path.abspath("posts/")))
years = years_walk[1]
for year in years:
    posts_walk = next(os.walk(os.path.abspath(f"posts/{year}")))
    posts = posts_walk[-1]
    for post in posts:
        blog_ident = f"{year}/{post[0:5]}"
        blog_date = index.new_tag("h2", id=blog_ident)
        blog_date.string = f"{post[0:5]}-{year}"
        postings.append(blog_date)
        with open(os.path.abspath(f"posts/{year}/{post}")) as fo:
            post_html = markdown.markdown(fo.read())
            post_soup = BeautifulSoup(post_html)
            print(post_soup)
            #for element in post_soup.body:
            #    postings.append(element)
        postings.append(index.new_tag("hr"))
#print(index)
