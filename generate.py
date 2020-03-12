__author__ = "Jeremy Nelson"

import datetime
import os

from bs4 import BeautifulSoup
import xml.etree.ElementTree as etree
import markdown

BLOG_URI = "https://jermnelson.github.io/garden-blog/"

with open("index-template.html") as fo:
    template = fo.read()
    index = BeautifulSoup(template, features="html.parser")

rss_xml = etree.fromstring("""<rss version="2.0" />""")
channel = etree.SubElement(rss_xml, "channel")
link = etree.SubElement(channel, "link")
link.text = BLOG_URI
title = etree.SubElement(channel, "title")
title.text = "Garden Reflections"
description = etree.SubElement(channel, "description")
description.text = "A blog by Jeremy Nelson"
postings = index.find("div", class_="postings")
latest = index.find("ul", class_="latest")
footer = index.find("footer")
timestamp = index.new_tag("span")
published_now = datetime.datetime.utcnow()
timestamp.string = f"Last updated on {published_now.isoformat()}"
footer.append(timestamp)
years_walk = next(os.walk(os.path.abspath("posts/")))
years = years_walk[1]
for year in sorted(years, reverse=True):
    posts_walk = next(os.walk(os.path.abspath(f"posts/{year}")))
    posts = sorted(posts_walk[-1])
    for post in reversed(posts):        
        if post.endswith(".swp"):
            continue
        item = etree.SubElement(channel, 'item')
        author = etree.SubElement(channel, 'author')
        author.text = "jermnelson@gmail.com"
        div_container = index.new_tag("div")
        div_container['class'] = "blog-post"
        blog_ident = f"{year}/{post[0:5]}"
        link = etree.SubElement(item, "link")
        link.text = f"{BLOG_URI}#{blog_ident}"
        blog_date = datetime.datetime.strptime(blog_ident, "%Y/%m-%d")
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
        post_path = os.path.abspath(f"posts/{year}/{post}") 
        with open(post_path) as fo:
            post_html = markdown.markdown(fo.read())
        post_soup = BeautifulSoup(post_html, features="html.parser")
        body = post_soup.find('body')
        if body is None:
            h1 = post_soup.find('h1')
        else:
            h1 = body.find('h1')
        title = etree.SubElement(item, "title")
        title.text = h1.string
        #breakpoint()
        if body is None:
            copy_soup = post_soup
            div_container.append(copy_soup)
        else:
            div_container.append(body)
        
        # description = etree.SubElement(item, "description")
        
        postings.append(div_container)

with open("rss.xml", "wb+") as fo:
   fo.write(etree.tostring(rss_xml)) 
    
with open("index.html", "w+") as fo:
    fo.write(index.prettify())
