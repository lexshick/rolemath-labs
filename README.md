# RoleMath Labs

RoleMath Labs publishes small, auditable experiments from [RoleMath](https://rolemath.com/), an
evidence-backed technical certification decision product. Version 0.2.0 adds an indexable public
case study, methodology, and data landing page while keeping the client-only Certification Fit
Check `noindex, follow`.

**Stable site:** <https://lexshick.github.io/rolemath-labs/>

## Public artifacts

- [Product and operations case study](https://lexshick.github.io/rolemath-labs/case-study/)
- [Methodology and limitations](https://lexshick.github.io/rolemath-labs/methodology/)
- [Data landing](https://lexshick.github.io/rolemath-labs/data/)
- [Certification Fit Check](https://lexshick.github.io/rolemath-labs/fit-check/) (`noindex`)

## Download the data

- [JSON](data/certifications.json)
- [CSV](data/certifications.csv)
- [Field dictionary](data/field_dictionary.json)
- [SHA-256 checksums](checksums.txt)

The Labs release is v0.2.0; the byte-preserved dataset content revision remains v0.1.0. The dataset
contains 50 fact records. Each consequential field retains an attributable source
and checked date where available. A `route_identifier` is a stable RoleMath identifier, not proof
that a public page exists. `rolemath_url` is non-null only when the exact route appeared in the
310-URL RoleMath sitemap observed on 2026-08-10; that does not prove Google indexing or traffic.

## What this does not prove

- Certification-caused salary, hiring, placement, pass rate, or return on investment.
- Current training seats, provider willingness, a provider relationship, or complete market
  coverage.
- Qualified traffic, leads, conversions, revenue, or employment outcomes for RoleMath.

Unknown values remain unknown when RoleMath did not find a current attributable value. Occupation
statistics describe the mapped occupation—not credential holders—and do not prove a credential
caused the observed pay or employment measure.

## Licenses

Data and documentation are licensed under [CC BY 4.0](LICENSE-DATA). The small static site and Fit
Check display code are licensed under [MIT](LICENSE-CODE).
