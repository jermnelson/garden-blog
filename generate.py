__author__ = "Jeremy Nelson"

import datetime
import os
import pathlib
from email.utils import format_datetime

from bs4 import BeautifulSoup
import xml.etree.ElementTree as etree
import markdown

BLOG_URI = "https://jermnelson.github.io/garden-blog/"

def absolute_urls(elements):
    for element in elements:
        element['src'] = f"{BLOG_URI}{element['src']}"

def get_post_md(year, post_file):
    post_path = os.path.abspath(f"posts/{year}/{post_file}") 
    with open(post_path) as fo:
        post_html = markdown.markdown(fo.read())
    return post_html

def get_html_template():
    with open("index-template.html") as fo:
        template = fo.read()
    return BeautifulSoup(template, features="html.parser")

def create_post_html(year, month, day, post_file):
    post_path = pathlib.Path(f"{year:05d}/{month:02}/{day:02}/index.html")
    if post_path.exists():
        return
    post_date = datetime.datetime(year, month, day)
    html_page = get_html_template()
    page_soup = BeautifulSoup(html_page, features="html.parser")
    post_html = get_post_md(year, post_file)
    post_soup = BeautifulSoup(post_html, features="html.parser")
    absolute_urls(post_soup.find_all('img'))
    absolute_urls(post_soup.find_all('source'))
    h1_title = page_soup.find("h1", "title")
    h1_title.string = f"""{h1_title.text.strip()} - {post.strftime("%b %d, %Y")}"""
    wrapper = html_page.find("div", "wrapper")
    postings = wrapper.find("div", "postings")
    postings.append(post_soup)



rss_xml = etree.fromstring("""<rss version="2.0" />""")
channel = etree.SubElement(rss_xml, "channel")
link = etree.SubElement(channel, "link")
link.text = BLOG_URI
title = etree.SubElement(channel, "title")
title.text = "Garden Reflections"
description = etree.SubElement(channel, "description")
description.text = "A blog by Jeremy Nelson"

years_walk = next(os.walk(os.path.abspath("posts/")))
years = years_walk[1]
for year in sorted(years, reverse=True):
    posts_walk = next(os.walk(os.path.abspath(f"posts/{year}")))
    posts = sorted(posts_walk[-1])
    for post in reversed(posts):
        if not post.endswith(".md"):
            continue

        post_html = get_post_md(year, post)
        post_soup = BeautifulSoup(post_html, features="html.parser")
        body = post_soup.find('body')
        h1 = (body or post_soup).find('h1')
        if h1 is None:
            print(f"Skipping posts/{year}/{post}, no title found")
            continue

        blog_ident = f"{year}/{post[0:5]}"
        blog_date = datetime.datetime.strptime(blog_ident, "0%Y/%m-%d")

        item = etree.SubElement(channel, 'item')
        link = etree.SubElement(item, "link")
        link.text = f"{BLOG_URI}#posts/{blog_ident}"
        pubDate = etree.SubElement(item, 'pubDate')
        pubDate.text = format_datetime(blog_date)
        author = etree.SubElement(item, 'author')
        author.text = "jermnelson@gmail.com"
        title = etree.SubElement(item, "title")
        title.text = h1.get_text()
        content = body if body is not None else post_soup
        item.append(etree.fromstring(f"<description>{content}</description>"))

with open("rss.xml", "wb+") as fo:
    fo.write(etree.tostring(rss_xml))
