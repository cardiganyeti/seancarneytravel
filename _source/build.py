"""Builds Sean Carney Travel's static site from page fragments in ./pages."""
import os, re, pathlib

ROOT = pathlib.Path(__file__).parent
OUT = ROOT.parent / "site"
FORM = "https://secure.foratravel.com/intake/ZT49q4ptG1"
NEWSLETTER = "https://www.slowcrossings.com/subscribe"

NAV = [("Journal", "journal/index.html"), ("How I work", "how-i-work.html"), ("About", "about.html")]

def page(rel_out, title, description, body, current=None):
    depth = rel_out.count("/")
    up = "../" * depth
    nav = "".join(
        f'<li><a href="{up}{href}"{" aria-current=\"page\"" if current == label else ""}>{label}</a></li>'
        for label, href in NAV
    )
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,500&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}styles.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{up}index.html">Sean Carney <span>Travel Advisor</span></a>
    <nav aria-label="Main">
      <ul class="nav">{nav}<li><a class="button" href="{FORM}">Tell me about your trip</a></li></ul>
    </nav>
  </div>
</header>
<main id="main">
{body.replace("{UP}", up).replace("{FORM}", FORM).replace("{NEWSLETTER}", NEWSLETTER)}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div>
      <h2>Sean Carney, Travel Advisor</h2>
      <p>Based in Los Angeles. Usually somewhere with coffee and grey skies.</p>
      <p>An independent advisor with Fora Travel.</p>
    </div>
    <div>
      <h2>Get in touch</h2>
      <ul>
        <li><a href="{FORM}">Tell me about your trip</a></li>
        <li><a href="mailto:sean.carney@fora.travel">sean.carney@fora.travel</a></li>
        <li><a href="tel:+13109075730">+1 (310) 907-5730</a></li>
        <li><a href="{NEWSLETTER}">Get the newsletter</a></li>
      </ul>
    </div>
    <div>
      <h2>Elsewhere</h2>
      <ul>
        <li><a href="https://www.instagram.com/sean_carney_travel_advisor">Instagram</a></li>
        <li><a href="https://www.facebook.com/slowcrossings">Facebook</a></li>
        <li><a href="https://www.linkedin.com/in/carneysean/">LinkedIn</a></li>
        <li><a href="https://www.youtube.com/channel/UCuHdFoC1thOTfwFiiCjM_0Q">YouTube</a></li>
        <li><a href="{up}privacy.html">Privacy</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap"><p>&copy; 2026 Sean Carney. Photos are my own.</p></div>
</footer>
</body>
</html>
"""
    dest = OUT / rel_out
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html)

for f in sorted((ROOT / "pages").glob("**/*.html")):
    text = f.read_text()
    meta = dict(re.findall(r"<!--\s*(\w+):\s*(.*?)\s*-->", text.split("\n\n", 1)[0]))
    body = text.split("\n\n", 1)[1]
    rel = str(f.relative_to(ROOT / "pages"))
    page(rel, meta["title"], meta["description"], body, meta.get("current"))
    print("built", rel)
