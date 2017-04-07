# !usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#
# @Author: Brian Cherinka
# @Date:   2017-04-06 15:30:50
# @Last modified by:   Brian Cherinka
# @Last Modified time: 2017-04-07 17:51:47

from __future__ import print_function, division, absolute_import
import os
import pytest
import requests
from flask import url_for
from selenium import webdriver
from marvin.web import create_app
from marvin.tests.web.live_server import live_server

browserstack = os.environ.get('USE_BROWSERSTACK', None)

if browserstack:
    osdict = {'OS X': ['El Capitan', 'Sierra'], 'Windows': ['10', '7']}
    browserdict = {'chrome': ['55', '54', '53'], 'firefox': ['52', '51'], 'safari': ['10', '9.1']}
else:
    osdict = {'OS X': ['El Capitan']}
    browserdict = {'chrome': ['55']}

osstuff = [(k, i) for k, v in osdict.items() for i in v]
browserstuff = [(k, i) for k, v in browserdict.items() for i in v]


@pytest.fixture(params=osstuff)
def osinfo(request):
    return request.param


@pytest.fixture(params=browserstuff)
def browserinfo(request):
    return request.param


@pytest.fixture(scope='session')
def app():
    app = create_app(debug=True, local=True, use_profiler=False)
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
    app.config['LIVESERVER_PORT'] = 8943
    return app


@pytest.fixture(scope='function')
def base_url(live_server):
    return '{0}/marvin2/'.format(live_server.url())


@pytest.fixture(scope='function')
def driver(base_url, osinfo, browserinfo):
    ostype, os_version = osinfo
    browser, browser_version = browserinfo
    if browserstack:
        username = os.environ.get('BROWSERSTACK_USER', None)
        access = os.environ.get('BROWSERSTACK_ACCESS_KEY', None)
        desired_cap = {'os': ostype, 'os_version': os_version, 'browser': browser,
                       'browser_version': browser_version, 'project': 'marvin', 'resolution': '1920x1080'}
        desired_cap['browserstack.local'] = True
        desired_cap['browserstack.debug'] = True
        desired_cap['browserstack.localIdentifier'] = os.environ['BROWSERSTACK_LOCAL_IDENTIFIER']
        driver = webdriver.Remote(
            command_executor='http://{0}:{1}@hub.browserstack.com:80/wd/hub'.format(username, access),
            desired_capabilities=desired_cap)
    else:
        if browser == 'chrome':
            driver = webdriver.Chrome()
        elif browser == 'firefox':
            driver = webdriver.Firefox()
        elif browser == 'safari':
            driver = webdriver.Safari()

    driver.get(base_url)
    yield driver
    # teardown
    driver.quit()


@pytest.mark.usefixtures('live_server')
class TestLiveServer(object):

    def test_server_is_up_and_running(self, base_url):
        response = requests.get(base_url)
        assert response.status_code == 200




