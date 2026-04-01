# Keyword Mapper — AI SEO Tool (Hire Overseas)

## Overview

An 8-step SEO content workflow tool that takes a seed keyword and guides the user through keyword mapping, SERP analysis, outline generation, article writing, and internal linking — all powered by the Anthropic Claude API.

## Architecture

- **Frontend**: Single static HTML file (`keyword_mapper.html`) — vanilla HTML, CSS, and JavaScript with a dark theme
- **Server**: Simple Python HTTP server (`server.py`) on port 5000
- **AI**: Calls the Anthropic Claude API directly from the browser (`claude-sonnet-4-20250514`)
- **No build system**, no package manager, no frameworks

## Project Structure

```
keyword_mapper.html   # Main application file (all UI, styles, and logic)
server.py             # Python HTTP server that serves the HTML on port 5000
.replit               # Replit configuration
```

## Running the App

The workflow "Start application" runs `python3 server.py` which serves the app on port 5000.

## 8-Step Workflow

1. **Keyword** — Enter seed keyword, Claude analyses it and generates a pillar/cluster content map
2. **Map** — Review pillar & cluster pages in a table. Each row has a "Generate Keywords" button to get 10 secondary and 10 semantic keywords per page
3. **SERP** — Select a page to get detailed SERP analysis (competitors, featured snippets, AI overview status, content gaps)
4. **Outline** — Generate 2 SEO-optimised outline options based on SERP data
5. **Draft** — Review and choose between 2 outline drafts with different competitive angles
6. **Article** — Claude writes a full, human-quality SEO article optimised for search and AI overviews
7. **Links** — Internal linking recommendations with anchor text types (exact match, branded, secondary, descriptive) and placement suggestions
8. **Export** — Final output with word count, character count, read time, and copy/export options (HTML, plain text, Markdown, CSV)

## Key Features

- Pillar/Cluster page mapping with cannibalization detection against 49+ live site pages
- Per-row keyword generation (secondary + semantic) with bulk generate option
- SERP competitive analysis with featured snippet and AI overview strategies
- Dual outline options with different competitive angles
- Full article generation optimised for SEO, AI overviews, and featured snippets
- Internal linking with mixed anchor text types and natural placement context
- Multiple export formats (HTML, plain text, Markdown, CSV)

## Notes

- API calls go directly from the browser to `https://api.anthropic.com/v1/messages`
- The site index includes Hire Overseas pages (roles, blogs, landing pages) for cannibalization checking
- Dark theme with Inter + JetBrains Mono fonts
