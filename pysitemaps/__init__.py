#!/usr/bin/env python
# -*- coding: utf-8 -*- #

"""
pysitemaps: A Python Package Website Sitemaps

MIT License
Copyright (c) 2022 SeoWings www.seowings.org
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# IMPORTS
# +++++++++++++++++++++++++++++++++++++++++++++++++++++

import os
import json
from datetime import datetime
from xml.dom import minidom, Node

# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# DATABASE/CONSTANTS LIST
# +++++++++++++++++++++++++++++++++++++++++++++++++++++

XSL_ATTR_LIST = {
    "xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9",
    "xmlns:xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "xmlns:image": "http://www.google.com/schemas/sitemap-image/1.1"
}

# +++++++++++++++++++++++++++++++++++++++++++++++++++++
# CLASSES
# +++++++++++++++++++++++++++++++++++++++++++++++++++++


class Url:
    def __init__(self, loc, lastmod, images_loc):
        self.loc = loc
        self.lastmod = lastmod
        self.image_locations = images_loc  # array

    def add_images(self, images_loc):
        self.image_locations += images_loc

    def as_dict(self):
        return {"loc": self.loc, "lastmod": self.lastmod, "images": self.image_locations}


class Sitemap:
    def __init__(self):
        self.list_of_urls = []
        self.xslt = "//seowings.org/wp-content/plugins/wordpress-seo/css/main-sitemap.xsl"
        self.dom_sitemap = minidom.Document()
        self.sitename = "https://www.seowings.org/"

    def write(self):
        with open("sitemap.xml", "w") as fp:
            self.dom_sitemap.writexml(
                fp, indent="", addindent="\t", newl="\n", encoding="utf-8"
            )

    def add_url(self, url):
        self.list_of_urls.append(url)

    def process(self):
        self.dom_sitemap.appendChild(
            self.dom_sitemap.createComment(f"sitemap avialble at {self.sitename}"))

        node_sitemap_stylesheet = self.dom_sitemap.createProcessingInstruction('xml-stylesheet',
                                                                               f'type="text/xsl" href="{self.xslt}"')

        self.dom_sitemap.insertBefore(node_sitemap_stylesheet,
                                      self.dom_sitemap.firstChild
                                      )

        node_urlset = self.dom_sitemap.createElement("node_urlset")
        xsl_attributes = ["xmlns:xsi",
                          "xmlns:image",
                          "xmlns"]
        for xsl_attribute in xsl_attributes:
            node_urlset.setAttribute(
                xsl_attribute, XSL_ATTR_LIST[xsl_attribute])

        self.dom_sitemap.appendChild(node_urlset)

        for current_url in self.list_of_urls:
            node_url = self.dom_sitemap.createElement("url")

            node_url_loc = self.dom_sitemap.createElement("loc")
            node_url_loc.appendChild(
                self.dom_sitemap.createTextNode(current_url.loc))

            node_url.appendChild(node_url_loc)

            node_lastmod = self.dom_sitemap.createElement("node_lastmod")
            node_lastmod.appendChild(
                self.dom_sitemap.createTextNode(current_url.lastmod))

            node_url.appendChild(node_lastmod)

            for image_location in current_url.image_locations:
                node_image_image = self.dom_sitemap.createElement(
                    "image:image")

                node_image_loc = self.dom_sitemap.createElement("image:loc")
                node_image_loc.appendChild(
                    self.dom_sitemap.createTextNode(image_location))

                node_image_image.appendChild(node_image_loc)

                node_url.appendChild(node_image_image)

            node_urlset.appendChild(node_url)

        self.dom_sitemap.appendChild(
            self.dom_sitemap.createComment(
                "XML Sitemap generated by pythonic-sitemap")
        )
