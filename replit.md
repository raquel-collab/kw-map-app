# Keyword Mapper — AI SEO Tool

## Overview

A single-page web application that helps SEO strategists generate a comprehensive content map from a single "seed" keyword. It uses the Anthropic Claude API to suggest page types, titles, slugs, and meta tags, while cross-referencing existing blog posts to detect cannibalization risks.

## Architecture

- **Frontend**: Single static HTML file (`keyword_mapper.html`) — vanilla HTML, CSS, and JavaScript
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

## Key Features

- Keyword mapping (Pillar Pages, Cluster Pages, Landing Pages, Blog Posts, Comparison Pages)
- Cannibalization Guard — checks new content against existing blog posts
- SEO optimization with meta title/description validation
- CSV export of generated content maps

## Notes

- The user must supply their own Anthropic API key via the UI
- API calls go directly from the browser to `https://api.anthropic.com/v1/messages`
