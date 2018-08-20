#!/usr/bin/env python
# -*- coding:UTF-8 -*-
import pytest
import sys
import os
project_folder = os.getcwd()[0:os.getcwd().find("ui_auto_test")]
sys.path.append(project_folder+"ui_auto_test/src")
sys.path.append(project_folder+"ui_auto_test/src/touch")
import helper


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    summary = []
    extra = getattr(report, 'extra', [])
    if report.when == 'call' and not report.passed:
        try:
            screenshot = helper.get_appium().get_screenshot_as_base64()
        except Exception as e:
            summary.append('WARNING: Failed to gather screenshot: {0}'.format(e))
            return
        if pytest_html is not None:
            # add screenshot to the html report
            extra.append(pytest_html.extras.image(screenshot, 'Screenshot'))
