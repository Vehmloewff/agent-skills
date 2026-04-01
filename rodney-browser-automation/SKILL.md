---
name: rodney-browser-automation
description: Use Rodney CLI to automate browser tasks like navigation, login, extraction, screenshots, downloads, and scripted documentation crawling
---

# Rodney CLI Guide

This skill explains how to use **Rodney** effectively for important browser-driven tasks.

> Note: the CLI tool name is `rodney`. This file is named `rodeny.md` to match the requested path.
>
> If `rodney` is not installed, prefer direct links so a basic agent can still complete the install without browsing:
> - Repository: https://github.com/simonw/rodney
> - Releases: https://github.com/simonw/rodney/releases
> - Latest release page: https://github.com/simonw/rodney/releases/latest
> - Example macOS Apple Silicon download: https://github.com/simonw/rodney/releases/download/v0.4.0/rodney-darwin-arm64.tar.gz
> - Example macOS Intel download: https://github.com/simonw/rodney/releases/download/v0.4.0/rodney-darwin-amd64.tar.gz
> - Example Linux x86_64 download: https://github.com/simonw/rodney/releases/download/v0.4.0/rodney-linux-amd64.tar.gz
> - Example Linux ARM64 download: https://github.com/simonw/rodney/releases/download/v0.4.0/rodney-linux-arm64.tar.gz
>
> Installation steps:
> 1. Download the archive for the current platform from one of the links above.
> 2. Extract it, for example: `tar -xzf rodney-<platform>.tar.gz`
> 3. Create the bin directory if needed: `mkdir -p ~/.local/bin`
> 4. Copy the binary into place: `cp rodney ~/.local/bin/rodney`
> 5. Make sure it is executable: `chmod +x ~/.local/bin/rodney`
> 6. Verify install: `~/.local/bin/rodney --help`

## What Rodney is

Rodney is a command-line browser automation tool for Chrome. It is useful for:
- opening websites
- logging into web apps
- navigating documentation sites
- extracting text and HTML
- clicking buttons and links
- filling forms
- evaluating JavaScript on pages
- taking screenshots
- downloading assets

## Core mental model

Rodney works like a scriptable browser session.

Typical flow:
1. start browser
2. open a page
3. wait for load / stability / idle
4. inspect text, HTML, or DOM
5. interact if needed
6. repeat across pages
7. stop browser when done

## Session modes

Rodney supports two session scopes:
- **local**: session files stored in `./.rodney/`
- **global**: session files stored in `~/.rodney/`

For project work, prefer **local** sessions:

```bash
rodney start --local
```

This keeps cookies and auth tied to the current working directory.

## Starting and stopping

### Start headless browser
```bash
rodney start --local
```

### Start visible browser
```bash
rodney start --local --show
```

Visible mode is useful when:
- diagnosing login issues
- handling redirects or MFA
- understanding dynamic UI behavior

### Check status
```bash
rodney status
```

### Stop browser
```bash
rodney stop
```

## Basic navigation

### Open a URL
```bash
rodney open 'https://example.com'
```

### Open a new tab
```bash
rodney newpage 'https://example.com/docs'
```

### List tabs
```bash
rodney pages
```

### Switch tabs
```bash
rodney page 1
```

### Reload
```bash
rodney reload
rodney reload --hard
```

### Navigate history
```bash
rodney back
rodney forward
```

## Waiting correctly

Most Rodney failures happen because the page has not finished rendering.

Useful wait commands:

### Wait for page load
```bash
rodney waitload
```

### Wait for DOM to stabilize
```bash
rodney waitstable
```

### Wait for network idle
```bash
rodney waitidle
```

### Wait for a specific element
```bash
rodney wait 'input[type="email"]'
```

### Add a fixed pause
```bash
rodney sleep 2
```

## Recommended waiting pattern

For modern JS-heavy sites:

```bash
rodney open 'https://example.com'
rodney waitload
rodney waitstable
rodney waitidle
```

If a specific element matters, also wait for it directly:

```bash
rodney wait 'main'
```

## Getting page information

### Current URL
```bash
rodney url
```

### Page title
```bash
rodney title
```

### Full page HTML
```bash
rodney html
```

### HTML for one element
```bash
rodney html 'main'
```

### Text content for an element
```bash
rodney text 'main'
```

### Attribute value
```bash
rodney attr 'a.cta' href
```

## Best way to extract structured info

Rodney’s `js` command is often the most powerful option.

Example: gather headings and links:

```bash
rodney js "JSON.stringify({
  title: document.title,
  h1: [...document.querySelectorAll('h1')].map(x => x.innerText),
  h2: [...document.querySelectorAll('h2')].map(x => x.innerText),
  links: [...document.querySelectorAll('a')]
    .map(a => ({ text: a.innerText.trim(), href: a.href }))
    .filter(x => x.text)
    .slice(0, 50)
}, null, 2)"
```

Example: quick whole-page text dump:

```bash
rodney js "document.body.innerText.slice(0,4000)"
```

## Interacting with pages

### Click an element
```bash
rodney click 'button[type="submit"]'
```

### Fill an input
```bash
rodney input 'input[name="username"]' 'my-user'
```

### Clear an input
```bash
rodney clear 'input[name="search"]'
```

### Submit a form
```bash
rodney submit 'form'
```

### Select a dropdown value
```bash
rodney select 'select[name="region"]' 'us'
```

### Hover or focus
```bash
rodney hover '.menu-trigger'
rodney focus 'input[type="search"]'
```

## Login workflows

Typical login pattern:

