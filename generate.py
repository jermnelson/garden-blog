__author__ = "Jeremy Nelson"

import copy
import datetime
import os
import pathlib

import jinja2
import xml.etree.ElementTree as etree
import markdown

from bs4 import BeautifulSoup

BLOG_URI = "https://jermnelson.github.io/garden-blog/"


env = jinja2.Environment(
    loader=jinja2.FileSystemLoader("templates"),
    autoescape=jinja2.select_autoescape()
)

def absolute_urls(elements):
    for element in elements:
        element['src'] = f"{BLOG_URI}{element['src']}"

def generate_year_page(year: pathlib.Path):
    for post in year.glob("*.md"):
        print(post.name)
        month_template = env.get_template("index.html")
        generate_month_page(month)
       

        month, day = post.name.split(".")[0].split("-")
        print(f"Month {month}, Day {day}")
        if (month / ".html").exists():
            continue
        generate_month_page(month)

def generate_post(post: pathlib.Path):
    if post.exists(): # and Github commit hasn't changed
        return
    with post_path.open() as fo:
        post_html = markdown.markdown(fo.read())
    with post_path.open('w+') as fo:
        fo.write(post_html)

def generate_years(years: list):
    for year in years:
        year_page, month_page = year / f"{year.name}.html", []
        generate_year_page(year)
        if not year_page.exists():
            print(f"{year}.html does not exist")
            continue  # Need to check for month pages
        print(year_page)

def get_html_template():
    return
    #with open("index-template.html") as fo:
    #    template = fo.read()
    #return BeautifulSoup(template, features="html.parser")

def create_post_html(**kwargs):
    post: pathlib.Path = kwargs['post']
    year: str = kwargs["year"]
    month: str = kwargs["month"]
    day: kwargs["day"]

    if post.exists():
        return

    with post.open() as fo:
        post_html = markdown.markdown(fo.read())
 
    post_path = pathlib.Path(f"0{year:05d}/{month:02}/{day:02}/index.html")
    post_path.mkdir(exists=True)
    if post_path.exists():
        return
    post_date = datetime.datetime(year, month, day)
    post_template = env.get_template("index.html")

    with post_path.open("w+") as fo:
        fo.write(
            post_template.render(
              page={"title":  f"""{h1_title.text.strip()} - {post.strftime("%b %d, %Y")}""",
                    "posts": [{ "href": f"{BLOG_URI}{post_path}",
                                "date": post_date.strftime("%b %d, %Y"),
                                "html": post_html }]}
            )
        )

    return
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

def year_blog(years: list):
    for year in years:
        year_page, month_page = year / f"{year.name}.html", []
        generate_year_page(year)
        if not year_page.exists():
            print(f"{year}.html does not exist")
            continue  # Need to check for month pages
        print(year_page)

index = get_html_template()
rss_xml = etree.fromstring("""<rss version="2.0" />""")
channel = etree.SubElement(rss_xml, "channel")
link = etree.SubElement(channel, "link")
link.text = BLOG_URI
title = etree.SubElement(channel, "title")
title.text = "Garden Reflections"
description = etree.SubElement(channel, "description")
description.text = "A blog by Jeremy Nelson"
#postings = index.find("div", class_="postings")
#latest = index.find("ul", class_="latest")
#footer = index.find("footer")
#timestamp = index.new_tag("span")
published_now = datetime.datetime.utcnow()
#timestamp.string = f"Last updated on {published_now.isoformat()}"
#footer.append(timestamp)
years = [year for year in pathlib.Path("posts").glob("02*")]
#breakpoint()

year_blog(years)

with open("rss.xml", "wb+") as fo:
   fo.write(etree.tostring(rss_xml)) 
    
#with open("index.html", "w+") as fo:
#    fo.write(index.prettify())
