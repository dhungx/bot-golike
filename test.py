from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.webkit.launch(
        headless=False,
        proxy={
            "server": "181.129.43.3:8080",
        },
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
