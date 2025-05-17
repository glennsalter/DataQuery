import csv
from bs4 import BeautifulSoup


def parse_announcements(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    # Find the container using the same XPath logic as Selenium
    container = soup.select_one("body > div:nth-of-type(3) > div > div > div > div > div:nth-of-type(3) > div > div")

    if not container:
        print("Announcements container not found.")
        exit(1)

    # Find all announcement divs inside the container
    announcement_divs = container.select("div.bn-flex")

    messages = []
    for div in announcement_divs:
        a_tag = div.find("a")
        if a_tag:
            messages.append(a_tag.get_text(strip=True))

    # Write to CSV
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["title"])
        for message in messages:
            writer.writerow([message])

    print(f"Number of titles: {len(messages)}")