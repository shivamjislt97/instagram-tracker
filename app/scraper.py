from playwright.sync_api import sync_playwright


def fetch_profile(insta_url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto(insta_url, timeout=60000, wait_until="domcontentloaded")
        except Exception as e:
            print("❌ Instagram page load failed:", e)
            browser.close()
            return {
                "bio": None,
                "image": None
            }

        page.wait_for_timeout(3000)

        # Bio
        try:
            bio = page.locator("header section div span").last.text_content()
        except:
            bio = None

        # Profile image
        try:
            image = page.locator("header img").first.get_attribute("src")
        except:
            image = None

        browser.close()

        return {
            "bio": bio,
            "image": image
        }
