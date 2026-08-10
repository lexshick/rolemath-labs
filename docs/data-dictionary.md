# Data dictionary

The machine-readable dictionary is [`data/field_dictionary.json`](../data/field_dictionary.json).

The CSV is a compact projection for analysis. The JSON retains nested source, cost, occupation,
preparation, and dated training-observation structures.

Key identity fields:

- `certification_id`: stable RoleMath record ID.
- `vendor_id` and `vendor_name`: vendor identity.
- `slug`: stable record slug.
- `route_identifier`: stable path-shaped RoleMath identifier; not a live-page claim.
- `rolemath_url`: exact sitemap-verified RoleMath URL or null/blank.
- `official_url`: vendor-owned credential source when recorded.

Key evidence fields:

- `currentness`: current exam/version state, source, transition source, and checked date.
- `eligibility`: hard prerequisite, recommended background, and registration eligibility kept
  separate.
- `cost`: scoped exam and renewal facts; null remains unknown.
- `preparation`: attributable official/free preparation records.
- `roles` and `occupations`: relationship context with source period and non-causality warning.
- `training_offers`: bounded dated observations, not availability or relationship claims.
- `known_unknowns`: explicit unresolved public facts.
