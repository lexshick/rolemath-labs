# RoleMath Labs

RoleMath Labs publishes small, auditable experiments from [RoleMath](https://rolemath.com/), an
evidence-backed technical certification decision product. The first release contains a 50-record
certification facts dataset and a client-only Certification Fit Check.

**Stable site:** <https://lexshick.github.io/rolemath-labs/>

## Download the data

- [JSON](data/certifications.json)
- [CSV](data/certifications.csv)
- [Field dictionary](data/field_dictionary.json)
- [SHA-256 checksums](checksums.txt)

Version `0.1.0` contains exactly 50 records. Each consequential field retains an attributable
source and checked date where available. A `route_identifier` is a stable RoleMath identifier, not
proof that a public page exists. `rolemath_url` is non-null only when the exact route appeared in
the 310-URL RoleMath sitemap observed on 2026-08-10; that does not prove Google indexing or traffic.

## What this does not prove

- Certification-caused salary, hiring, placement, pass rate, or return on investment.
- Current training seats, provider willingness, a provider relationship, or complete market
  coverage.
- Traffic, users, leads, conversions, revenue, or employment outcomes for RoleMath.

Unknown values remain unknown when RoleMath did not find a current attributable value. Occupation
statistics describe the mapped occupation—not credential holders—and do not prove a credential
caused the observed pay or employment measure.

## Licenses

Data and documentation are licensed under [CC BY 4.0](LICENSE-DATA). The small static site and Fit
Check display code are licensed under [MIT](LICENSE-CODE).

## Authoritative evidence

The sidecar is a dated public artifact. Current decision pages and source ledgers remain on
[RoleMath](https://rolemath.com/). See the public
[methodology](https://rolemath.com/how-rolemath-works/) and the local
[methodology and limitations](docs/methodology-and-limitations.md).
