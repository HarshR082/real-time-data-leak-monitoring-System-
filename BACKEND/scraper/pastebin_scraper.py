import httpx
from bs4 import BeautifulSoup

PASTEBIN_ARCHIVE_URL = "https://pastebin.com/archive"

async def fetch_public_pastes():
    """
    Scrapes the latest public pastes from Pastebin Archive.
    Returns:
        List of dicts with LeakEvent-style info.
    """
    pastes = []

    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(PASTEBIN_ARCHIVE_URL, timeout=10)
            r.raise_for_status()

            soup = BeautifulSoup(r.text, "html.parser")
            rows = soup.select("table.maintable tr")

            for row in rows[1:]:  # Skip header row
                cols = row.find_all("td")
                if len(cols) < 2:
                    continue

                link_tag = cols[0].find("a")
                if not link_tag:
                    continue

                paste_link = "https://pastebin.com" + link_tag.get("href")
                paste_title = cols[1].text.strip()

                # Fetch paste content
                paste_content = await fetch_paste_content(client, paste_link)

                # Assemble LeakEvent-style dictionary
                pastes.append({
                    "title": paste_title or "Untitled Paste",
                    "description": paste_content[:500],  # Limit size
                    "severity": "Medium",
                    "source": paste_link
                })

    except Exception as e:
        print(f"[Scraper Error] {e}")

    return pastes


async def fetch_paste_content(client: httpx.AsyncClient, url: str) -> str:
    try:
        r = await client.get(url, timeout=10)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")
        content_div = soup.find("textarea", {"id": "paste_code"})
        return content_div.text.strip() if content_div else ""

    except Exception as e:
        print(f"[Fetch Content Error] {e}")
        return ""