```bash
rodney open 'https://example.com/login'
rodney waitidle
rodney input 'input[name="username"]' 'USERNAME'
rodney input 'input[name="password"]' 'PASSWORD'
rodney click 'button[type="submit"]'
rodney waitidle
```

### Tips for login reliability
- use `--show` if the auth flow is complex
- wait for inputs before typing
- inspect selectors with `rodney html` or `rodney js`
- confirm success with `rodney url` and `rodney title`
- if login state matters later, use `--local` session mode

## Working with dynamic documentation sites

Documentation sites often use client-side rendering and nested navigation. Best practices:
- wait for network idle
- extract links from nav using `js`
- use `newpage` for branching exploration
- pull `document.body.innerText` when semantic selectors are unreliable
- save discovered URLs into local files for later crawling

Example:

```bash
rodney open 'https://docs.example.com'
rodney waitidle
rodney js "JSON.stringify([...document.querySelectorAll('a')].map(a => a.href).filter(Boolean), null, 2)"
```

## Screenshots and PDFs

### Screenshot page
```bash
rodney screenshot page.png
```

### Screenshot with dimensions
```bash
rodney screenshot -w 1440 -h 2200 page.png
```

### Screenshot one element
```bash
rodney screenshot-el 'main' main.png
```

### Save page as PDF
```bash
rodney pdf page.pdf
```

## Downloads

### Download a linked file
```bash
rodney download 'a[href$=".pdf"]' file.pdf
```

### Stream download to stdout
```bash
rodney download 'a[href$=".json"]' -
```

## Element checks and assertions

### Check existence
```bash
rodney exists 'main'
```

### Check visibility
```bash
rodney visible 'button'
```

### Count elements
```bash
rodney count 'a'
```

### Assert a JS expression
```bash
rodney assert "document.title.includes('Docs')"
```

### Assert equality
```bash
rodney assert "document.querySelectorAll('h1').length" 1
```

These are useful in repeatable scripts.

## Accessibility inspection

Rodney can inspect the accessibility tree, which is helpful when CSS selectors are unstable.

### Dump accessibility tree
```bash
rodney ax-tree --depth 3
```

### Find nodes by role or name
```bash
rodney ax-find --role button
rodney ax-find --name 'Sign In'
```

### Inspect one element
```bash
rodney ax-node 'button[type="submit"]'
```

## Common debugging workflow

When a command fails:

1. check browser status
```bash
rodney status
```

2. inspect current page
```bash
rodney title
rodney url
```

3. dump visible text
```bash
rodney js "document.body.innerText.slice(0,3000)"
```

4. inspect candidate selectors
```bash
rodney html 'body'
```

5. take a screenshot
```bash
rodney screenshot debug.png
```

6. switch to visible mode if needed
```bash
rodney stop
rodney start --local --show
```

## Good selector strategy

Prefer selectors in this order:
1. stable IDs
2. semantic form selectors like `input[name="email"]`
3. specific button selectors like `button[type="submit"]`
4. data attributes if available
5. text-derived JS logic when plain selectors are weak

Avoid overly fragile selectors based on long class name chains.

## Using Rodney from scripts

Rodney works well inside shell scripts.

Example:

```bash
rodney start --local
rodney open 'https://example.com'
rodney waitidle
rodney title
rodney js "document.body.innerText.slice(0,2000)"
```

For multiple pages, loop over URLs in shell or another scripting language and call Rodney repeatedly.

## Important reusable patterns

### Pattern: collect product or docs info
```bash
rodney newpage 'https://example.com/docs'
rodney waitidle
rodney title
rodney js "document.body.innerText.slice(0,5000)"
```

### Pattern: inspect site navigation
```bash
rodney newpage 'https://docs.example.com'
rodney waitidle
rodney js "JSON.stringify([...document.querySelectorAll('a')].map(a => ({text: a.innerText.trim(), href: a.href})).filter(x => x.text), null, 2)"
```

### Pattern: gather page structure
```bash
rodney js "JSON.stringify({
  h1: [...document.querySelectorAll('h1')].map(x => x.innerText),
  h2: [...document.querySelectorAll('h2')].map(x => x.innerText),
  code: [...document.querySelectorAll('code')].slice(0,30).map(x => x.innerText)
}, null, 2)"
```

### Pattern: authenticated crawling setup
```bash
rodney start --local --show
rodney open 'https://docs.example.com'
# log in manually or with input/click commands
rodney waitidle
```

After auth succeeds, continue using the same local session for all documentation extraction.

## Limitations to remember

- some sites block automation or rate-limit requests
- single-page apps may require extra waits
- login flows may involve redirects, cookies, or MFA
- text extraction can miss content hidden behind tabs or accordions
- `open` can occasionally fail on navigation-heavy pages; `newpage` is often more reliable

## Practical guidance

### Prefer `newpage` when:
- branching into new docs pages
- preserving the current page for reference
- dealing with unstable navigation

### Prefer `js` when:
- HTML is noisy
- you need structured extraction
- headings, links, or code blocks need summarizing

### Prefer `--show` when:
- selectors are hard to understand
- login needs visual confirmation
- automation seems flaky

## Minimal cheat sheet

```bash
rodney start --local --show
rodney open 'https://example.com'
rodney waitload
rodney waitidle
rodney title
rodney url
rodney js "document.body.innerText.slice(0,3000)"
rodney click 'button'
rodney input 'input[name="q"]' 'test'
rodney screenshot debug.png
rodney stop
```

## Final recommendation

For serious documentation extraction tasks, the best Rodney workflow is:
- use a local session
- use visible mode during login/setup
- use `newpage` generously
- always wait for idle/stability
- use `js` for structured extraction
- save outputs into local markdown or data files
