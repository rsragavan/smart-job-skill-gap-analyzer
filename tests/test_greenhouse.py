from app.scraper.greenhouse import GreenhouseScraper


def main():
    scraper = GreenhouseScraper()

    # Temporary test URL
    url = "https://job-boards.greenhouse.io/sonos"

    html = scraper.fetch_html(url)

    if html:
        print("\n✅ HTML downloaded successfully!")
        print(f"HTML Length: {len(html)} characters")
        print("\nFirst 1000 characters:\n")
        print(html[:1000])
    else:
        print("\n❌ Failed to download HTML.")

    scraper.close()


if __name__ == "__main__":
    main()