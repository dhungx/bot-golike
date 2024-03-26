import asyncio
from recognizer.agents.playwright import AsyncChallenger
from playwright.async_api import async_playwright
import sys
from playwright.sync_api import TimeoutError



async def accountComplete(page, number_account):
    try:
        await page.get_by_text("Hiện tại chưa có jobs mới,vui").click(timeout=5000)
        await page.get_by_role("button", name="OK").click(timeout=5000)
        element = page.get_by_text("Chọn tài khoảnKiếm Tiền").first
        element.click()

        select_account = page.locator(".page-container .container").all()
        print(len(select_account))

        number = 0
        for account in select_account:
            try:
                name = account.locator("span").inner_text()

                if number == number_account:
                    # page.locator("span").filter(has_text=f"{name}check").locator("span").click() # change account shoppe
                    page.get_by_text(f"{name}").click()
                    return True
                number += 1
            except Exception as e:
                print(f"Error occurred change account: {e}")
        return False
    except TimeoutError:
        return False


async def check_captcha_visible(page):
    captcha_frame = page.frame_locator("//iframe[contains(@src,'bframe')]")
    label_obj = captcha_frame.locator("//strong")
    try:
        await label_obj.wait_for(state="visible", timeout=10000)
    except TimeoutError:
        return False


async def main():
    async with async_playwright() as p:
        number_account = 0

        browser = await p.webkit.launch(
            headless=False,
        )
        ctx = await browser.new_context(
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
            viewport={"width": 460, "height": 667},
        )
        page = await ctx.new_page()

        if len(sys.argv) != 3:
            print("Usage: python3 run_bot.py [username] [password]")
            sys.exit(1)
        username = sys.argv[1]
        password = sys.argv[2]

        challenger = AsyncChallenger(page)
        for __ in range(3):
            try:
                print("access login")

                await page.goto("https://app.golike.net/login")
                await page.wait_for_timeout(2000)
                await page.locator('input[type="text"]').click()
                await page.locator('input[type="text"]').fill(username)
                await page.locator('input[type="password"]').fill(password)
                await page.locator('input[type="password"]').press("Enter")

                if challenger.check_captcha_visible:
                    print("recapcha ....")
                    await page.wait_for_timeout(2000)
                    await challenger.solve_recaptcha()
                    
                await page.wait_for_timeout(2000)
                break

            except TimeoutError:
                return False
            
            except RecursionError as e:
                print(f"RecursionError occurred: {e}")
                break

            except Exception as e:
                print(f"Error occurred: {e}")
                await page.reload()

        await page.reload()
        print("success login")
        while True:
            try:
                print(f"load page - account number: {number_account}")
                await page.wait_for_timeout(5000)
                await page.goto("https://app.golike.net/jobs/Instagram")
                await page.wait_for_timeout(2000)
                await page.get_by_text("Nhận Job ngay").click()
                change_account = await accountComplete(page,number_account)
                if change_account:
                    number_account += 1
                else:
                    number_account = 0
                await page.wait_for_timeout(2000)

                print("apply job")
                async with page.expect_popup() as page1_info:
                    await page.get_by_role("link", name="Instagram").click()

                page1 = await page1_info.value
                await page1.wait_for_timeout(10000)
                await page1.close()

                await page.wait_for_timeout(2000)
                await page.get_by_role("button", name="Hoàn thành").click()

                print("recapcha ....")
                challenger = AsyncChallenger(page)
                await page.wait_for_timeout(2000)
                await challenger.solve_recaptcha()
                print("success job")
                await page.wait_for_timeout(5000)

            except Exception as e:
                print(f"Error occurred: {e}")

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
