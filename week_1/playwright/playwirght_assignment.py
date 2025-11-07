import asyncio
from playwright.async_api import async_playwright, TimeoutError

async def run():
    async with async_playwright() as p:
        # Launch browser (visible)
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # Step 1: Go to DuckDuckGo
        await page.goto("https://duckduckgo.com")

        # Step 2: Wait for 2 seconds before searching
        await page.wait_for_timeout(2000)

        # Step 3: Search for the match
        search_text = "Ind vs SA women's final"
        await page.locator("//*[@id='searchbox_input']").fill(search_text)
        await page.keyboard.press("Enter")

        # Step 4: Wait for search results
        await page.wait_for_selector("a[data-testid='result-title-a']", timeout=10000)

        # Step 5: Click on the Cricbuzz link (first matching link)
        cricbuzz_link = page.locator("a[data-testid='result-title-a']", has_text="Cricbuzz").first
        if await cricbuzz_link.count() > 0:
            await cricbuzz_link.click()
        else:
            print("⚠️ Cricbuzz link not found. Clicking first link instead.")
            await page.locator("a[data-testid='result-title-a']").first.click()

        # Step 6: Wait 3 seconds to ensure page loads fully
        # await page.wait_for_timeout(3000)

        # Step 7: Take a full-page screenshot
        screenshot_name = "cricbuzz_final.png"
        try:
            # networkidle may never be reached on some sites (ads, long-polling).
            # wait up to 30s (default) then fall back to 'load' state.
            await page.wait_for_load_state("networkidle")
        except TimeoutError:
            print("⚠️ wait_for_load_state('networkidle') timed out. Falling back to 'load' state.")
            try:
                await page.wait_for_load_state("load", timeout=10000)
            except TimeoutError:
                print("⚠️ Fallback wait_for_load_state('load') also timed out. Proceeding to take a screenshot anyway.")

        await page.screenshot(path=screenshot_name, full_page=True)

        print(f"✅ Screenshot saved as '{screenshot_name}'")

        # Step 8: Close browser (ensure awaited)
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
