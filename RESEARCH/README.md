# RESEARCH: how my agent reads the web

Three free tools and one rule that decides which of them runs. Paste the rule into
your `CLAUDE.md`, add two servers, done.

None of it needs an account. Signing up only raises the limits.

---

## The rule

Paste this into `~/.claude/CLAUDE.md`:

```markdown
## Reading the web
- I have the URL: run `defuddle parse <url> --md` in Bash. Clean article text, nothing else.
- I don't know where the answer is: use exa (`web_search_exa`). Search and page text in one call.
- The page needs JavaScript, or defuddle comes back empty: use firecrawl (`firecrawl_scrape`).
- Never put a raw HTML page into the context.
```

The order is the point. The first tool runs on your own machine and costs no request.
The other two are hosted and rate-limited without an account, so they only get the
jobs the first one can't do.

---

## 01 · defuddle: you have the link

**<https://github.com/kepano/defuddle>**

Turns a page into the article and nothing else: no nav, no cookie banner, no
newsletter modal. If you took the REPOS drop, you already have it.

```bash
npm install -g defuddle-cli
defuddle parse https://example.com/some-article --md
```

---

## 02 · exa: you don't have the link

**<https://github.com/exa-labs/exa-mcp-server>**

A search engine built for models. One call returns the matching pages with their
text, so the agent doesn't search, then open, then read.

```bash
claude mcp add --transport http -s user exa https://mcp.exa.ai/mcp
```

The hosted server works anonymously with rate limits. For higher limits, sign in
with Exa when your client asks, or see their README.

`-s user` makes the server available in every folder, not only the one you are
standing in.

---

## 03 · firecrawl: the page needs a browser

**<https://github.com/firecrawl/firecrawl-mcp-server>**

Some pages are empty until JavaScript runs. Firecrawl loads them in a real
browser and hands back the text.

```bash
claude mcp add --transport http -s user firecrawl https://mcp.firecrawl.dev/v2/mcp
```

Without a key you get `firecrawl_scrape`, `firecrawl_search` and
`firecrawl_parse`, rate-limited. Crawl and map need an account.

---

## Check that it works

Same page, two ways:

```bash
URL=https://en.wikipedia.org/wiki/Markdown
curl -sL "$URL" | wc -w
defuddle parse "$URL" --md | wc -w
```

The first number is what lands in the context when you paste raw HTML. The
second is what your model actually needs. Then open Claude Code, type `/mcp`,
and check that exa and firecrawl show as connected.

---

## Why three and not one

| | When | Runs | Account |
|---|---|---|---|
| defuddle | you have the URL | on your machine | none |
| exa | you need to find the page | hosted | none, rate-limited |
| firecrawl | the page needs JavaScript | hosted | none for scrape, search, parse |

Have the link → read it locally. Don't have it → search. Page fights back →
send a browser.

---

defuddle, exa-mcp-server and firecrawl-mcp-server are MIT. Check each project's
terms before you ship commercially. This page is MIT.
