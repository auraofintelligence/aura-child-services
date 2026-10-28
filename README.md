# Aura Children and Young People

A public guide to Luke Nathan Hayes’s proposal, **Aura Genesis for Children and Young People in Australian Care**. The guide begins with a chosen interest and supported creative learning, then follows self understanding, law, family and culture, mentors, contribution and opportunities for adulthood.

Website: https://auraofintelligence.github.io/aura-child-services/

Repository: https://github.com/auraofintelligence/aura-child-services

## What is included

Fifteen public pages plus a custom noindex 404: a welcoming homepage, ten substantive grouped chapters, the complete source register, related projects, exact licence text and a searchable sitemap. All 329 top-level paragraphs, both tables and all 19 distinct original external source URLs from the supplied DOCX are covered in the readable HTML. Blank source paragraphs do not produce empty visible content. The original DOCX remains unchanged in `documents/`, with its SHA-256 and byte length in `content/documents.json` and `documents/SHA256SUMS`.

The editorial introductions lead into the original reading. They do not replace the substantive narrative. Word hyperlinks retain their exact targets and labels; tables stay in their original position relative to the surrounding text. Original reference IDs and edition descriptions are preserved.

The design uses warm paper, plum, sage and apricot; large serif headings and system sans-serif text. Headings and introductions precede artwork. Three original generated raster concepts show fictional ordinary creative learning, mentorship and future work. They are not photographs of actual participants, installed facilities or agreed services. Prompts, alt text, hashes and optimisation records are in `content/artwork.json` and `content/artwork-prompts.json`. No partner artwork is copied.

All text is at least 18px at the default root size except 15px image credits. Reading, navigation, chapter contents, circular previous/next routes, source downloads and licence text work without JavaScript. JavaScript adds sitemap filtering and Escape/outside dismissal for the native All pages menu. Keyboard focus, reduced motion, print rules and a floating Top link are included.

## Content distinctions

The children and teens proposal uses Verse Box and everyday learning. Pressure treatment and the adult Truth Engine research activities are outside its activities. The sixty-day adult teacher course is facilitator background, not a child participation requirement or professional qualification.

The proposed progression is interest/project, reflection and rights, human mentors and later adult opportunities. Care, adoption, school learning, statutory records and personal Aura records keep their distinct purposes. There is no trauma-disclosure demand, credibility or placement score, invented family history, operating care service, recruitment system or promised qualification.

C-Hours recognise verified voluntary human contribution. They have no monetary value. Essential support, care and schooling remain independent of programme participation and contribution. Actual employment, finance, supervision, safeguarding, access and legal authority follow the relevant real arrangements.

## Sources reviewed on 28 October 2026

Three primary guidance pages were reviewed for the short, separately labelled notes on the Sources page:

- [OAIC: children and young people](https://www.oaic.gov.au/privacy/your-privacy-rights/more-privacy-rights/children-and-young-people): contextual capacity for privacy decisions and differences in coverage.
- [Australian Human Rights Commission: child safe organisations](https://humanrights.gov.au/resource-hub/resources-for-organisations-businesses/child-safe-organisations): National Principles, participation and organisational practice.
- [Queensland: charter of rights](https://www.families.qld.gov.au/our-work/child-safety/children-young-people-care/charter-rights): privacy, identity, voice and transition from care. The source page states it was reviewed on 20 July 2026.

The remaining references preserve the source proposal’s context. This is not a claim that every legal, clinical or external source has been freshly verified. Current authority and duties depend on the organisation, jurisdiction, role and activity.

Related-project descriptions were checked against the local Genesis, Verse Box and Mutual Futures repositories. `connections.html` includes distinct links to UNGA81, Claytons Road, P4A, C-Hours, law and the adult teacher course. Links do not establish operational partnerships.

## Build and check

Python 3.12 or later is sufficient. The build and checks use the standard library; no package installation is required. The optional local asset optimisation used the bundled Pillow package, but builds use the committed WebP files directly.

```sh
python scripts/build.py
python scripts/check.py
node --check assets/app.js
python -m http.server 4197 --bind 127.0.0.1
```

Open http://127.0.0.1:4197/. The preview is for local development; the deployment workflow publishes only the public pages, assets, document and provenance data.

| File | Purpose |
| --- | --- |
| `scripts/build.py` | Document extraction, chapter groupings, editorial introductions and static HTML/discovery generation |
| `scripts/check.py` | Internal links/anchors, full navigation, source text, exact source URLs, assets and document/artwork hashes |
| `assets/style.css`, `assets/app.js` | Responsive presentation and optional progressive enhancement |
| `content/source.json` | Ordered paragraphs/tables extracted from the unchanged source |
| `content/documents.json` | Document integrity and attribution |
| `content/artwork.json` | Original concept artwork provenance, prompts, alt text and hashes |

Regenerate and check after source or shared layout edits. Generated root HTML is committed for GitHub Pages. `npm run build`, `npm run check` and `npm run dev` are convenience wrappers for the same commands.

## Publishing and discovery

`.github/workflows/pages.yml` rebuilds, checks and publishes a public-only artifact using GitHub Pages. Set the repository Pages source to **GitHub Actions**. Pushes to `main` run the workflow. The repository metadata alone does not claim deployment has occurred.

The site includes canonical/OG metadata, XML and HTML sitemaps and `llms.txt`. The project-level `robots.txt` is informational: crawler policy applies at `https://auraofintelligence.github.io/robots.txt`. `.github/robots-root-snippet.txt` supplies narrowly scoped rules for this project, allowing general/OAI/Claude search discovery while asking GPTBot, ClaudeBot and Google-Extended not to collect this path. Merge into existing origin policy without replacing other project directives. Crawler cooperation does not guarantee discovery or enforce rights.

## Rights and attribution

Concept and source direction: Luke Nathan Hayes / Strange But True / Aura of Intelligence. Website implementation prepared with ChatGPT.

Original project material uses the [Strange But True Public Source Licence](LICENCE.md), preserving the Verse Box licence terms with only the project name/URL changed. It is a public-source licence with reserved commercial rights. Supplied documents and third-party material retain their existing rights. See [RIGHTS.md](RIGHTS.md). Discovery grants no additional commercial reuse or AI-training permission.
