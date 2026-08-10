# Release notes

## Site v0.2.0 — public proof and discoverability

Published 2026-08-10. This is a static-site and documentation release; the Top-50 dataset remains
v0.1.1.

- The landing page, case study, methodology, and data dictionary are `index, follow`.
- The Fit Check remains `noindex, follow` and is excluded from the sitemap.
- The sitemap contains exactly four intended-indexable URLs.
- Dataset and Article JSON-LD, canonical metadata, Open Graph metadata, and `robots.txt` are present.
- A repository validator checks indexability parity, internal targets, JSON-LD, dataset integrity,
  checksums, and the Fit Check's client-only boundary.
- The public case study reports dated facts and explicitly withholds unvalidated audience, lead,
  provider, conversion, revenue, and employment claims.

No certification facts, route projections, provider observations, licensing terms, or Fit Check
decision logic changed.

## v0.1.1 — checksum serialization correction

The v0.1.1 maintenance release declares LF line endings as the canonical serialization and
corrects `checksums.txt` to match Git and GitHub Pages. The v0.1.0 data content is unchanged.

## v0.1.0

Published 2026-08-10 from RoleMath source-ready package
`2ff4983f0238085f29d0faf3307c23aee24c33c8`.

- Records: 50.
- Data files: exactly three.
- RoleMath sitemap observed: 310 URLs.
- Exact live-route matches: 28; null RoleMath URLs: 22.
- Sitemap SHA-256: `5c1424e53f6abe914cc3a39d6bdc26209a8556156c063242c320fdd876533acd`.
- Provider-observation records: Security+, CCNA, AWS Solutions Architect Associate only.
- Initial indexability: public and shareable, but `noindex, follow` pending a deliberate decision.

This release makes no claim of Google indexing, organic traffic, users, leads, provider
relationships, conversion, revenue, credential-caused pay, or employment outcomes.
