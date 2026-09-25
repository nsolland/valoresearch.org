# Repository control

This repository is the canonical public source for https://valoresearch.org.

- `main` is the production branch.
- GitHub Pages publishes the static files directly from the repository root.
- Do not add GitHub Actions, CI deployment workflows, external build services, or another hosting control plane.
- A push to `main` is the publication trigger.
- Interactive demos and services that require a runtime are deployed separately, currently on Railway, and linked from this site.
- Do not place credentials, private claims, internal application code, or runtime secrets in this public repository.
- Do not call a change live until the canonical production URL returns the expected content.

## Chat image and engagement asset handling

These rules apply when a task refers to an image already created or uploaded in the active ChatGPT conversation.

1. If the instruction is "use this image", "use the image from this chat", "add the image", or equivalent, use the existing conversation image as the source asset. Do not regenerate, reinterpret, redraw, or replace it unless explicitly instructed.
2. Before committing, establish the actual source file available from the conversation/runtime. Do not invent a filename or pretend an unavailable image is accessible.
3. Customer-specific engagement assets belong under `engage/customers/<customer>/assets/`.
4. Reusable shared engagement assets belong under `engage/_assets/common/`.
5. Use stable, descriptive lowercase filenames. Prefer `.webp` for photographic/generated raster assets, `.png` when transparency or lossless raster output is materially required, and `.svg` for authored vector diagrams.
6. If a conversion is needed, preserve the visual content. Conversion is not permission to regenerate or restyle the image.
7. Public-repository rule: only commit an image when it is explicitly safe for public publication. Customer engagement content and asset metadata must be treated as public unless a separate authenticated/private delivery surface is explicitly in use.
8. If the requested source image is not actually available in the active conversation/runtime, stop the image-ingest step and request the source image. Never substitute a newly generated image silently.
9. Commit image assets on the active feature branch before merging to `main`, and report the exact repository path and commit SHA.
10. For engagement pages, content should reference the committed asset path; do not depend on temporary chat URLs, local paths, or runtime-only files.


## Production deployment contract — verified 2026-09-23

This section is authoritative for deployment work unless production is deliberately migrated and this file is updated in the same change.

### Canonical production path

```text
nsolland/valoresearch.org
  main
    -> GitHub Pages
      -> valoresearch.org
```

Verified repository facts on 2026-09-23:
- GitHub reports Pages enabled for this repository.
- `CNAME` contains `valoresearch.org`.
- `.nojekyll` is present.
- The production site is static content published from this repository.
- `nsolland/website-deployer` is **not** the canonical publication source for `valoresearch.org`, even if documentation there describes a Cloudflare Pages architecture.

### Hard deployment rules

1. **Inspect before changing.** Before any website deployment, verify the current production repository, branch, Pages/hosting configuration, CNAME/domain binding, and public origin. Do not infer hosting from old documentation.
2. **One control plane.** Do not introduce Cloudflare Pages, Vercel, Railway, Replit, GitHub Actions deployment workflows, or another hosting mechanism for `valoresearch.org` unless an explicit migration has first been approved.
3. **No DNS changes for ordinary content.** New pages and content must use the existing GitHub Pages path. Do not modify DNS merely to publish a route.
4. **Build for the actual host.** Pages under `valoresearch.org` must work under GitHub Pages/static-host constraints, including direct navigation/refresh where applicable.
5. **Test before main.** Implement on a branch, run the relevant tests/checks, inspect the generated/static artifact, and verify route behavior before merging to `main`.
6. **Production last.** A push/merge to `main` is a production publication event. Do not merge merely to discover whether the implementation works.
7. **Verify after publication.** Do not report a page as live until its canonical `https://valoresearch.org/...` URL returns the expected content.
8. **Diagnose, do not stack deployers.** If publication fails, investigate the existing GitHub Pages chain first. Never add a second deployment mechanism as a workaround.

### Migration rule

If hosting is intentionally migrated later, the migration is incomplete until all of the following agree: actual DNS/origin, repository deployment configuration, this `AGENTS.md`, and the VALO project context in `nsolland/Index`. Historical deployment notes must be marked historical rather than left as apparently current instructions.
