__author__ = "Jeremy Nelson"

import datetime
import os

from bs4 import BeautifulSoup
import xml.etree.ElementTree as etree
import markdown

with open("index-template.html") as fo:
    index = BeautifulSoup(fo)


rss_xml = etree.fromstring("""<rss version="2.0" />""")
#rss = rss_xml.getroot()
postings = index.find("div", class_="postings")
latest = index.find("ul", class_="latest")
footer = index.find("footer")
timestamp = index.new_tag("span")
published_now = datetime.datetime.utcnow()
timestamp.string = f"Last updated on {published_now.isoformat()}"
footer.append(timestamp)
years_walk = next(os.walk(os.path.abspath("posts/")))
years = years_walk[1]
for year in years:
    posts_walk = next(os.walk(os.path.abspath(f"posts/{year}")))
    posts = sorted(posts_walk[-1])
    for post in reversed(posts):
        item = etree.SubElement(rss_xml, 'item')
        if post.endswith(".swp"):
            continue
        div_container = index.new_tag("div")
        div_container['class'] = "blog-post"
        blog_ident = f"{year}/{post[0:5]}"
        blog_label = f"{post[0:5]}-{year}"
        pubDate = etree.SubElement(item,'pubDate')
        pubDate.text = f"{year}-{post[0:5]}"
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
            title = etree.SubElement(item, "title")
            h1 = body.find('h1')
            title.text = h1.string
        postings.append(div_container)
with open("rss.xml", "wb+") as fo:
   fo.write(etree.tostring(rss_xml)) 
    
with open("index.html", "w+") as fo:
    fo.write(index.prettify())
