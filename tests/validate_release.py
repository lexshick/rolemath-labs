from __future__ import annotations

import csv
import hashlib
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[1]
INDEXABLE = {
    "/rolemath-labs/": ROOT / "index.html",
    "/rolemath-labs/data/": ROOT / "data" / "index.html",
    "/rolemath-labs/methodology/": ROOT / "methodology" / "index.html",
    "/rolemath-labs/case-study/": ROOT / "case-study" / "index.html",
}
FIT_CHECK = ROOT / "fit-check" / "index.html"


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.h1 = 0
        self.links: list[str] = []
        self.forms = 0
        self.meta: list[dict[str, str]] = []
        self.canonicals: list[str] = []
        self.jsonld: list[str] = []
        self._jsonld = False
        self._buffer: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {key: value or "" for key, value in attrs}
        if tag == "h1":
            self.h1 += 1
        elif tag == "a" and attr.get("href"):
            self.links.append(attr["href"])
        elif tag == "form":
            self.forms += 1
        elif tag == "meta":
            self.meta.append(attr)
        elif tag == "link" and "canonical" in attr.get("rel", ""):
            self.canonicals.append(attr.get("href", ""))
        elif tag == "script" and attr.get("type") == "application/ld+json":
            self._jsonld = True
            self._buffer = []

    def handle_data(self, data: str) -> None:
        if self._jsonld:
            self._buffer.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self._jsonld:
            self.jsonld.append("".join(self._buffer))
            self._jsonld = False


def parse(path: Path) -> tuple[str, PageParser]:
    text = path.read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(text)
    return text, parser


def local_target(href: str) -> Path | None:
    parsed = urlsplit(href)
    if parsed.scheme or parsed.netloc or not parsed.path.startswith("/rolemath-labs/"):
        return None
    rel = parsed.path.removeprefix("/rolemath-labs/")
    target = ROOT / rel
    return target / "index.html" if parsed.path.endswith("/") else target


def main() -> None:
    errors: list[str] = []
    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    robots_text = (ROOT / "robots.txt").read_text(encoding="utf-8")
    sitemap_urls = set(re.findall(r"<loc>([^<]+)</loc>", sitemap))
    expected = {f"https://lexshick.github.io{route}" for route in INDEXABLE}
    if sitemap_urls != expected:
        errors.append(f"sitemap mismatch: {sitemap_urls ^ expected}")
    if "Disallow: /rolemath-labs/fit-check/" in robots_text:
        errors.append("robots.txt blocks the Fit Check and would hide its noindex directive")

    all_pages = [*INDEXABLE.values(), FIT_CHECK]
    for route, path in INDEXABLE.items():
        text, page = parse(path)
        robots = [meta.get("content", "").lower() for meta in page.meta if meta.get("name") == "robots"]
        canonical = f"https://lexshick.github.io{route}"
        if robots != ["index, follow"]:
            errors.append(f"{route}: robots {robots}")
        if page.canonicals != [canonical]:
            errors.append(f"{route}: canonical {page.canonicals}")
        if page.h1 != 1:
            errors.append(f"{route}: {page.h1} H1s")
        if page.forms:
            errors.append(f"{route}: form present")
        if len(page.jsonld) != 1:
            errors.append(f"{route}: expected one JSON-LD block")
        else:
            try:
                json.loads(page.jsonld[0])
            except json.JSONDecodeError as exc:
                errors.append(f"{route}: invalid JSON-LD: {exc}")
        if not all(token in text for token in ('property="og:title"', 'property="og:description"', 'name="twitter:title"')):
            errors.append(f"{route}: incomplete social metadata")

    fit_text, fit = parse(FIT_CHECK)
    fit_robots = [meta.get("content", "").lower() for meta in fit.meta if meta.get("name") == "robots"]
    if fit_robots != ["noindex, follow"]:
        errors.append(f"fit check robots: {fit_robots}")
    if "fit-check" in sitemap:
        errors.append("fit check is in sitemap")
    js = (ROOT / "assets" / "fit-check.js").read_text(encoding="utf-8")
    for forbidden in ("fetch(", "XMLHttpRequest", "localStorage", "sessionStorage"):
        if forbidden in js:
            errors.append(f"fit check forbidden behavior: {forbidden}")
    if fit.forms or re.search(r'type=["\']email', fit_text, re.I):
        errors.append("fit check contains lead capture")

    for page_path in all_pages:
        _, page = parse(page_path)
        for href in page.links:
            target = local_target(href)
            if target is not None and not target.exists():
                errors.append(f"{page_path.relative_to(ROOT)}: missing target {href}")

    checksum_lines = (ROOT / "checksums.txt").read_text(encoding="utf-8").splitlines()
    for line in checksum_lines:
        if not line.strip():
            continue
        digest, filename = line.split(maxsplit=1)
        target = ROOT / filename.lstrip("*")
        # The repository declares LF as the canonical Git/Pages serialization. Windows
        # checkouts may materialize CRLF despite that contract, so validate the served bytes.
        canonical = target.read_bytes().replace(b"\r\n", b"\n")
        actual = hashlib.sha256(canonical).hexdigest()
        if actual != digest:
            errors.append(f"checksum mismatch: {filename}")

    records = json.loads((ROOT / "data" / "certifications.json").read_text(encoding="utf-8"))
    with (ROOT / "data" / "certifications.csv").open(encoding="utf-8", newline="") as handle:
        csv_rows = list(csv.DictReader(handle))
    json_rows = records.get("records", [])
    if records.get("record_count") != 50 or len(json_rows) != 50 or len(csv_rows) != 50:
        errors.append(
            f"dataset count declared={records.get('record_count')} JSON={len(json_rows)} CSV={len(csv_rows)}"
        )
    offers = [offer for record in json_rows for offer in record.get("training_offers", [])]
    offer_records = [record for record in json_rows if record.get("training_offers")]
    if len(offers) != 11 or len(offer_records) != 3:
        errors.append(f"provider observation boundary offers={len(offers)} records={len(offer_records)}")

    if records.get("release", {}).get("version") != "0.2.0":
        errors.append(f"dataset version: {records.get('release', {}).get('version')}")
    saa = next(
        (
            record
            for record in json_rows
            if record.get("credential", {}).get("slug") == "aws-solutions-architect-associate"
        ),
        None,
    )
    renewal = (saa or {}).get("cost", {}).get("renewal", {})
    if renewal.get("fee") is not None or renewal.get("fee_unit") != "route_dependent":
        errors.append(f"AWS SAA renewal cost must remain route-dependent: {renewal}")

    if errors:
        raise SystemExit("\n".join(errors))
    print("PASS: v0.2.0 static release contract; 4 indexable URLs; Fit Check noindex; 50 JSON/CSV records; 11 offers across 3 credential records; no lead capture or Fit Check network/storage behavior.")


if __name__ == "__main__":
    main()
