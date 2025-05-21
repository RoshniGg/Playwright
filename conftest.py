import os
import time
from pathlib import Path

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Playwright
from pytest_html import extras
from slugify import slugify

from utils.logger import logger

test_results = []


def pytest_addoption(parser):
    parser.addoption(
        "--browser_option", action="store", default="chrome",
        help="Browser selection"
    )

    parser.addoption(
        "--env", action="store", default="qa",
        help="Test Environment selection: qa, stage, prod"
    )

@pytest.fixture(scope="session", autouse=True)
def load_env(request):
    env = request.config.getoption("--env")
    dotenv_path = f".env.{env}"
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    else:
        raise FileNotFoundError(f"Environment file '{dotenv_path}' not found.")



@pytest.fixture(scope="function")
def browse_open_url(playwright:Playwright,request):
    browser_name =request.config.getoption("--browser_option")
    base_url= os.getenv("BASE_URL")
    # opening browser
    if browser_name == 'chrome':
        browser = playwright.chromium.launch()
    elif browser_name == 'firefox':
        browser = playwright.firefox.launch()

    context = browser.new_context()
    page = context.new_page()

    # navigation to the site
    page.goto(base_url)
    yield page
    context.close()
    browser.close()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    screen_file = ''
    report = outcome.get_result()
    extra = getattr(report, "extra", [])
    if report.when == "call":
        xfail = hasattr(report, "wasxfail")
        if report.failed or xfail and "browse_open_url" in item.funcargs:
            page = item.funcargs.get("browse_open_url")
            screenshot_dir = Path("results/screenshots")
            screenshot_dir.mkdir(exist_ok=True)
            screen_file = str(screenshot_dir / f"{slugify(item.nodeid)}.png")
            screen_shot_file = str(Path("screenshots")/ f"{slugify(item.nodeid)}.png")
            page.screenshot(path=screen_file)

        if (report.skipped and xfail) or (report.failed and not xfail) :
            # add the screenshots to the html report
            extra.append(pytest_html.extras.png(screen_shot_file))
        report.extra = extra

# Hook to log test results during execution
@pytest.hookimpl(trylast=True)
def pytest_runtest_logreport(report):
    if report.when == "call":
        test_name = report.nodeid.split("[")[0]
        outcome = report.outcome
        duration = report.duration
        error_msg = str(report.longrepr) if report.failed else ""

        # Collect the result
        test_results.append([test_name, outcome, duration, error_msg])
        logger.info(f"Test: {test_name} | Result: {outcome} | Duration: {duration:.2f}s")
        if report.failed:
            logger.error(f"Test failed: {test_name} | Error: {error_msg}")