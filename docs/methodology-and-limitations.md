# Methodology and limitations

Dataset version 0.1.1 is a dated public-fact projection from RoleMath's private evidence system. It
is not a certification ranking, a course marketplace, or a claim that every record is complete.

The human-readable version is published at
<https://lexshick.github.io/rolemath-labs/methodology/>.

## Evidence and currentness

Credential identity, exam version, eligibility, fees, lifecycle, renewal, and preparation facts
are tied to attributable sources and checked dates where available. An unresolved value means
RoleMath did not find a current attributable value in the sources it checked. It does not mean a
vendor has confirmed the value is absent.

`route_identifier` is a stable RoleMath identifier. `rolemath_url` is populated only when the exact
identifier matched the 310-URL RoleMath sitemap observed on 2026-08-10. Twenty-eight records
matched; 22 remain null. Sitemap presence does not prove search-engine indexing, impressions, or
traffic.

## Occupation context

Occupation statistics use cited occupation-level sources such as BLS or O*NET. They describe the
mapped occupation, not people who hold a certification, and do not prove the credential caused a
salary, hiring, or employment outcome. Mapping a credential to an occupation is decision context,
not a universal employer requirement.

## Training observations

Published training offers are restricted to Security+, CCNA, and AWS Solutions Architect
Associate. They are dated observations from provider-owned pages. They do not establish current
seats, future availability, provider willingness, a commercial relationship, fulfillment, or
comprehensive market coverage.

## Deliberately excluded

Private readiness profiles, completeness scores, registry order, recommendation rankings,
confidence calculations, review workflow, publication state, internal source IDs, private provider
research, personal data, and commercial matching logic are not in this release.

For RoleMath's reader-facing evidence posture, see
<https://rolemath.com/how-rolemath-works/>.
