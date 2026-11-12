import urllib.request
from pathlib import Path

COUNTRIES = ["tj", "ru", "uz", "tr", "ir", "af"]
BASE = "https://iptv-org.github.io/iptv/countries/"

all_channels = [
    '#EXTM3U url-tvg="https://epg.one/ru2.xml.gz"'
]
seen = set()

Path("playlists").mkdir(exist_ok=True)

for country in COUNTRIES:
    url = BASE + country + ".m3u"

    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "Obshi-IPTV"}
        )
        data = urllib.request.urlopen(req, timeout=30)
        lines = data.read().decode("utf-8-sig").splitlines()

        result = ["#EXTM3U"]

        for i in range(1, len(lines) - 1):
            if lines[i].startswith("#EXTINF"):
                stream = lines[i + 1].strip()

                if stream.startswith("http"):
                    entry = (lines[i].strip(), stream)

                    if entry not in seen:
                        seen.add(entry)
                        result.extend(entry)
                        all_channels.extend(entry)

        Path(f"playlists/{country}.m3u").write_text(
            "\n".join(result) + "\n", encoding="utf-8"
        )

    except Exception as e:
        print(country, e)

header = [
    "#EXTM3U",
    '#EXTM3U x-tvg-url="https://marufjon2979.github.io/Obshi_IPTV/epg.xml"'
]

Path("playlist.m3u").write_text(
    "\n".join(header + all_channels[1:]) + "\n",
    encoding="utf-8"
)

print("Playlist generated")
