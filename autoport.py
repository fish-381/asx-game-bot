import asyncio
import os
from pyppeteer import launch
from dotenv import load_dotenv

async def login_with_pyppeteer():
    # Load environment variables
    load_dotenv()

    # Get username and password from .env file
    username = os.getenv("LOGID")
    password = os.getenv("PASSWORD")

    if not username or not password:
        print("Username or password not found in .env file.")
        return

    # Launch browser
    browser = await launch(headless=False)  # Change to headless=True for headless mode
    page = await browser.newPage()

    try:
        # Navigate to the login page
        await page.goto("https://game.asx.com.au/game/student/school/2024-1/login", {"waitUntil": "networkidle0"})

        # Type username with a delay
        await page.type("#studentLoginForm\:loginId", username, {'delay': 100})  # Adjust the delay value as needed

        # Type password with a delay
        await page.type("#studentLoginForm\:password", password, {'delay': 100})  # Adjust the delay value as needed

        # Click on the login button
        await page.click("#studentLoginForm\:j_idt369")

        # Wait for navigation to complete
        await page.waitForNavigation({"waitUntil": "networkidle0"})

        # Wait until no network traffic and the page is loaded
        await page.waitForSelector("#j_idt400\:j_idt432\:j_idt440")
        await page.click("#j_idt400\:j_idt432\:j_idt440")
        await page.waitForNavigation({"waitUntil": "networkidle0"})

        # Click on #more-table
        await page.waitForSelector("#more-table")
        await page.click("#more-table")
        await page.waitForNavigation({"waitUntil": "networkidle0"})

        # Extract code and holding amount
        code = await page.evaluate('''
            () => {
                const codeElement = document.querySelector("#portfolioForm\\:j_idt403\\:0\\:j_idt405\\:j_idt407");
                return codeElement ? codeElement.innerText : null;
            }
        ''')

        holding_amount = await page.evaluate('''
            () => {
                const amountElement = document.querySelector("#table-view > tbody > tr");
                return amountElement ? amountElement.children[1].innerText : null;
            }
        ''')

        print("Code:", code)
        print("Holding Amount:", holding_amount)

    finally:
        # Close the browser
        await browser.close()

# Run the async function
asyncio.get_event_loop().run_until_complete(login_with_pyppeteer())
