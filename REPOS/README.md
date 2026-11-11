# REPOS: four open source projects that run a one-person company

All four are free. All four are open source. No Canva, no Notion AI, no
$49/month tool.

Here they are with the exact setup.

---

## 01 · gstack: skills that start themselves

**<https://github.com/garrytan/gstack>**

A stack of engineering skills for your coding agent: review, QA, ship,
security, planning. You don't invoke them. You describe what you're doing and
the right one loads itself.

The reason it matters isn't the skill count. It's that you stop re-typing the
same instructions into a fresh chat every morning.

```bash
git clone --single-branch --depth 1 \
  https://github.com/garrytan/gstack.git ~/.claude/skills/gstack \
  && cd ~/.claude/skills/gstack && ./setup
```

Needs Claude Code, Git and Bun. Then just work. `/review`, `/qa` and `/ship`
are there when you want to call one directly.

---

## 02 · defuddle: any link, clean text, no tab open

**<https://github.com/kepano/defuddle>**

Point it at a URL, get back clean Markdown: the article, without the nav, the
cookie banner, the newsletter modal, the related-posts grid.

```bash
npm install -g defuddle-cli
defuddle parse https://example.com/some-article
```

Use it instead of pasting a URL into a chat and hoping. Same content, a fraction
of the text, and you can read what the model is about to read.

---

## 03 · Playwright: render, don't design

**<https://github.com/microsoft/playwright>**

A browser you drive from code. It was built for testing; the interesting use is
that it will screenshot anything you can write in HTML.

```bash
npm install -D playwright
npx playwright install chromium
```

Write the layout in HTML and CSS once, feed it data, screenshot it at whatever
size you need. Every graphic comes out pixel-identical, and changing the brand
colour is one line, not thirty files.

It also means your visuals live in git: diffable, reviewable, revertable.
Design tools do not give you that.

---

## 04 · Caddy: one config file, every site you own

**<https://github.com/caddyserver/caddy>**

A web server that gets HTTPS certificates by itself and renews them by itself.
No certbot, no cron job, no expired-certificate morning.

```bash
brew install caddy   # or: apt install caddy
```

The entire config for a static site plus a proxied app:

```
example.com {
    root * /srv/site
    file_server
}

app.example.com {
    reverse_proxy localhost:3000
}
```

```bash
caddy reload
```

That's it. Certificates appear on their own.

---

## Why these four

They cover the whole loop, and each one replaces a subscription:

| | Does | Instead of |
|---|---|---|
| gstack | builds | re-typing the same brief |
| defuddle | reads | a dozen open tabs |
| Playwright | produces | a design subscription |
| Caddy | ships | a hosting dashboard |

Build → read → produce → deliver. That's a company.

---

Each project has its own licence. Check before you ship commercially.
This page is MIT.
