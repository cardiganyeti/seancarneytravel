"""Builds Sean Carney Travel's static site from page fragments in ./pages."""
import os, re, pathlib, json, html as htmlmod

ROOT = pathlib.Path(__file__).parent
OUT = ROOT.parent / "site"
FORM = "https://secure.foratravel.com/intake/ZT49q4ptG1"
NEWSLETTER = "https://www.slowcrossings.com/subscribe"
SITE = "https://seancarneytravel.com/"
SITEMAP = []

NAV = [("Journal", "journal/index.html"), ("How I work", "how-i-work.html"), ("About", "about.html")]

def page(rel_out, title, description, body, current=None):
    depth = rel_out.count("/")
    up = "../" * depth
    nav = "".join(
        f'<li><a href="{up}{href}"{" aria-current=\"page\"" if current == label else ""}>{label}</a></li>'
        for label, href in NAV
    )
    url = SITE + ("" if rel_out == "index.html" else rel_out.replace("index.html", ""))
    SITEMAP.append(url)
    m = re.search(r'<img src="\{UP\}(img/[^"]+)"', body)
    img = SITE + (m.group(1) if m else "img/hero-breda-cafe.jpg")
    is_post = rel_out.startswith("journal/") and rel_out != "journal/index.html"
    head_title = re.sub(r"\s*\|.*$", "", title)
    t = htmlmod.escape(title, quote=True); d = htmlmod.escape(description, quote=True)
    person = {"@type": "Person", "name": "Sean Carney", "url": SITE + "about.html"}
    if is_post:
        ld = {"@context": "https://schema.org", "@type": "Article", "headline": head_title,
              "description": description, "image": img, "author": person,
              "publisher": person, "datePublished": "2026-11-11", "mainEntityOfPage": url}
    elif rel_out == "index.html":
        ld = {"@context": "https://schema.org", "@type": "TravelAgency", "name": "Sean Carney, Travel Advisor",
              "url": SITE, "image": img, "description": description, "telephone": "+1-310-907-5730",
              "email": "sean.carney@fora.travel", "areaServed": "Worldwide",
              "address": {"@type": "PostalAddress", "addressLocality": "Los Angeles", "addressRegion": "CA", "addressCountry": "US"},
              "founder": person,
              "sameAs": ["https://www.instagram.com/sean_carney_travel_advisor", "https://www.facebook.com/slowcrossings",
                         "https://www.linkedin.com/in/carneysean/", "https://www.youtube.com/channel/UCuHdFoC1thOTfwFiiCjM_0Q"]}
    else:
        ld = None
    seo = f"""<link rel="canonical" href="{url}">
<meta property="og:type" content="{'article' if is_post else 'website'}">
<meta property="og:site_name" content="Sean Carney, Travel Advisor">
<meta property="og:title" content="{htmlmod.escape(head_title, quote=True)}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{img}">
<meta name="twitter:card" content="summary_large_image">""" + (f'\n<script type="application/ld+json">{json.dumps(ld)}</script>' if ld else "")
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
{seo}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,500&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}styles.css">
<script>function loadScript(a){{var b=document.getElementsByTagName("head")[0],c=document.createElement("script");c.type="text/javascript",c.src="https://tracker.metricool.com/resources/be.js",c.onreadystatechange=a,c.onload=a,b.appendChild(c)}}loadScript(function(){{beTracker.t({{hash:"2556c45c4e3e2e1167f9219507665ba0"}})}});</script>
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

(OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + "".join(f"  <url><loc>{u}</loc></url>\n" for u in SITEMAP) + "</urlset>\n")
(OUT / "robots.txt").write_text("User-agent: *\nDisallow: /_source/\nDisallow: /media/\n\nSitemap: " + SITE + "sitemap.xml\n")
print("built sitemap.xml, robots.txt")
