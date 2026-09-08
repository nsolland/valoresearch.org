# Repository control

This repository is the canonical public source for https://valoresearch.org.

- `main` is the production branch.
- GitHub Pages publishes the static files directly from the repository root.
- Do not add GitHub Actions, CI deployment workflows, external build services, or another hosting control plane.
- A push to `main` is the publication trigger.
- Interactive demos and services that require a runtime are deployed separately, currently on Railway, and linked from this site.
- Do not place credentials, private claims, internal application code, or runtime secrets in this public repository.
- Do not call a change live until the canonical production URL returns the expected content.
