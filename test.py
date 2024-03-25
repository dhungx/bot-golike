from playwright.sync_api import Playwright, sync_playwright, expect
import random
import requests

proxy_list = [
    "2.58.56.39:80",
    "20.210.113.32:8123",
    "50.204.219.230:80",
    "50.175.212.72:80",
    "51.15.242.202:8888",
    "50.174.7.159:80",
    "50.223.239.166:80",
    "50.173.140.149:80",
]


def check_proxy(playwright: Playwright, proxy):
    browser = playwright.chromium.launch(
        headless=False,
        proxy={"server": proxy},
    )

    page = browser.new_page()
    try:
        page.goto("https://httpbin.org/ip")
        ip_address = page.inner_text("#ip")
        print(f"Proxy {proxy} IP: {ip_address}")
        return True
    except Exception as e:
        print(f"Error occurred with proxy {proxy}: {e}")
        return False
    finally:
        browser.close()


def run(playwright: Playwright) -> None:

    responsive_proxies = [
        proxy for proxy in proxy_list if check_proxy(playwright, proxy)
    ]
    print(responsive_proxies)

    if not responsive_proxies:
        print("No responsive proxies found.")
        return

    proxy_server = random.choice(responsive_proxies)

    browser = playwright.chromium.launch(
        headless=False,
        proxy={"server": proxy_server},
    )
    context = browser.new_context(
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
        viewport={"width": 460, "height": 667},
        locale="de-DE",
        timezone_id="Europe/Berlin",
    )

    page = context.new_page()
    page.goto("https://httpbin.org/ip")
    html_content = page.content()
    print(html_content)
    page.wait_for_timeout(200000)

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
