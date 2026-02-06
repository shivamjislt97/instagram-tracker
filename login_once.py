from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    page.goto("https://www.instagram.com/accounts/login/", timeout=60000)

    print("👉 Instagram login page open ho gaya")
    print("👉 Ab AAP manually username/password type karo")
    print("👉 Login complete hone ke baad 15 second wait karo")

    # Aap manually login karoge
    page.wait_for_timeout(30000)

    # Cookies save
    context.storage_state(path="ig_session.json")
    print("✅ Login session save ho gaya (ig_session.json)")

    browser.close()
