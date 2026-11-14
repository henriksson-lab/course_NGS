#!/usr/bin/env python3
"""Download a Wikimedia Commons photo, but only on a licence we may actually use.

Records author, licence and source in img/CREDITS.tsv so the credits page can be
generated from data rather than from memory. Refuses anything not on the allowlist,
and refuses to write a file whose licence it could not read.

  python3 tools/fetch_photo.py "File:Illumina MiSeq.jpg" miseq
"""
import json
import os
import re
import sys
import urllib.parse
import urllib.request

API = "https://commons.wikimedia.org/w/api.php"
UA = "course-NGS-build/1.0 (teaching material; contact via repository)"
OK_LICENCES = {"cc0", "cc-by-2.0", "cc-by-2.5", "cc-by-3.0", "cc-by-4.0",
               "cc-by-sa-2.0", "cc-by-sa-3.0", "cc-by-sa-4.0", "public domain"}
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDITS = os.path.join(ROOT, "img", "CREDITS.tsv")


def clean(h):
    return re.sub(r"\s+", " ", re.sub("<[^>]+>", "", h or "")).strip()


def get(title, width=1100):
    q = {"action": "query", "titles": title, "prop": "imageinfo", "format": "json",
         "iiprop": "url|extmetadata|size", "iiurlwidth": str(width)}
    req = urllib.request.Request(API + "?" + urllib.parse.urlencode(q), headers={"User-Agent": UA})
    pages = json.load(urllib.request.urlopen(req, timeout=60))["query"]["pages"]
    page = next(iter(pages.values()))
    if "imageinfo" not in page:
        raise SystemExit("no such file: %s" % title)
    ii = page["imageinfo"][0]
    m = ii.get("extmetadata", {})
    lic = clean(m.get("LicenseShortName", {}).get("value", ""))
    return {
        "title": page["title"],
        "licence": lic,
        "licence_key": lic.lower().replace(" ", "-"),
        "licence_url": clean(m.get("LicenseUrl", {}).get("value", "")),
        "author": clean(m.get("Artist", {}).get("value", "")),
        "credit": clean(m.get("Credit", {}).get("value", "")),
        "descr": clean(m.get("ImageDescription", {}).get("value", ""))[:200],
        "url": ii.get("thumburl") or ii["url"],
        "page": ii["descriptionurl"],
    }


def main():
    title, slug = sys.argv[1], sys.argv[2]
    width = int(sys.argv[3]) if len(sys.argv) > 3 else 1100
    info = get(title, width)
    key = info["licence_key"]
    if not any(key.startswith(k) or key == k for k in OK_LICENCES):
        raise SystemExit("REFUSED: licence %r is not on the allowlist (%s)"
                         % (info["licence"], title))
    if not info["author"]:
        raise SystemExit("REFUSED: no author recorded, so it cannot be attributed (%s)" % title)
    ext = os.path.splitext(info["url"])[1].split("?")[0].lower() or ".jpg"
    if ext not in (".jpg", ".jpeg", ".png"):
        ext = ".jpg"
    out = os.path.join(ROOT, "img", slug + ext)
    req = urllib.request.Request(info["url"], headers={"User-Agent": UA})
    data = urllib.request.urlopen(req, timeout=120).read()
    with open(out, "wb") as fh:
        fh.write(data)
    new = not os.path.exists(CREDITS)
    with open(CREDITS, "a") as fh:
        if new:
            fh.write("file\ttitle\tauthor\tlicence\tlicence_url\tsource\n")
        fh.write("\t".join([os.path.basename(out), info["title"], info["author"],
                            info["licence"], info["licence_url"], info["page"]]) + "\n")
    print("ok  %-26s %-13s %s" % (os.path.basename(out), info["licence"], info["author"][:40]))
    print("    %s  (%d kB)" % (info["page"], len(data) // 1024))


if __name__ == "__main__":
    main()
