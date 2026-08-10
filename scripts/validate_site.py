#!/usr/bin/env python3
"""Fail-closed validation for the static RoleMath Labs release.

The validator intentionally uses only the Python standard library so it can run
locally or in GitHub Actions without installing a dependency stack.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://lexshick.github.io/rolemath-labs"

INDEXABLE_PAGES = {
    Path("index.html"): f"{BASE_URL}/",
    Path("case-study/index.html"): f"{BASE_URL}/case-study/",
    Path("methodology/index.html"): f"{BASE_URL}/methodology/",
    Path("data-dictionary/index.html"): f"{BASE_URL}/data-dictionary/",
}
NOINDEX_PAGES = {
    Path("fit-check/index.html"): f"{BASE_URL}/fit-check/",
}
EXPECTED_DATA_FILES = {
    "data/certifications.json",
    "data/certifications.csv",
    "data/field_dictionary.json",
}
EXPECTED_RECORD_COUNT = 50
EXPECTED_LIVE_URLS = 28
EXPECTED_NULL_URLS = 22
EXPECTED_SITEMAP_ROUTE_COUNT = 310


class ValidationError(RuntimeError):
    """Raised when a release invariant is violated."""


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.html_lang = ""
        self.titles: list[str] = []
        self.in_title = False
        self.title_parts: list[str] = []
        self.meta: list[dict[str, str]] = []
        self.canonicals: list[str] = []
        self.links: list[str] = []
        self.scripts: list[dict[str, str]] = []
        self.h1_count = 0
        self.in_json_ld = False
        self.json_ld_parts: list[str] = []
        self.json_ld_blocks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value or "" for key, value in attrs}
        tag = tag.lower()
        if tag == "html":
            self.html_lang = values.get("lang", "")
        elif tag == "title":
            self.in_title = True
            self.title_parts = []
        elif tag == "meta":
            self.meta.append(values)
        elif tag == "link":
            href = values.get("href", "")
            if href:
                self.links.append(href)
            if values.get("rel", "").lower() == "canonical":
                self.canonicals.append(href)
        elif tag == "a":
            href = values.get("href", "")
            if href:
                self.links.append(href)
        elif tag == "script":
            self.scripts.append(values)
            if values.get("type", "").lower() == "application/ld+json":
                self.in_json_ld = True
                self.json_ld_parts = []
        elif tag == "h1":
            self.h1_count += 1

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title" and self.in_title:
            self.in_title = False
            self.titles.append("".join(self.title_parts).strip())
        elif tag == "script" and self.in_json_ld:
            self.in_json_ld = False
            self.json_ld_blocks.append("".join(self.json_ld_parts).strip())

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.title_parts.append(data)
        if self.in_json_ld:
            self.json_ld_parts.append(data)

    def meta_content(self, *, name: str | None = None, prop: str | None = None) -> list[str]:
        matches: list[str] = []
        for item in self.meta:
            if name is not None and item.get("name", "").lower() == name.lower():
                matches.append(item.get("content", "").strip())
            if prop is not None and item.get("property", "").lower() == prop.lower():
                matches.append(item.get("content", "").strip())
        return matches


class ReleaseValidator:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.pages: dict[Path, PageParser] = {}

    def check(self, condition: bool, message: str) -> None:
        if not condition:
            self.errors.append(message)

    def require_file(self, relative: Path | str) -> Path:
        path = ROOT / relative
        self.check(path.is_file(), f"required file is missing: {relative}")
        return path

    def parse_page(self, relative: Path) -> PageParser:
        path = self.require_file(relative)
        parser = PageParser()
        if path.is_file():
            parser.feed(path.read_text(encoding="utf-8"))
            parser.close()
        self.pages[relative] = parser
        return parser

    def validate_page(self, relative: Path, canonical: str, *, indexable: bool) -> None:
        parser = self.parse_page(relative)
        label = relative.as_posix()
        self.check(parser.html_lang.lower() == "en", f"{label}: html lang must be en")
        self.check(len(parser.titles) == 1 and bool(parser.titles[0]), f"{label}: exactly one non-empty title is required")
        descriptions = parser.meta_content(name="description")
        self.check(len(descriptions) == 1 and len(descriptions[0]) >= 50, f"{label}: one useful meta description is required")
        self.check(parser.canonicals == [canonical], f"{label}: canonical must be exactly {canonical}")
        self.check(parser.h1_count == 1, f"{label}: exactly one h1 is required")

        robots = [value.lower().replace(" ", "") for value in parser.meta_content(name="robots")]
        self.check(len(robots) == 1, f"{label}: exactly one robots meta tag is required")
        if robots:
            directives = {item for item in robots[0].split(",") if item}
            if indexable:
                self.check("index" in directives, f"{label}: intended public page must be indexable")
                self.check("noindex" not in directives, f"{label}: intended public page cannot contain noindex")
                self.check("follow" in directives, f"{label}: intended public page must permit following")
            else:
                self.check("noindex" in directives, f"{label}: held demo must remain noindex")
                self.check("follow" in directives, f"{label}: held demo should remain follow")

        og_urls = parser.meta_content(prop="og:url")
        if indexable:
            self.check(og_urls == [canonical], f"{label}: indexable page og:url must match canonical")
            self.check(bool(parser.meta_content(prop="og:title")), f"{label}: indexable page requires og:title")
            self.check(bool(parser.meta_content(prop="og:description")), f"{label}: indexable page requires og:description")

    @staticmethod
    def internal_target(href: str) -> Path | None:
        parsed = urlsplit(href)
        if parsed.scheme or parsed.netloc or not parsed.path.startswith("/rolemath-labs/"):
            return None
        local = parsed.path.removeprefix("/rolemath-labs/")
        if not local:
            return Path("index.html")
        if local.endswith("/"):
            return Path(local) / "index.html"
        return Path(local)

    def validate_internal_links(self) -> None:
        for relative, parser in self.pages.items():
            for href in parser.links:
                target = self.internal_target(href)
                if target is None:
                    continue
                self.check((ROOT / target).is_file(), f"{relative.as_posix()}: internal target does not exist: {href}")

    def validate_structured_data(self) -> None:
        parser = self.pages.get(Path("index.html"))
        if parser is None:
            return
        decoded: list[object] = []
        for index, block in enumerate(parser.json_ld_blocks, start=1):
            try:
                decoded.append(json.loads(block))
            except json.JSONDecodeError as error:
                self.errors.append(f"index.html: JSON-LD block {index} is invalid: {error}")
        types: set[str] = set()
        for item in decoded:
            if isinstance(item, dict):
                value = item.get("@type")
                if isinstance(value, str):
                    types.add(value)
                elif isinstance(value, list):
                    types.update(str(entry) for entry in value)
        self.check("Dataset" in types, "index.html: landing page must expose Dataset JSON-LD")

    def validate_sitemap_and_robots(self) -> None:
        sitemap_path = self.require_file("sitemap.xml")
        urls: list[str] = []
        if sitemap_path.is_file():
            try:
                root = ElementTree.parse(sitemap_path).getroot()
                namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
                urls = [node.text.strip() for node in root.findall("s:url/s:loc", namespace) if node.text]
            except ElementTree.ParseError as error:
                self.errors.append(f"sitemap.xml is invalid XML: {error}")

        expected = set(INDEXABLE_PAGES.values())
        self.check(len(urls) == len(set(urls)), "sitemap.xml contains duplicate URLs")
        self.check(set(urls) == expected, f"sitemap.xml must contain exactly the four intended indexable pages; got {sorted(urls)}")
        self.check(NOINDEX_PAGES[Path("fit-check/index.html")] not in urls, "Fit Check must not appear in sitemap.xml")

        robots = self.require_file("robots.txt")
        if robots.is_file():
            text = robots.read_text(encoding="utf-8")
            self.check("User-agent: *" in text, "robots.txt must declare the general user agent")
            self.check("Disallow: /" not in text, "robots.txt cannot block the public sidecar")
            self.check(f"Sitemap: {BASE_URL}/sitemap.xml" in text, "robots.txt must name the canonical sitemap")

    def validate_fit_check_privacy(self) -> None:
        script_path = self.require_file("assets/fit-check.js")
        if not script_path.is_file():
            return
        text = script_path.read_text(encoding="utf-8")
        forbidden = {
            r"\bfetch\s*\(": "fetch",
            r"XMLHttpRequest": "XMLHttpRequest",
            r"navigator\.sendBeacon": "sendBeacon",
            r"\blocalStorage\b": "localStorage",
            r"\bsessionStorage\b": "sessionStorage",
            r"document\.cookie": "document.cookie",
            r"\bindexedDB\b": "indexedDB",
            r"\bWebSocket\b": "WebSocket",
            r"\bEventSource\b": "EventSource",
        }
        for pattern, label in forbidden.items():
            self.check(re.search(pattern, text) is None, f"assets/fit-check.js: client-only boundary violated by {label}")

        parser = self.pages.get(Path("fit-check/index.html"))
        if parser is not None:
            external_scripts = [item.get("src", "") for item in parser.scripts if item.get("src", "").startswith(("http://", "https://"))]
            self.check(not external_scripts, f"fit-check/index.html: external scripts are prohibited: {external_scripts}")

    def validate_data(self) -> None:
        data_dir = ROOT / "data"
        actual_files = {
            path.relative_to(ROOT).as_posix()
            for path in data_dir.rglob("*")
            if path.is_file()
        } if data_dir.is_dir() else set()
        self.check(actual_files == EXPECTED_DATA_FILES, f"data directory must contain exactly three release files; got {sorted(actual_files)}")

        json_path = self.require_file("data/certifications.json")
        csv_path = self.require_file("data/certifications.csv")
        dictionary_path = self.require_file("data/field_dictionary.json")
        if not all(path.is_file() for path in (json_path, csv_path, dictionary_path)):
            return

        try:
            payload = json.loads(json_path.read_text(encoding="utf-8"))
            dictionary = json.loads(dictionary_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as error:
            self.errors.append(f"release JSON is invalid: {error}")
            return

        records = payload.get("records") if isinstance(payload, dict) else None
        self.check(isinstance(records, list), "certifications.json: records must be a list")
        if not isinstance(records, list):
            return
        self.check(payload.get("record_count") == EXPECTED_RECORD_COUNT, "certifications.json: declared record_count must be 50")
        self.check(len(records) == EXPECTED_RECORD_COUNT, "certifications.json: records length must be 50")
        schema = payload.get("schema_version")
        self.check(schema == "rolemath_open_certification_data_v2", "certifications.json: unexpected schema_version")
        self.check(dictionary.get("schema_version") == schema, "field_dictionary.json: schema_version must match certifications.json")

        ids: list[str] = []
        routes: list[str] = []
        live_urls = 0
        for index, record in enumerate(records):
            self.check(isinstance(record, dict), f"certifications.json: record {index} must be an object")
            if not isinstance(record, dict):
                continue
            self.check(record.get("schema_version") == schema, f"certifications.json: record {index} schema mismatch")
            credential = record.get("credential")
            self.check(isinstance(credential, dict), f"certifications.json: record {index} credential must be an object")
            if not isinstance(credential, dict):
                continue
            cert_id = str(credential.get("certification_id") or "")
            route = str(credential.get("route_identifier") or "")
            ids.append(cert_id)
            routes.append(route)
            self.check(bool(cert_id), f"certifications.json: record {index} has blank certification_id")
            self.check(route.startswith("/certifications/") and not route.endswith("/"), f"certifications.json: record {cert_id or index} has malformed route_identifier")
            rolemath_url = credential.get("rolemath_url")
            if rolemath_url is not None:
                live_urls += 1
                self.check(isinstance(rolemath_url, str) and rolemath_url.startswith("https://rolemath.com/"), f"certifications.json: {cert_id} has invalid rolemath_url")

        self.check(len(ids) == len(set(ids)), "certifications.json: certification_id values must be unique")
        self.check(len(routes) == len(set(routes)), "certifications.json: route_identifier values must be unique")
        self.check(live_urls == EXPECTED_LIVE_URLS, f"certifications.json: expected 28 live RoleMath URLs, got {live_urls}")
        self.check(len(records) - live_urls == EXPECTED_NULL_URLS, f"certifications.json: expected 22 null RoleMath URLs, got {len(records) - live_urls}")

        with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            csv_rows = list(reader)
            csv_fields = reader.fieldnames or []
        dictionary_fields = [
            str(item.get("name") or "")
            for item in dictionary.get("csv_fields", [])
            if isinstance(item, dict)
        ]
        self.check(csv_fields == dictionary_fields, "certifications.csv: columns must exactly match the field dictionary")
        self.check(len(csv_rows) == EXPECTED_RECORD_COUNT, "certifications.csv: row count must be 50")
        self.check({row.get("certification_id", "") for row in csv_rows} == set(ids), "CSV and JSON certification_id sets must match")

        projection = dictionary.get("release", {}).get("live_url_projection", {}) if isinstance(dictionary.get("release"), dict) else {}
        self.check(projection.get("sitemap_route_count") == EXPECTED_SITEMAP_ROUTE_COUNT, "field_dictionary.json: live projection must preserve the observed 310-route sitemap count")
        self.check(projection.get("matched_records") == EXPECTED_LIVE_URLS, "field_dictionary.json: live projection matched_records must be 28")
        self.check(projection.get("null_records") == EXPECTED_NULL_URLS, "field_dictionary.json: live projection null_records must be 22")

    def validate_checksums(self) -> None:
        checksum_path = self.require_file("checksums.txt")
        if not checksum_path.is_file():
            return
        declared: dict[str, str] = {}
        for line_number, raw in enumerate(checksum_path.read_text(encoding="utf-8").splitlines(), start=1):
            line = raw.strip()
            if not line:
                continue
            parts = line.split(maxsplit=1)
            if len(parts) != 2 or not re.fullmatch(r"[0-9a-f]{64}", parts[0]):
                self.errors.append(f"checksums.txt:{line_number}: malformed checksum line")
                continue
            path = parts[1].lstrip("*")
            declared[path] = parts[0]
        self.check(set(declared) == EXPECTED_DATA_FILES, f"checksums.txt must cover exactly the three data files; got {sorted(declared)}")
        for relative, expected in declared.items():
            path = ROOT / relative
            if not path.is_file():
                continue
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            self.check(actual == expected, f"checksum mismatch for {relative}: expected {expected}, got {actual}")

    def validate_release_labels(self) -> None:
        for relative in [*INDEXABLE_PAGES, *NOINDEX_PAGES]:
            path = ROOT / relative
            if path.is_file():
                text = path.read_text(encoding="utf-8")
                self.check("v0.2.0" in text, f"{relative.as_posix()}: release label must be v0.2.0")

    def run(self) -> None:
        for relative, canonical in INDEXABLE_PAGES.items():
            self.validate_page(relative, canonical, indexable=True)
        for relative, canonical in NOINDEX_PAGES.items():
            self.validate_page(relative, canonical, indexable=False)
        self.validate_internal_links()
        self.validate_structured_data()
        self.validate_sitemap_and_robots()
        self.validate_fit_check_privacy()
        self.validate_data()
        self.validate_checksums()
        self.validate_release_labels()

        if self.errors:
            print(f"RoleMath Labs validation failed with {len(self.errors)} error(s):", file=sys.stderr)
            for error in self.errors:
                print(f"- {error}", file=sys.stderr)
            raise SystemExit(1)

        print(
            "RoleMath Labs validation passed: "
            f"{len(INDEXABLE_PAGES)} indexable pages, "
            f"{len(NOINDEX_PAGES)} noindex demo, "
            f"{EXPECTED_RECORD_COUNT} data records."
        )


if __name__ == "__main__":
    ReleaseValidator().run()
