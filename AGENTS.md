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


## Production serving contract — corrected 2026-09-30

This section supersedes the stale 2026-09-23 GitHub Pages assumption below. The current operator-confirmed production serving layer for `valoresearch.org` is Cloudflare.

### Canonical source and serving model

```text
nsolland/valoresearch.org
  main
    -> Cloudflare serving layer
      -> valoresearch.org
```

### Hard safety rules

1. **Preserve the existing Cloudflare setup.** Do not migrate, recreate, replace, or reconfigure the current Cloudflare serving path merely to publish content.
2. **Do not infer the Cloudflare product or topology.** Before changing deployment configuration, verify whether the active path uses Pages, Workers, static assets, DNS/proxy/origin routing, or another Cloudflare mechanism.
3. **Source is not serving.** GitHub `main` is the canonical public source repository; do not describe GitHub Pages as the production serving layer unless it is independently re-verified later.
4. **No deployer stacking.** Do not add Vercel, Railway, Replit, GitHub Pages, GitHub Actions deployment workflows, or another hosting control plane as a workaround.
5. **No DNS or Cloudflare configuration changes for ordinary content work.** Content changes should preserve the current serving architecture.
6. **Inspect before infrastructure changes.** Verify the active Cloudflare project/configuration, domain binding, origin and publication trigger before touching deployment files.
7. **Production last.** Test content changes on a branch before merging to `main`.
8. **Verify after publication.** Do not call a change live until the canonical production URL returns the expected content.
9. **Runtime services remain separate.** Railway or other runtimes may host interactive services linked by the site; they are not the serving layer for the main VALO website unless explicitly migrated.
10. **Do not delete legacy deployment artifacts blindly.** Files such as `CNAME`, `.nojekyll`, `vercel.json`, or old deployment notes may be historical. Preserve them until their current role is verified; removal requires an explicit cleanup task.

### Historical note

The previous section identified GitHub Pages as canonical based on a 2026-09-23 inspection. That conclusion is superseded by the operator-confirmed Cloudflare serving architecture as of 2026-09-30. Historical artifacts must not be used to infer the current host.

### Migration rule

Any future hosting migration is incomplete until the actual Cloudflare/DNS/origin state, repository deployment configuration, this `AGENTS.md`, and VALO project context agree. Do not change production infrastructure as part of an unrelated content task.
