import asyncio
import sys
from playwright.async_api import async_playwright
from recognizer.agents.playwright import AsyncChallenger


async def main():
    async with async_playwright() as p:

        if len(sys.argv) != 3:
            print("Usage: python3 shopee.py [username] [password]")
            return

        username = sys.argv[1]
        password = sys.argv[2]

        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
            viewport={"width": 460, "height": 667},
        )
        page = await ctx.new_page()

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

                if await challenger.check_captcha_visible():
                    print("recapcha ....")
                    await page.wait_for_timeout(2000)
                    await challenger.solve_recaptcha()
                break

            except RecursionError as e:
                print(f"RecursionError occurred: {e}")
                break

            except Exception as e:
                print(f"Error occurred: {e}")
                if "Invisible reCaptcha Timed Out." in str(e):
                    break
                else:
                    await page.reload()

        await page.reload()
        print("success login")
        while True:
            try:
                print("load page")
                await page.wait_for_timeout(5000)
                await page.goto("https://app.golike.net/jobs/shopee")

                await page.wait_for_load_state("networkidle")
                await page.wait_for_timeout(2000)
                print("apply job")
                await page.get_by_text("Nhận Job ngay").click()
                await page.wait_for_timeout(2000)

                async with page.expect_popup() as page1_info:
                    await page.get_by_role("link", name="Trình duyệt").click()

                page1 = await page1_info.value
                await page1.wait_for_timeout(10000)
                await page1.close()

                await page.wait_for_timeout(2000)
                await page.get_by_role("button", name="Hoàn thành").click()

                print("recapcha ....")
                await page.wait_for_timeout(2000)
                await challenger.solve_recaptcha()
                print("success job")
                await page.wait_for_timeout(5000)

            except Exception as e:
                print(f"Error occurred: {e}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
