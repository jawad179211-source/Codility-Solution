import time
import csv
import undetected_chromedriver as uc
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException

def scrape_indeed(job_title, location, days_filter):
    chrome_driver_path = r"chromedriver.exe"

    # Chrome Options
    options = uc.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = uc.Chrome(driver_executable_path=chrome_driver_path, options=options)

    # Apply stealth mode
    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win64",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    # -------------------------------
    # Build Search URL
    # -------------------------------
    
    driver.get("https://www.indeed.com")
    time.sleep(5)
    base_url = f"https://www.indeed.com/jobs?q={job_title}&l={location}&fromage={days_filter}"

    driver.get(base_url)
    time.sleep(4)

    all_jobs = []
    page = 1

    while True:
        print(f"\nScraping page {page} ...")

        job_cards = driver.find_elements(By.CSS_SELECTOR, "div.cardOutline")

        if not job_cards:
            print("No jobs found on this page.")
            break

        for job in job_cards:
            try:
                title = job.find_element(By.CSS_SELECTOR, "h2.jobTitle").text.strip()
            except:
                title = ""

            try:
                company = job.find_element(By.CSS_SELECTOR, '[data-testid="company-name"]').text.strip()
            except:
                company = ""

            try:
                location = job.find_element(By.CSS_SELECTOR, '[data-testid="text-location"]').text.strip()
            except:
                location = ""


            try:
                job_url = job.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            except:
                job_url = ""

            all_jobs.append([title, company, location, job_url])

        # ---------------------------
        # Pagination
        # ---------------------------
        try:
            next_btn = driver.find_element(By.CSS_SELECTOR, "a[aria-label='Next']")
            next_btn.click()
            time.sleep(3)
            page += 1

        except NoSuchElementException:
            print("No more pages.")
            break

    driver.quit()

    # ---------------------------
    # Save to CSV
    # ---------------------------
    if all_jobs:
        with open("indeed_jobs.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Job Title", "Company", "Location", "Job URL"])
            writer.writerows(all_jobs)

        print("\n✅ Scraping Completed!")
        print("📁 Data saved in: indeed_jobs.csv")
    else:
        print("\n⚠ No jobs found. CSV not created.")

# --------------------------------------
# RUN SCRAPER
# --------------------------------------
scrape_indeed("python developer", "Remote", 7)