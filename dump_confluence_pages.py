#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: zhipeng
# @Email: zhipeng.py@gmail.com
# @Date:   2022-10-13 18:07:22
# @Last Modified By:    zhipeng
# @Last Modified: 2022-10-14 17:14:20

import os
import requests
import simplejson as json

cookie = "PUT Cookie AT HERE"
base_domain = 'https://community.atlassian.net'
url = '%s/wiki/pages/children.action?' % base_domain
dump_dir = './confluence/'

req = requests.session()

def crawler_space_pages(name="", page_id=None):
    pages = {}
    if page_id:
        res = req.get(url, params={'pageId': page_id}, headers={'cookie': cookie})
    else:
        res = req.get(url, params={'spaceKey': name, 'node': 'root'}, headers={'cookie': cookie} )
    try:
        page_list = json.loads(res.content)
        if not page_id and not page_list:
            print ('space pages empty, check it. key: %s' % name)
    except:
        print (res.content)
    # [{"nodeClass":"closed","text":"page title","position":1111,"href":"/wiki/spaces/XXXXX/overview","pageId":"2222","linkClass":"home-node"}]
    for page in page_list:
        page_url = (base_domain + page['href'])
        page['url'] = page_url
        print ('fetch page: %s' % page_url)
        crawler_space_html(page)
        if page["nodeClass"] == "closed":
            sub_pages = crawler_space_pages(page_id=page['pageId'])
            pages.update(sub_pages)
        pages[page['pageId']] = page
    return pages


def crawler_space_html(page, end_with_html=False):
    full_path = os.path.join(dump_dir, page['href'][1:])
    dir_path, file_name = os.path.split(full_path)
    try:
        os.makedirs(dir_path)
    except:
        pass
    res = req.get(page['url'], headers={'cookie': cookie})
    if end_with_html:
        full_path = full_path + '.html'
    with open(full_path, 'wb') as f:
        f.write(res.content)


if __name__ == "__main__":
    # https://community.atlassian.net/cgraphql?q=SpaceDirectorySpacesQuery
    spaces = [
        (u'RD', u'R&D'),
    ]
    for key, name in spaces:
        print ('process key: %s, name: %s' % (key, name))
        pages = crawler_space_pages(name=key)
