from playwright.sync_api import Playwright, sync_playwright


def run(playwright: Playwright) -> None:
    global account_number
    account_number = 0

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
        viewport={"width": 460, "height": 667},
    )
    page = context.new_page()
    page.goto("https://app.golike.net/login")
    page.locator('input[type="text"]').click()
    page.locator('input[type="text"]').click()
    page.locator('input[type="text"]').fill("giauphanbii")
    page.locator('input[type="text"]').press("Enter")
    page.locator('input[type="password"]').fill("giauvip12345")
    page.locator('input[type="password"]').press("Enter")

    page.wait_for_timeout(30000)
    for __ in range(5):
        element = page.get_by_text("Chọn tài khoảnKiếm Tiền").first
        element.click()

        select_account = page.locator(".page-container .container").all()
        print(len(select_account))

        number = 0
        for account in select_account:
            try:
                name = account.locator("span").inner_text()

                if number == account_number:
                    # page.locator("span").filter(has_text=f"{name}check").locator("span").click() # change account shoppe
                    page.get_by_text(f"{name}").click()
                    account_number += 1
                number += 1
            except Exception as e:
                print(e)

        

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
