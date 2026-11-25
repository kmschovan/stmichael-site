# sitegen.py — generates the complete static site from the harvest
# Run: python sitegen.py   (from C:\Users\Kevin\stmichael-site)
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(BASE, "site")
HARVEST = json.load(open(os.path.join(BASE, "harvest", "site_content.json"), encoding="utf-8"))

# ---------------------------------------------------------------- helpers
def tgt(flag):
    return ' target="_blank" rel="noopener"' if flag else ''

def link(label, href, ext=False):
    return f'<a href="{href}"{tgt(ext)}>{label}</a>'

# ---------------------------------------------------------------- nav tree
NAV = [
    ("Home", "index.html", None),
    ("16:8", None, [
        ("Introduction", "168-introduction.html", False),
        ("Progress & Prayer Log", "168-progress.html", False),
        ("Weekly Reflections", "168-reflections.html", False),
    ]),
    ("About", None, [
        ("About Us", "about.html", False),
        ("Contact Us", "contact.html", False),
        ("FAQ", "faq.html", False),
        ("Mass Times", "mass-times.html", False),
        ("Eucharistic Adoration", "adoration.html", False),
        ("Holy Days of Obligation", "holy-days.html", False),
        ("Finding Us", "finding-us.html", False),
        ("Prayers & Intentions", "prayers.html", False),
    ]),
    ("Stewardship", None, [
        ("Time, Talent & Treasure", "time-talent-treasure.html", False),
        ("Regular Offertory", "offertory.html", False),
        ("Sacramentals Fund", "sacramentals-fund.html", False),
        ("Online Giving", "online-giving.html", False),
        ("Bishop's Appeal", "bishops-appeal.html", False),
    ]),
    ("Sacraments", None, [
        ("Baptism", "baptism.html", False),
        ("Confession", "confession.html", False),
        ("Communion", "communion.html", False),
        ("Confirmation", "confirmation.html", False),
        ("Marriage", "marriage.html", False),
        ("Holy Orders", "holy-orders.html", False),
        ("Anointing of the Sick", "anointing.html", False),
    ]),
    ("Resources", None, [
        ("Advent 2026", "advent-2026.html", False),
        ("OCIA — Becoming Catholic", "ocia.html", False),
        ("Order of the Mass", "order-of-mass.html", False),
        ("Daily Mass Readings", "daily-readings.html", False),
        ("Mass Details", "https://scheduler.stmichaelsallangels.com/display.html", True),
        ("Mass Details (mobile)", "https://scheduler.stmichaelsallangels.com/display_mobile.html", True),
        ("Scheduler", "https://scheduler.stmichaelsallangels.com/", True),
        ("Forms", "forms.html", False),
    ]),
]

FOOTER_COLS = [
    ("Our Parish", [
        ("Prayers & Intentions", "prayers.html", False),
        ("Parish Calendar", "calendar.html", False),
        ("Volunteer Signup", "https://scheduler.stmichaelsallangels.com/", True),
    ]),
    ("Stewardship", [
        ("Time, Talent & Treasure", "time-talent-treasure.html", False),
        ("Regular Offertory", "offertory.html", False),
        ("Sacramentals Fund", "sacramentals-fund.html", False),
        ("Online Giving", "online-giving.html", False),
        ("Bishop's Appeal", "bishops-appeal.html", False),
    ]),
    ("Connect", [
        ("Contact Us", "contact.html", False),
        ("Flocknote", "flocknote.html", False),
        ("Facebook", HARVEST["site"]["facebook"], True),
        ("Forms", "forms.html", False),
    ]),
]

CHURCH = HARVEST["site"]
CSS_VERSION = "20261121c"  # bump whenever site.css changes so browsers refetch
ORDO_URL = "https://ordinariate.net/ordo"
GIVING_WIX = "https://www.stmichaelsallangels.com/parishioner"

# ---------------------------------------------------------------- shared chrome
def header():
    items = []
    for label, href, subs in NAV:
        if subs:
            rows = "".join(link(l, h, e) for l, h, e in subs)
            items.append(f'<div class="has-sub"><a href="#">{label}</a><div class="sub">{rows}</div></div>')
        else:
            items.append(f'<a href="{href}">{label}</a>')
    nav_html = "".join(items)
    mobile = []
    for label, href, subs in NAV:
        if subs:
            mobile.append(f'<div class="grp">{label}</div>')
            mobile.extend(link(l, h, e) for l, h, e in subs)
        else:
            mobile.append(f'<a href="{href}">{label}</a>')
    mobile.append('<a href="online-giving.html" style="color:var(--gold-light)">Give Online &rarr;</a>')
    mobile_html = "".join(mobile)
    return f"""<header class="site">
  <div class="header-inner">
    <a class="brand" href="index.html">
      <img src="assets/images/crest.jpg" alt="Parish crest"
           style="width:46px;height:46px;border-radius:50%;border:1.5px solid var(--gold);object-fit:cover;">
      <div class="name">
        <strong>Saint Michael &amp; All Angels</strong>
        <small>Catholic Church &middot; Denison, TX</small>
      </div>
    </a>
    <nav class="main">{nav_html}<a href="online-giving.html" class="give">GIVE</a></nav>
    <button class="menu-btn" onclick="document.querySelector('.mobile-panel').classList.toggle('open')">&#9776; Menu</button>
  </div>
  <div class="mobile-panel">{mobile_html}</div>
</header>"""

# Website statistics beacon — posts one page view to the Church Hub per page load.
# Privacy-friendly: no cookies, no third parties; the server stores only a salted
# daily hash of request metadata (never the raw IP).
STATS_BEACON = """
<script>
(function () {
  try {
    var p = location.pathname.replace(/\\.html$/, '');
    if (p === '/' || p === '') p = '/home';
    fetch('https://scheduler.stmichaelsallangels.com/api/stats/visit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ path: p, referrer: document.referrer || '' }),
      keepalive: true
    }).catch(function () {});
  } catch (e) {}
})();
</script>
"""

def footer():
    cols = "".join(
        '<div><h4>' + t + '</h4>' + "".join(link(l, h, e) for l, h, e in links) + '</div>'
        for t, links in FOOTER_COLS)
    return f"""<footer>
  <div class="foot-grid">
    <div>
      <h4>{CHURCH['name']}</h4>
      <p class="mission">{CHURCH['address']}<br>{CHURCH['phone']}</p>
      <div class="foot-social">
        <a href="{CHURCH['flocknote']}" target="_blank" rel="noopener" aria-label="Flocknote" title="Flocknote" style="background:#fff;">
          <img src="assets/images/flocknote-sheep.svg" alt="Flocknote">
        </a>
        <a href="https://www.facebook.com/stmichaelallangel/" target="_blank" rel="noopener" aria-label="Facebook" title="Facebook">
          <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="12" fill="#1877F2"/><path d="M15.6 12.9l.4-2.4h-2.3V9.2c0-.7.4-1.3 1.4-1.3h1V6.4s-.9-.2-1.8-.2c-2 0-3.2 1.2-3.2 3.2v1.8H9.2v2.4h1.9v6h2.7v-6h1.8z" fill="#fff"/></svg>
        </a>
      </div>
    </div>
    {cols}
  </div>
  <div class="foot-bottom">
    <span>&copy; 2026 {CHURCH['name']} &middot; Denison, Texas</span>
    <span>Ordinariate of the Chair of Saint Peter</span>
  </div>
</footer>""" + STATS_BEACON

def page_head(title, desc):
    suffix = "" if "Saint Michael" in title else " — Saint Michael &amp; All Angels Catholic Church, Denison TX"
    return f"""<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}{suffix}</title>
<meta name="description" content="{desc}">
<link rel="icon" type="image/png" href="assets/images/crest-192.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/site.css?v={CSS_VERSION}">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Church","name":"{CHURCH['name']}","url":"https://www.stmichaelsallangels.com/","telephone":"{CHURCH['phone']}","address":{{"@type":"PostalAddress","streetAddress":"101 E Texas St","addressLocality":"Denison","addressRegion":"TX","postalCode":"75020","addressCountry":"US"}},"denomination":"Roman Catholic"}}
</script>
</head>"""

def give_card(note_html="", title="Give to Saint Michael &amp; All Angels"):
    """Branded card: external-page warning + button opening the ParishSoft giving form in a new tab."""
    note = f'<p style="margin:18px auto 0;font-size:.88rem;color:var(--ink);max-width:520px;">{note_html}</p>' if note_html else ""
    return f"""<div style="max-width:760px;margin:36px auto 0;background:#fff;border:1px solid var(--line);border-radius:14px;overflow:hidden;box-shadow:0 10px 30px rgba(20,50,79,.08);">
  <div style="background:var(--burgundy);color:#fff;padding:14px 24px;min-height:62px;display:flex;flex-direction:column;justify-content:center;align-items:flex-start;gap:4px;">
    <span style="font-family:'Cormorant Garamond',Georgia,serif;font-size:1.25rem;">{title}</span>
    <span style="font-family:'Inter',sans-serif;font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;color:var(--gold-light);">Secure &middot; ParishSoft Giving</span>
  </div>
  <div style="padding:40px 32px 44px;text-align:center;">
    <div style="background:var(--parchment);border-left:3px solid var(--gold);border-radius:0 8px 8px 0;padding:14px 18px;margin:0 auto 28px;max-width:520px;text-align:left;">
      <p style="margin:0;font-size:.88rem;color:var(--ink);line-height:1.55;">
        <strong>Heads up:</strong> you'll be leaving our website to visit
        <strong>ParishSoft Giving</strong>, the parish's external payment processor.
        The giving form opens in a new browser tab.
      </p>
    </div>
    <a class="btn btn-primary" style="font-size:1.08rem;padding:16px 44px;" href="https://giving.parishsoft.com/App/Form/1acdfb5d-b7b1-4b80-ad4b-5f7b16cfa05a" target="_blank" rel="noopener">Give Online Now &nearr;</a>
    <p style="font-size:.8rem;color:var(--muted);margin-top:14px;">One-time and recurring gifts &middot; bank drafts carry the lowest processing fee</p>
    {note}
  </div>
</div>"""

def make_page(fname, title, desc, body):
    html = f"""<!DOCTYPE html>
<html lang="en">
{page_head(title, desc)}
<body>
{header()}
{body}
{footer()}
<a class="give-float" href="online-giving.html">Online Giving &nearr;</a>
</body>
</html>"""
    with open(os.path.join(SITE, fname), "w", encoding="utf-8") as f:
        f.write(html)
    return fname

def subpage(fname, title, desc, eyebrow, hero_title, body, hero_sub=None):
    sub = f'<p>{hero_sub}</p>' if hero_sub else ''
    hero = f"""<div class="page-hero">
  <div class="eyebrow">{eyebrow}</div>
  <h1>{hero_title}</h1>
  {sub}
</div>
<section style="padding: 24px 0 76px;">
  <div class="wrap">{body}</div>
</section>"""
    return make_page(fname, title, desc, hero)

# ================================================================ HOMEPAGE
def build_home():
    body = f"""<section class="hero" id="home">
  <div class="hero-grid">
    <a class="btn btn-ghost btn-new" href="about.html">I&#8217;m New</a>
    <div>
      <h1>St. Michael &amp; All Angels</h1>
      <p class="welcome">A Roman Catholic community-in-formation under the <a href="https://ordinariate.net/" target="_blank" rel="noopener">Personal Ordinariate of the Chair of Saint Peter</a></p>
      <p class="sub">A small church with a big heart, serving North Texas and southern Oklahoma. We worship the Blessed Trinity in the beautiful and reverent Ordinariate form of the Roman Rite — focusing on evangelization through reverent liturgy, orthodox teaching, fellowship, and the spiritual life. We invite you to join us for prayer and worship.</p>
    </div>
    <figure class="hero-photo">
      <img src="assets/img/hero-church.jpg" alt="St. Michael's church with cross">
    </figure>
  </div>
</section>

<div class="mass-strip" id="mass">
  <div class="mass-inner">
    <div class="mass-cell"><div class="day">Wednesday</div><div class="time">6:30 pm</div><div class="note">Weekday Mass</div></div>
    <div class="mass-cell"><div class="day">Saturday Vigil</div><div class="time">6:00 pm</div><div class="note">English</div></div>
    <div class="mass-cell"><div class="day">Sunday</div><div class="time">8:00 &amp; 10:00 am</div><div class="note">English</div></div>
    <div class="mass-cell"><div class="day">Confession</div><div class="time">10:00 – 11:00 am</div><div class="note">Saturdays, or by appointment</div></div>
  </div>
</div>

<section class="band">
  <div class="wrap">
    <div class="band-tag">New &middot; Begins this Advent</div>
    <p class="verse">"Give thanks to the Lord, call upon His name, make known His deeds."</p>
    <p class="ref">— 1 Chronicles 16:8</p>
    <p><strong>16:8 at St. Michael's</strong> — a yearlong parish prayer initiative. We will begin Wednesday, December 2, 2026 — the first Wednesday of Advent — with a blessing of the candles. Bring your candle and join us as we begin this journey together.</p>
    <a class="btn btn-primary" style="background: var(--gold);" href="168-introduction.html">Learn About 16:8</a>
  </div>
</section>

<section id="sacraments">
  <div class="wrap">
    <div class="section-head">
      <div class="eyebrow">The Sacraments</div>
      <h2>The life of grace</h2>
      <div class="rule"></div>
    </div>
    <div class="cards">
      <a class="card" href="baptism.html">
        <h3>Baptism</h3>
        <p>"The basis of the whole Christian life, the gateway to life in the Spirit, and the door which gives access to the other sacraments."</p>
        <span class="more">Learn More</span>
      </a>
      <a class="card" href="confession.html">
        <h3>Confession</h3>
        <p>Saturdays 10:00 – 11:00 am, or by appointment with Father Randall. "Pardon from God's mercy... reconciled with the Church."</p>
        <span class="more">Learn More</span>
      </a>
      <a class="card" href="communion.html">
        <h3>Communion</h3>
        <p>"The holy Eucharist completes Christian initiation." Received kneeling at the altar rail by intinction, per the Ordinariate tradition.</p>
        <span class="more">Learn More</span>
      </a>
    </div>
  </div>
</section>

<section id="giving">
  <div class="wrap">
    <div class="section-head">
      <div class="eyebrow">Stewardship</div>
      <h2>Time &middot; Talent &middot; Treasure</h2>
      <div class="rule"></div>
    </div>
    <div class="give-grid">
      <div class="give-card">
        <h3>Regular Offertory</h3>
        <p>Contributions cover the day-to-day operations of the parish — Father's payroll, building maintenance, utilities, and our liturgical programs.</p>
        <a class="btn btn-ghost" href="offertory.html">Give Online</a>
      </div>
      <div class="give-card">
        <h3>Sacramentals Fund</h3>
        <p>Keeping our worship equipped with the essentials — the Paschal Candle, communion supplies, palms, and more. No donation is too small.</p>
        <a class="btn btn-ghost" href="sacramentals-fund.html">Give to the Fund</a>
      </div>
      <div class="give-card">
        <h3>Bishop's Appeal</h3>
        <p>Supporting the Ordinariate of the Chair of Saint Peter and its mission to proclaim Christ — vocations, communion, and connection.</p>
        <a class="btn btn-ghost" href="bishops-appeal.html">Learn More</a>
      </div>
    </div>
  </div>
</section>

"""
    return make_page("index.html",
        "Saint Michael & All Angels Catholic Church — Denison, TX",
        "A Roman Catholic community-in-formation in Denison, Texas under the Personal Ordinariate of the Chair of Saint Peter. Mass times, sacraments, stewardship, and a warm welcome.",
        body)

# ================================================================ CONTENT PAGES
PAGES = []

def P(fname, title, desc, eyebrow, hero_title, body, hero_sub=None, art=None):
    if art:
        body = f"""<div class="sacrament-layout">
<div class="sacrament-art"><img src="assets/images/{art}" alt="{hero_title} — sacred art"></div>
{body}
</div>"""
    PAGES.append((fname, title, desc, eyebrow, hero_title, body, hero_sub))

P("about.html", "About Us",
  "About Saint Michael & All Angels Catholic Church — a Roman Catholic community-in-formation under the Personal Ordinariate of the Chair of Saint Peter in Denison, Texas.",
  "About Us", "A small church with a big heart",
  f"""<div class="about-grid">
  <div class="text">
    <p class="lead">"We believe that the door to salvation is always open — and so are the doors to our church."</p>
    <p>We are a small Catholic church with a big heart — a <strong>community-in-formation</strong>, not yet large enough to be canonically established as a parish, serving North Texas and southern Oklahoma under the <a href="https://ordinariate.net/"{tgt(True)}>Personal Ordinariate of the Chair of Saint Peter</a>, established by Pope Benedict XVI in 2012 to welcome Anglicans seeking full communion with the Roman Catholic Church. Ordinariate parishes and churches are fully Roman Catholic, while retaining elements of Anglican heritage, enriching the faith through reverent liturgy and historical sacred music.</p>
    <p>All Catholics are warmly invited to join our Divine Worship liturgy and receive Holy Communion. Following the traditions of the Ordinariate, you kneel (if able) at the altar rail, where communion is administered by intinction &mdash; on the tongue.</p>
    <p>Our members generally come from across greater Grayson County, Texas, and southern Bryan County, Oklahoma. United by our love for Christ and our steadfast commitment to the teachings of the Roman Catholic Church, we celebrate our faith with reverence, joy, and warm hospitality, forming a vibrant and diverse community.</p>
    <p>If you are searching for a church home, we warmly invite you to visit us. Saint Michael and All Angels is a welcoming and loving family.</p>
  </div>
  <div class="about-photo">
    <img src="assets/images/church-tall-a.jpg" alt="Community life at Saint Michael &amp; All Angels">
  </div>
</div>
<div class="prose" style="margin-top: 44px;">
  <h2>Mass Readings</h2>
  <p>If you are interested in the specific readings for any day of the year, please see the <a href="{ORDO_URL}"{tgt(True)}>Ordinariate Ordo</a>.</p>
</div>""")

P("finding-us.html", "Finding Us",
  "Location, directions, and Mass times for Saint Michael & All Angels Catholic Church, 101 E Texas St, Denison, TX 75020.",
  "About Us", "Finding us",
  """<div class="visit-grid">
  <div>
    <ul class="hours">
      <li><span>Wednesday</span><span>6:30 pm — Weekday Mass</span></li>
      <li><span>Saturday</span><span>6:00 pm — Vigil Mass &middot; 10:00 am Confession</span></li>
      <li><span>Sunday</span><span>8:00 am &amp; 10:00 am — Mass (English)</span></li>
      <li><span>1st Friday</span><span>6:30 pm — First Friday Mass</span></li>
      <li><span>Confession</span><span>Saturdays 10–11 am, or by appointment</span></li>
    </ul>
    <p style="margin-top: 20px; color: var(--muted); font-size: .92rem;">
      Saint Michael &amp; All Angels Catholic Church<br>
      101 E Texas St, Denison, TX 75020<br>
      <a href="tel:9038217511">903-821-7511</a>
    </p>
    <a class="btn btn-primary" style="margin-top:18px" href="contact.html">Contact Us</a>
  </div>
  <iframe class="map-embed" style="min-height:380px;border:1px solid var(--line);"
    src="https://www.google.com/maps?q=101+E+Texas+St,+Denison,+TX+75020&output=embed"
    loading="lazy" title="Map to Saint Michael &amp; All Angels"></iframe>
</div>""")

P("holy-days.html", "Holy Days of Obligation",
  "The Holy Days of Obligation observed by Catholics, and by Saint Michael & All Angels Catholic Church (Ordinariate of the Chair of Saint Peter), Denison TX.",
  "About Us", "Holy Days of Obligation",
  f"""<p class="lead" style="margin-bottom: 26px;">In addition to Sunday Mass, Catholics are obliged to attend Holy Mass on the following Holy Days of Obligation:</p>
<div class="sched">
  <table>
    <tr><th>Holy Day</th><th>Date</th><th>What We Celebrate</th></tr>
    <tr>
      <td>Solemnity of Mary, the Holy Mother of God</td>
      <td>January 1</td>
      <td>The Octave Day of Christmas, honoring the Blessed Virgin Mary as the Mother of God.</td>
    </tr>
    <tr>
      <td>Solemnity of the Ascension of the Lord</td>
      <td>Thursday, the 40th day of Easter (movable)</td>
      <td>The Risen Christ ascends into heaven and is seated at the right hand of the Father. In the Ordinariate it is kept on its traditional Thursday.</td>
    </tr>
    <tr>
      <td>Solemnity of the Assumption of the Blessed Virgin Mary</td>
      <td>August 15</td>
      <td>At the end of her earthly life, Mary was taken up body and soul into heavenly glory.</td>
    </tr>
    <tr>
      <td>Solemnity of All Saints</td>
      <td>November 1</td>
      <td>The Church honors all the saints in heaven &mdash; those known by name and the countless unnamed.</td>
    </tr>
    <tr>
      <td>Solemnity of the Immaculate Conception</td>
      <td>December 8</td>
      <td>God preserved the Blessed Virgin Mary from all stain of original sin from the first moment of her conception. She is the Patroness of the United States.</td>
    </tr>
    <tr>
      <td>Solemnity of the Nativity of Our Lord Jesus Christ</td>
      <td>December 25</td>
      <td>Christmas &mdash; the Word became flesh and dwelt among us.</td>
    </tr>
  </table>
</div>
<div class="prose">
  <h2>Why We Keep Them &mdash; From the Heart</h2>
  <p>Catholics attend Holy Days of Obligation to worship God together, receive the Eucharist, and mark the great events and mysteries of salvation history. Beyond a church requirement, these days offer regular spiritual nourishment and a chance to respond to God&rsquo;s grace in love.</p>
  <ul style="list-style:none;padding-left:0;max-width:760px;">
    <li style="padding:8px 0 8px 26px;position:relative;"><span style="position:absolute;left:0;color:var(--gold);">✦</span><strong>Encounter Christ in the Eucharist.</strong> Mass provides spiritual nourishment through Scripture and Holy Communion, helping believers stay rooted in Christ rather than relying solely on private prayer.</li>
    <li style="padding:8px 0 8px 26px;position:relative;"><span style="position:absolute;left:0;color:var(--gold);">✦</span><strong>Honor the key mysteries of faith.</strong> Holy days spotlight the great moments involving Jesus, Mary, and the saints &mdash; Christmas, the Immaculate Conception, the Assumption, All Saints&rsquo; Day.</li>
    <li style="padding:8px 0 8px 26px;position:relative;"><span style="position:absolute;left:0;color:var(--gold);">✦</span><strong>Practice the virtue of religion.</strong> Giving God due worship and thanksgiving is a core moral act that puts love of God and neighbor first.</li>
    <li style="padding:8px 0 8px 26px;position:relative;"><span style="position:absolute;left:0;color:var(--gold);">✦</span><strong>Build communal faith.</strong> Worshipping alongside fellow Catholics unites the community and strengthens our shared faith.</li>
    <li style="padding:8px 0 8px 26px;position:relative;"><span style="position:absolute;left:0;color:var(--gold);">✦</span><strong>Fulfill a precept of the Church.</strong> As Ascension and Catholic Answers remind us, these obligations set an indispensable baseline for the life of prayer; missing Mass without a serious reason (such as illness) is considered a grave sin.</li>
  </ul>
</div>
<div class="prose">
  <h2>The Holy Days in 2027</h2>
  <p>Here is how the six Holy Days fall in the coming liturgical year, and when Mass is offered at Saint Michael's for each:</p>
  <div class="sched" style="margin-top:14px;">
    <table>
      <tr><th>Holy Day</th><th>Falls On</th><th>Masses at St. Michael's</th></tr>
      <tr><td>Mary, the Holy Mother of God</td><td><strong>Friday, January 1, 2027</strong></td><td>10:00 am &amp; 6:30 pm</td></tr>
      <tr><td>Ascension of the Lord</td><td><strong>Thursday, May 6, 2027</strong></td><td>6:30 pm</td></tr>
      <tr><td>Assumption of the Blessed Virgin Mary</td><td><strong>Sunday, August 15, 2027</strong></td><td>The Sunday Masses (8:00 &amp; 10:00 am) fulfill the obligation</td></tr>
      <tr><td>All Saints</td><td><strong>Monday, November 1, 2027</strong></td><td>6:30 pm &mdash; falling on a Monday, the obligation is lifted this year, but the feast is kept with Mass</td></tr>
      <tr><td>Immaculate Conception</td><td><strong>Wednesday, December 8, 2027</strong></td><td>6:30 pm</td></tr>
      <tr><td>Nativity of the Lord</td><td><strong>Saturday, December 25, 2027</strong></td><td>Midnight Mass at 12:00 am &amp; Christmas Day Mass at 10:00 am</td></tr>
    </table>
  </div>
  <p style="margin-top:14px;color:var(--muted);font-size:.9rem;">Each January we refresh this table for the new liturgical year, since the weekday a Holy Day falls on (and in a few cases, whether the obligation carries) changes from year to year.</p>
  <h2>What the Obligation Means</h2>
  <p>Attending Holy Mass on Sundays and Holy Days of Obligation is one of the precepts of the Church &mdash; the minimum asked of every Catholic. On those days the faithful are bound to participate in the Mass just as on Sunday, unless prevented by serious reason or dispensed by their pastor.</p>
  <p class="cite">Catechism of the Catholic Church, <a href="https://www.vatican.va/archive/ENG0015/__P7O.HTM"{tgt(True)}>2180</a></p>
  <h2>The Holy Days in Our Ordinariate</h2>
  <p>Upon the recommendation of the Governing Council in 2016, Bishop Steven J. Lopes decreed that the six solemnities listed above are observed as Holy Days of Obligation throughout the Personal Ordinariate of the Chair of Saint Peter. Two customs are particular to us: the Ascension is kept on its traditional date, the Thursday forty days after Easter, and whenever January 1, August 15, or November 1 falls on a Saturday or a Monday, the obligation to attend Mass is abrogated &mdash; the feast is still joyfully celebrated, but attendance is no longer required.</p>
  <h2>Holy Day Masses at Saint Michael's</h2>
  <p>When a Holy Day falls on a weekday, Holy Mass is ordinarily offered at 6:30 pm; when it falls on a Sunday, the Sunday Masses of that day fulfill the observance. Please see <a href="mass-times.html">Mass Times</a> for our standing weekly schedule, or the <a href="https://scheduler.stmichaelsallangels.com/"{tgt(True)}>Church Hub</a> for the exact Holy Day schedule, including Christmas and the Easter Triduum.</p>
</div>""")

P("mass-times.html", "Mass Times",
  "Mass schedule and confession times for Saint Michael & All Angels Catholic Church, Denison TX.",
  "Mass Times", "The Holy Sacrifice of the Mass",
  """<div class="sched">
  <table>
    <tr><th>Day</th><th>Time</th><th>Liturgy</th></tr>
    <tr><td>Wednesday</td><td>6:30 pm</td><td>Weekday Mass</td></tr>
    <tr><td>Saturday</td><td>6:00 pm</td><td>Vigil Mass (English)</td></tr>
    <tr><td>Sunday</td><td>8:00 am</td><td>Mass (English)</td></tr>
    <tr><td>Sunday</td><td>10:00 am</td><td>Mass (English)</td></tr>
    <tr><td>1st Friday of each month</td><td>6:30 pm</td><td>First Friday Mass</td></tr>
  </table>
</div>
<div class="prose">
  <h2>Confession</h2>
  <p>Saturdays from 10:00 – 11:00 am. For alternate times, please call Father Randall at <a href="tel:9038217511">903-821-7511</a>.</p>
  <h2>Holy Days of Obligation</h2>
  <p>In addition to Sunday Mass, Catholics are obliged to attend Holy Mass on six Holy Days — see <a href="holy-days.html">Holy Days of Obligation</a>.</p>
  <h2>Mass Readings</h2>
  <p>If you are interested in the specific readings for any day of the year, please see the <a href="https://ordinariate.net/ordo" target="_blank" rel="noopener">Ordinariate Ordo</a>.</p>
  <h2>Stay Informed</h2>
  <p>We invite you to join our mailing list to receive emails with news and special Mass schedules — see <a href="flocknote.html">Flocknote</a>.</p>
</div>""")

P("prayers.html", "Prayers & Intentions",
  "Submit prayer requests and Mass intentions to Saint Michael & All Angels Catholic Church.",
  "Our Parish", "Prayer Requests & Mass Intentions",
  """<div class="prose">
  <p>Please use the form below to send us your prayer requests and Mass Intentions. Due to the many prayer requests we receive, we will not be able to respond to your request — but please be assured our prayer teams will be praying for your prayer requests. For Mass Intentions, we will get back to you when we can schedule your request. May God bless you.</p>
</div>
<div class="contact-form" style="margin-top: 32px;">
  <form id="prayerForm" name="prayer-requests" method="POST">
    <label for="pr-name">Your Name (optional)</label>
    <input id="pr-name" name="name" type="text" placeholder="Your name">
    <label for="pr-intention">Prayer Request / Mass Intention *</label>
    <textarea id="pr-intention" name="intention" rows="6" required placeholder="For whom, or for what intention, shall we pray?"></textarea>
    <label for="pr-type">Request Type *</label>
    <select id="pr-type" name="type" required style="width:100%;padding:10px 12px;border:1px solid var(--line);margin-bottom:20px;">
      <option value="prayer">Prayer request only</option>
      <option value="mass">Mass intention (please schedule)</option>
    </select>
    <button class="btn btn-primary" type="submit">Send Request</button>
  </form>
  <div id="prayerThanks" style="display:none;background:rgba(176,122,42,.12);border:1px solid var(--gold);padding:16px 18px;margin-top:12px;">
    <strong>Thank you!</strong> To be sure we received your request, please call the parish office at <a href="tel:9038217511">903-821-7511</a>.
  </div>
</div>
<script>
document.getElementById("prayerForm").addEventListener("submit", function (e) {
  e.preventDefault();
  this.style.display = "none";
  document.getElementById("prayerThanks").style.display = "block";
});
</script>""")

P("calendar.html", "Parish Calendar",
  "Calendar of events at Saint Michael & All Angels Catholic Church, Denison TX.",
  "Our Parish", "Parish Calendar",
  """<div class="prose">
  <p>Upcoming parish events, holy days, and special liturgies will appear here. This page is ready for a Google Calendar embed — provide the parish calendar ID and the build will wire it in.</p>
</div>
<div class="placeholder" style="margin-top: 28px;">
  <h3>Calendar embed coming soon</h3>
  <p>Give Hermes the Google Calendar ID (or iCal address) for the parish calendar and the embed will be added automatically.</p>
</div>""")

P("finance-council.html", "Finance Council",
  "The Finance Council of Saint Michael & All Angels Catholic Church, Denison TX.",
  "Our Parish", "Finance Council",
  """<div class="prose">
  <p>The Finance Council advises the pastor on the temporal affairs of the parish — budgeting, facilities, and the responsible stewardship of the resources entrusted to us by our parishioners.</p>
</div>
<div class="placeholder" style="margin-top: 28px;">
  <h3>Content coming soon</h3>
  <p>This page was empty on the previous site. Add the council's membership, meeting schedule, and annual-report highlights, and Hermes will rebuild the page.</p>
</div>""")

P("parish-council.html", "Parish Council",
  "The Parish Council of Saint Michael & All Angels Catholic Church, Denison TX.",
  "Our Parish", "Parish Council",
  """<div class="prose">
  <p>The Parish Council serves as an advisory body to the pastor, representing the voice of parishioners in the pastoral life and mission of the parish.</p>
</div>
<div class="placeholder" style="margin-top: 28px;">
  <h3>Content coming soon</h3>
  <p>This page was empty on the previous site. Add the council's membership, meeting schedule, and current initiatives, and Hermes will rebuild the page.</p>
</div>""")

P("time-talent-treasure.html", "Time, Talent & Treasure",
  "Stewardship at Saint Michael & All Angels — sharing all that God has provided by giving back and growing together.",
  "Stewardship", "Time, Talent & Treasure",
  """<div class="prose">
  <p class="lead">Sharing all that God has provided you by giving back and growing together.</p>
  <h2>Time</h2>
  <p>Our time on earth — approximately 25,000 days — is precious and cannot be hoarded like grain. God created us to reach heaven, which is why He sent Jesus. Our earthly life is a journey toward heaven, requiring daily progress and devotion to God.</p>
  <p>Daily prayer fosters a personal relationship with God, where we share our joys, sorrows, and seek His guidance. Reading Scripture daily allows us to meditate on His word and understand His boundless love for us.</p>
  <p>Giving our time to assist others and organizations glorifies God, allowing Christ to work through us. Your gift of time is irreplaceable — only you can offer it.</p>
  <h2>Talent</h2>
  <p>Each of us possesses unique talents and gifts, demonstrating God's boundless power and magnificence. These gifts aren't solely for our benefit; they are meant to enrich the lives of others and enhance our service to God.</p>
  <p>St. Peter urges us to steward these gifts responsibly for the service of others, recognizing the diverse graces bestowed upon us by God.</p>
  <p>In our parish and community, we are called to embody Christ's works:</p>
  <ul>
    <li>Visiting the sick and elderly</li>
    <li>Feeding the hungry</li>
    <li>Teaching the eager</li>
    <li>Comforting the lonely and grieving</li>
    <li>Offering prayers and support</li>
  </ul>
  <p>Being Christ's hands and voice in the world — by engaging in these Spiritual and Corporal Works of Mercy, we become partners with Christ in the work of redemption. As St. Francis of Assisi taught: <em>"It is in giving that we receive."</em></p>
  <h2>Treasure</h2>
  <p>The parable of the talents (Matthew 25:14–30) illustrates the Christian responsibility to share our material gifts. The first servant doubles five talents, the second doubles two, but the third buries one. The master praises the first two but rebukes the third for not utilizing the gift. This teaches us that God expects us to steward our resources — not bury them.</p>
  <p>Our material treasure, like our time and talent, is entrusted to us by God. Returning a deliberate, planned portion to the parish supports the works of the Church and is an act of thanksgiving. Your generous sharing of treasure gives you a vital share in St. Michael's mission to make known the love and salvation of the Lord Jesus Christ — helping us extend our ministry throughout the Denison/Sherman and Grayson County area, so we can go even further making new disciples of Jesus Christ.</p>
  <p style="margin-top: 28px;"><a class="btn btn-primary" href="offertory.html">Ways to Give</a></p>
</div>""")

P("offertory.html", "Regular Offertory",
  "Contributions to the Regular Offertory of Saint Michael & All Angels.",
  "Stewardship", "Regular Offertory",
  """<div class="prose">
  <p>Contributions to the Regular Offertory are crucial in covering the expenses associated with the day-to-day operations of the parish and its programs. These expenses encompass Father's payroll, building maintenance, utilities, and daily supplies, along with supporting our sacramental preparation services and liturgical programs.</p>
  <p><strong>Your generous offering gives you a vital share in St. Michael's mission to make known the love and salvation of the Lord Jesus Christ.</strong> Help us extend our ministry throughout the Denison/Sherman and Grayson County area, so we can go even further making new disciples of Jesus Christ.</p>
  <p>You can contribute traditionally by placing your offering in the offertory plate during Mass. Alternatively, we encourage parish members to set up a recurring gift using the Online Giving tool on this website. Through this tool, you'll have full control over the amount and frequency of your contributions.</p>
  <p>We deeply appreciate your investment in and ongoing support of your parish. Thank you.</p>
  <p style="margin-top: 28px;"><a class="btn btn-primary" href="online-giving.html">Give Online Now</a></p>
</div>""")

P("sacramentals-fund.html", "Sacramentals Fund",
  "Support the Sacramentals Fund — keeping our worship equipped with the essentials.",
  "Stewardship", "Sacramentals Fund",
  """<div class="prose">
  <p>We are excited to continue the impactful legacy of our Sacramentals Fund, which was established thanks to the extraordinary generosity of our church community.</p>
  <p>This fund ensures that our church is always equipped with the essential items that enrich our worship — from the Easter Paschal Candle to communion supplies, palms, and more. These sacred elements not only illuminate our physical space but also symbolize the light of Christ in our lives.</p>
  <p>As we look ahead, we invite you to join us in sustaining this vital fund. Your contributions, no matter the size, help keep our spiritual journey vibrant and our worship deeply meaningful.</p>
</div>

<div class="fund-row">
  <div class="fund-meter-card">
    <div class="fund-meter-head">
      <span class="fund-meter-title" id="fund-label">Immediate Goal</span>
      <span class="fund-meter-tag">Goal Meter</span>
    </div>
    <div class="fund-meter-body thermo">
      <div class="fund-nums">
        <div><span class="fund-cap">Goal</span><span class="fund-big" id="fund-goal">$0</span></div>
        <div><span class="fund-pct" id="fund-pct">0%</span> <span class="fund-cap">of goal</span><br><span class="fund-big" id="fund-raised">$0</span><span class="fund-cap" id="fund-raised-cap">given so far</span></div>
        <div><span class="fund-big" id="fund-remaining">$0</span><span class="fund-cap" id="fund-remaining-cap"></span></div>
      </div>
      <div class="thermo-scale">
        <div class="thermo-track" id="fund-bar-track" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0">
          <div class="thermo-fill" id="fund-fill"></div>
        </div>
        <span class="thermo-mark" style="bottom:25%">25%</span>
        <span class="thermo-mark" style="bottom:50%">50%</span>
        <span class="thermo-mark" style="bottom:75%">75%</span>
      </div>
    </div>
    <div class="fund-meter-foot" style="padding-top:0;">
      <p class="fund-updated" id="fund-updated"></p>
    </div>
  </div>
  <div class="fund-give-col">
  """
  + give_card('When the form opens, be sure to choose <strong>&ldquo;Sacramentals Fund&rdquo;</strong> from the fund drop-down — that directs your gift to candles, palms, communion supplies, and more.', title='Give to the Sacramental Fund') + """
  </div>
</div>
<p style="max-width:1060px;margin:14px auto 0;font-size:.85rem;color:var(--muted);text-align:center;">
  Gifts are processed securely by <strong>ParishSoft Giving</strong>. Questions about the fund? Call the parish office.
</p>

<div class="prose">
  <p>Thank you for your unwavering support and blessings!</p>
</div>

<script>
(function () {
  var fmt = function (n) { return '$' + n.toLocaleString('en-US'); };
  fetch('assets/data/fund.json').then(function (r) { return r.json(); }).then(function (d) {
    var goal = d.goal || 0, raised = Math.min(d.raised || 0, goal);
    var pct = goal > 0 ? Math.round(raised / goal * 100) : 0;
    document.getElementById('fund-label').textContent = d.label || 'Immediate Goal';
    document.getElementById('fund-raised').textContent = fmt(d.raised || 0);
    document.getElementById('fund-goal').textContent = fmt(goal);
    document.getElementById('fund-pct').textContent = pct + '%';
    document.getElementById('fund-bar-track').setAttribute('aria-valuenow', pct);
    var fill = document.getElementById('fund-fill');
    fill.style.height = pct + '%';
    var rem = goal - (d.raised || 0);
    if (rem <= 0) {
      document.getElementById('fund-remaining').textContent = '$0';
      document.getElementById('fund-raised-cap').textContent = 'goal reached — thank you!';
    } else {
      document.getElementById('fund-remaining').textContent = '$0';
    }
    if (d.updated) {
      var dt = new Date(d.updated + 'T12:00:00');
      document.getElementById('fund-updated').textContent = 'Progress updated ' + dt.toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' }) + '.';
    }
  }).catch(function () {
    var fill = document.getElementById('fund-fill');
    fill.style.height = '100%';
    fill.style.background = 'var(--line)';
  });
})();
</script>""")

P("online-giving.html", "Online Giving",
  "Give online to Saint Michael & All Angels — one-time or recurring gifts.",
  "Stewardship", "Online Giving",
  """<div class="prose">
  <p>Online giving is a convenient and secure way to support the parish — whether you're giving to the Regular Offertory, the Sacramentals Fund, or a special collection. Through the giving form you have full control over the amount and frequency of your contributions, and you can set up recurring gifts so your support continues even when you're away.</p>
  <p><strong>Your generous online gift gives you a vital share in St. Michael's mission to make known the love and salvation of the Lord Jesus Christ.</strong> Help us extend our ministry throughout the Denison/Sherman and Grayson County area, so we can go even further making new disciples of Jesus Christ.</p>
</div>
"""
  + give_card() + """
<p style="max-width:760px;margin:14px auto 0;font-size:.85rem;color:var(--muted);text-align:center;">
  Gifts are processed securely by <strong>ParishSoft Giving</strong> — the same system used for parish faith-formation and fee payments. Questions about giving? Call the parish office.
</p>""")

P("bishops-appeal.html", "Bishop's Appeal",
  "Support the Bishop's Appeal of the Ordinariate of the Chair of Saint Peter.",
  "Stewardship", "Bishop's Appeal",
  """<div class="prose">
  <p>The Bishop's Appeal provides essential support for the Ordinariate of the Chair of Saint Peter and its mission to proclaim Christ.</p>
  <p>Your generosity toward this annual appeal helps in our mission that all may have a personal relationship with the Lord Jesus and receive Him as the Bread of Life. Your gift helps invigorate services and programs that connect the Ordinariate's faithful to their bishop and to their brothers and sisters across the diocese, invites new members into full communion, and cultivates vocations to the priesthood and religious life — further spreading our Eucharistic faith.</p>
  <p style="margin-top: 28px;"><a class="btn btn-primary" href="https://www.stmichaelsallangels.com/parishioner" target="_blank" rel="noopener">Give to the Bishop's Appeal</a></p>
</div>""")

P("baptism.html", "Baptism",
  "Holy Baptism — the basis of the whole Christian life and the gateway to the other sacraments.",
  "The Sacraments", "Holy Baptism",
  """<div class="prose">
  <p class="lead">"Holy Baptism is the basis of the whole Christian life, the gateway to life in the Spirit, and the door which gives access to the other sacraments."</p>
  <p>Through Baptism we are freed from sin and reborn as sons of God; we become members of Christ, are incorporated into the Church and made sharers in her mission.</p>
  <p>As the first of the seven Sacraments, and the way by which to receive the other Sacraments, Baptism unites us to Christ, who died for us and repaired our relationship with God the Father. The Sacrament of Baptism signifies our new life in Christ, as the believer receives not only remission of original and personal sin but also the various fruits, gifts, and virtues necessary to live a holy life.</p>
  <p>Through the waters of Baptism, the believer is incorporated into the Body of Christ, the Church.</p>
  <p style="color:var(--muted);font-size:.86rem;"><a href="https://www.vatican.va/archive/ENG0015/__P3G.HTM" target="_blank" rel="noopener">— Catechism of the Catholic Church, 1213</a></p>
  <h2>Arranging a Baptism</h2>
  <p>To arrange a baptism for an infant or an adult, please call the parish at <a href="tel:9038217511">903-821-7511</a>. Preparation is coordinated with Father Randall.</p>
</div>""", art="art-baptism.webp")

P("confession.html", "Confession",
  "The Sacrament of Reconciliation — confession times and the grace of God's mercy.",
  "The Sacraments", "The Sacrament of Reconciliation",
  """<div class="prose">
  <p class="lead">"Those who approach the sacrament of Penance obtain pardon from God's mercy for the offense committed against Him, and are, at the same time, reconciled with the Church which they have wounded by their sins."</p>
  <p>In the Sacrament of Reconciliation, we approach God understanding how sin has hurt our soul and ask for His love and mercy. Confession helps us acknowledge our sinfulness, receive God's forgiveness, and labor — by charity, example, and prayer — for the conversion of others.</p>
  <p style="color:var(--muted);font-size:.86rem;"><a href="https://www.vatican.va/archive/ENG0015/__P46.HTM" target="_blank" rel="noopener">— Catechism of the Catholic Church, 1422</a></p>
  <h2>Confession Times</h2>
  <p><strong>Saturdays from 10:00 &ndash; 11:00 am</strong> at the parish.</p>
  <p>For alternate times, please call Father Randall at <a href="tel:9038217511">903-821-7511</a>.</p>

  <h2>Prepare for Confession</h2>
  <p>Before coming to the sacrament, prepare your heart with our companion pages &mdash; each is drawn from the Church&rsquo;s traditional examination of conscience:</p>
  <div style="max-width:760px;margin:14px auto 0;background:#fff;border:1px solid var(--line);padding:6px 24px;">
  <a href="examination-of-conscience.html" style="display:block;padding:9px 0;border-bottom:1px solid var(--line);text-decoration:none;font-weight:600;">Examination of Conscience</a>
  <a href="precepts-of-the-church.html" style="display:block;padding:9px 0;border-bottom:1px solid var(--line);text-decoration:none;font-weight:600;">Precepts of the Church</a>
  <a href="how-to-go-to-confession.html" style="display:block;padding:9px 0;text-decoration:none;font-weight:600;">How to Go to Confession</a>
  </div>
  <p style="margin-top:16px;">The USCCB offers an examination of conscience for each state in life &mdash; choose yours:</p>
  <div style="max-width:760px;margin:14px auto 0;background:#fff;border:1px solid var(--line);padding:6px 24px;">
  <a href="https://www.usccb.org/prayer-and-worship/sacraments-and-sacramentals/penance/sacrament-reconciliation-children-examination-conscience" target="_blank" rel="noopener" style="display:block;padding:9px 0;border-bottom:1px solid var(--line);text-decoration:none;font-weight:600;">For Children</a>
  <a href="https://www.usccb.org/prayer-and-worship/sacraments-and-sacramentals/penance/sacrament-reconciliation-young-adults-examination-of-conscience" target="_blank" rel="noopener" style="display:block;padding:9px 0;border-bottom:1px solid var(--line);text-decoration:none;font-weight:600;">For Young Adults</a>
  <a href="https://www.usccb.org/prayer-and-worship/sacraments-and-sacramentals/penance/examination-of-conscience-for-single-people" target="_blank" rel="noopener" style="display:block;padding:9px 0;border-bottom:1px solid var(--line);text-decoration:none;font-weight:600;">For Single People</a>
  <a href="https://www.usccb.org/prayer-and-worship/sacraments-and-sacramentals/penance/sacrament-reconciliation-married-persons-examination-of-conscience" target="_blank" rel="noopener" style="display:block;padding:9px 0;text-decoration:none;font-weight:600;">For Married Persons</a>
  </div>

  <h2>Confession is a Place of Victory</h2>
  <p>Fr. Mike Schmitz puts words to the heart of it: confession is not a defeat for the sinner but the place where the war is finally won. Take a few minutes with this &mdash; and then come see for yourself on a Saturday morning.</p>
  <div class="video-embed" style="margin-top: 20px;">
    <iframe src="https://www.youtube-nocookie.com/embed/YiVjwlUO9Sc?rel=0" title="Confession is a Place of Victory — Ascension Presents" loading="lazy" allowfullscreen allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin"></iframe>
  </div>
  <p class="video-caption">Watch: <strong>Confession is a Place of Victory</strong> &mdash; with thanks to <a href="https://www.youtube.com/@AscensionPresents" target="_blank" rel="noopener">Ascension Presents</a> on YouTube.</p>
</div>""", art="art-confession.webp")

P("adoration.html", "Eucharistic Adoration",
  "Eucharistic Adoration at Saint Michael & All Angels — a quiet hour with Our Lord every Saturday morning, with confession available at the same time.",
  "About Us", "An hour with Our Lord",
  """<div class="prose">
  <p class="lead"><em>&ldquo;Could you not watch with me one hour?&rdquo;</em> &mdash; <a href="https://www.biblegateway.com/passage/?search=Matthew%2026:40&version=RSVCE" target="_blank" rel="noopener">Matthew 26:40</a></p>
  <p>The first invitation in Eucharistic Adoration is the Lord&rsquo;s own. Beginning soon, every Saturday morning the <strong>Blessed Sacrament will be exposed on the altar</strong> of Saint Michael &amp; All Angels while Father Randall hears confessions next door &mdash; a full hour of quiet, of presence, of simply being with Him. Bring the concern you have been carrying, the thanksgiving you have been saving, or nothing at all. He does the rest.</p>
  <h2>Saturday Mornings &mdash; 10:00 to 11:00 am</h2>
  <p>From <strong>10:00 to 11:00 am every Saturday</strong> the monstrance will stand on the altar and the church will be hushed and open. This is not a program and not a meeting &mdash; it is an audience with the King of Kings, and the most peaceful hour of your week.</p>
  <h2>Two Halves, One Hour</h2>
  <p><strong>All are welcome</strong> &mdash; and we encourage a large crowd for adoration. The sign-ups exist for one reason: to guarantee that <strong>at least one person is present with Our Lord at all times</strong> throughout the hour.</p>
  <p>The halves are also for you. The hour is kept in <strong>two 30-minute halves</strong> &mdash; the <strong>first half, 10:00 &ndash; 10:30 am</strong>, and the <strong>second half, 10:30 &ndash; 11:00 am</strong> &mdash; precisely so that those signing up have time for confession too: adore one half, and receive the sacrament in the other while another adorer keeps watch. Of course, you may also take both halves and keep the whole hour for Him.</p>
  <h2>Take a Half &mdash; or the Whole Hour</h2>
  <p>Adoration sign-ups live in the <strong>Church Hub</strong> &mdash; the same place you volunteer for Mass roles and log your 16:8 prayer. <strong>Anyone can join</strong>: sign in, choose your Saturday, and take a half; the schedule fills in as adorers sign up, so you can always see who is keeping watch.</p>
  <p><strong>One person can take both halves</strong> and keep the whole hour for Him &mdash; or, if you only have 30 minutes, take one half and know that another adorer has the other. Either way, you'll have your half-hour for confession: <em>come for adoration, stay for confession.</em></p>
  <div style="text-align:center;margin: 26px 0;">
    <a class="btn btn-primary" style="font-size:1.02rem;padding:15px 34px;" href="https://scheduler.stmichaelsallangels.com/?view=adoration" target="_blank" rel="noopener">Sign Up for Adoration &rarr;</a>
  </div>
  <p style="font-size:.95rem;">Need a Church Hub account? Call the parish office at <a href="tel:9038217511">903-821-7511</a> and we will set you up &mdash; then take any open half you like.</p>
  <div style="max-width:640px;margin:30px auto;border-left:3px solid var(--gold);background:#fff;padding:20px 26px;">
    <p style="margin:0;font-size:.95rem;color:var(--ink);"><strong style="color:var(--burgundy);">While you keep watch</strong> &mdash; confession is available in the church office from 10:00 to 11:00 am. Arrive with your hour and leave with a clean heart: <em>come for adoration, stay for confession.</em></p>
  </div>
</div>""", art="adoration-monstrance.jpg")

P("communion.html", "Communion",
  "The Holy Eucharist — the source and summit of the Christian life.",
  "The Sacraments", "The Holy Eucharist",
  """<div class="prose">
  <p class="lead">"The holy Eucharist completes Christian initiation. Those who have been raised to the dignity of the royal priesthood by Baptism and configured to Christ by Confirmation participate with the whole community in the Lord's own sacrifice."</p>
  <p>The Eucharist is the source and summit of the Christian life. In the Blessed Sacrament, Christ is truly present — Body, Blood, Soul, and Divinity — under the appearances of bread and wine.</p>
  <p style="color:var(--muted);font-size:.86rem;"><a href="https://www.vatican.va/archive/ENG0015/__P3W.HTM" target="_blank" rel="noopener">— Catechism of the Catholic Church, 1322</a></p>
  <h2>Receiving Holy Communion at Saint Michael's</h2>
  <p>All Catholics free from grave sin and properly disposed are welcome to receive Holy Communion at our Masses. Following the traditions of the Ordinariate, you kneel (if able) at the altar rail, where Father Randall comes to each communicant and administers communion <strong>by intinction &mdash; on the tongue</strong>: the Eucharistic host is dipped into the precious blood and placed on the communicant's tongue.</p>
</div>""", art="art-communion.webp")

P("confirmation.html", "Confirmation",
  "The sacrament of Confirmation — the seal of the Holy Spirit at Saint Michael & All Angels.",
  "The Sacraments", "The Sacrament of Confirmation",
  """<div class="prose">
  <p class="lead">"Baptism, the Eucharist, and the sacrament of Confirmation together constitute the 'sacraments of Christian initiation,' whose unity must be safeguarded."</p>
  <p>In Confirmation, the baptized are more perfectly bound to the Church and are enriched with the special strength of the Holy Spirit. Through the anointing with chrism and the laying on of hands, the soul receives a permanent seal — the mark that consecrates us for Christian service.</p>
  <p>The Spirit strengthens us to witness to Christ boldly, in word and in deed, and to live out our baptismal calling as mature members of the Body of Christ.</p>
  <p style="color:var(--muted);font-size:.86rem;"><a href="https://www.vatican.va/archive/ENG0015/__P3P.HTM" target="_blank" rel="noopener">— Catechism of the Catholic Church, 1285</a></p>
  <h2>Receiving Confirmation</h2>
  <p>Preparation for Confirmation — for youth and for adults entering the Church through the Ordinariate — is coordinated through the parish. Please contact the office at <a href="tel:9038217511">903-821-7511</a> to learn about the next formation program.</p>
</div>""", art="art-confirmation.webp")

P("marriage.html", "Marriage",
  "The sacrament of Holy Matrimony — the covenant of love at Saint Michael & All Angels.",
  "The Sacraments", "The Sacrament of Holy Matrimony",
  """<div class="prose">
  <p class="lead">"The matrimonial covenant, by which a man and a woman establish between themselves a partnership of the whole of life, is by its nature ordered toward the good of the spouses and the procreation and education of offspring."</p>
  <p>Marriage between baptized persons is a true sacrament — a living sign of Christ's unfailing love for His Church. In the exchange of consent, the couple gives themselves to one another completely and irrevocably, and Christ himself strengthens and sanctifies that bond.</p>
  <p>Grounded in the nuptial blessing of the Church's tradition, the wedding liturgy at Saint Michael's draws from the Church's rich treasury — sacred music, reverent ritual, and the solemn vows exchanged before God and His people.</p>
  <p style="color:var(--muted);font-size:.86rem;"><a href="https://www.vatican.va/archive/ENG0015/__P50.HTM" target="_blank" rel="noopener">— Catechism of the Catholic Church, 1601</a></p>
  <h2>Arranging a Wedding</h2>
  <p>Arrangements for marriage at the parish should begin at least six months in advance, allowing time for preparation, instruction, and scheduling with Father Randall. Please call the parish office at <a href="tel:9038217511">903-821-7511</a> to begin.</p>
</div>""", art="art-marriage.webp")

P("holy-orders.html", "Holy Orders",
  "The sacrament of Holy Orders — the priesthood of Jesus Christ, conferred through the bishop.",
  "The Sacraments", "The Sacrament of Holy Orders",
  """<div class="prose">
  <p class="lead">"Holy Orders is the sacrament through which the mission entrusted by Christ to his apostles continues to be exercised in the Church until the end of time."</p>
  <p>Through the anointing of the Holy Spirit and the laying on of hands by the bishop, men are configured to Christ in one of three degrees: episcopate (bishops), presbyterate (priests), and diaconate (deacons). Each shares, in his own degree, in the ministry of teaching, sanctifying, and governing the people of God.</p>
  <p>Our parish is shepherded by this same sacrament — Father Randall's priestly ministry, from the celebration of the Mass to the absolution of sins in the confessional, flows from his ordination in service of Christ and His flock.</p>
  <p style="color:var(--muted);font-size:.86rem;"><a href="https://www.vatican.va/archive/ENG0015/__P4R.HTM" target="_blank" rel="noopener">— Catechism of the Catholic Church, 1536</a></p>
  <h2>Considering a Vocation?</h2>
  <p>If you, or someone you know, feels called to the priesthood or diaconate, Father Randall would be glad to talk with you. Call the parish office at <a href="tel:9038217511">903-821-7511</a>, or visit the <a href="https://ordinariate.net/" target="_blank" rel="noopener">Ordinariate's vocations page</a>.</p>
</div>""", art="art-holy-orders.webp")

P("anointing.html", "Anointing of the Sick",
  "The sacrament of Anointing of the Sick — Christ's healing grace in times of illness.",
  "The Sacraments", "Anointing of the Sick",
  """<div class="prose">
  <p class="lead">"Is anyone among you sick? Let him call for the elders of the church, and let them pray over him, anointing him with oil in the name of the Lord."</p>
  <p class="cite">— James 5:14-15</p>
  <p>The Church believes and confesses that this sacrament — once called Extreme Unction — is Christ's special gift for those facing serious illness, advanced age, or the frailty of life. Through the anointing with blessed oil and the prayer of the priest, the sick receive grace, strength, peace, and, when it is God's will, healing.</p>
  <p>The sacrament may also be received before serious surgery, and those who are chronically ill may receive it more than once. It is never to be feared: it is a visitation of Christ's mercy and comfort.</p>
  <p style="color:var(--muted);font-size:.86rem;"><a href="https://www.vatican.va/archive/ENG0015/__P4K.HTM" target="_blank" rel="noopener">— Catechism of the Catholic Church, 1511</a></p>
  <h2>Requesting the Sacrament</h2>
  <p>To request anointing for yourself or a loved one — at the church, at home, or in the hospital — please call Father Randall at <a href="tel:9038217511">903-821-7511</a>. In urgent situations, call at any time.</p>
</div>""", art="art-anointing.webp")

P("168-introduction.html", "16:8 — Introduction",
  "16:8 at St. Michael's — a yearlong parish prayer initiative: one hour of Eucharistic Adoration each week, twenty minutes of personal prayer each day.",
  "16:8", "16:8 at St. Michael's — Begin With Us",
  """<div class="sacrament-layout">
<div class="sacrament-art seal-art"><img src="assets/img/168-seal.png" alt="16:8 at St. Michael's seal — Saint Michael the Archangel"></div>
<div class="prose">
  <p class="lead">We all carry burdens &mdash; family struggles, illness, grief, broken relationships. 16:8 is an invitation to bring those things to God, pray with faith, and carry our crosses with Christ.</p>
  <p>16:8 at St. Michael's is a yearlong parish prayer initiative. Its heart is a deeper relationship with Christ through consistent prayer and Eucharistic Adoration &mdash; hopeful, reverent, and open to everyone.</p>
  <blockquote>"Give thanks to the Lord, call upon His name, and make His deeds known."<div class="cite"><a href="https://www.biblegateway.com/passage/?search=1%20Chronicles%2016%3A8&version=RSVCE" target="_blank" rel="noopener">&mdash; 1 Chronicles 16:8</a></div></blockquote>
</div>
</div>

<div class="prose">
  <h2>The Name</h2>
  <p>The name holds two ideas together. There are <strong>168 hours in a week</strong> &mdash; and <strong><a href="https://www.biblegateway.com/passage/?search=1%20Chronicles%2016%3A8&version=RSVCE" target="_blank" rel="noopener">1 Chronicles 16:8</a></strong> calls us to give thanks to the Lord, call upon His name, and make His deeds known.</p>

  <h2>The Commitment</h2>
  <p>Participants are invited to commit to two simple practices:</p>
</div>
<div class="cards cards-168">
  <a class="card" href="168.html" style="pointer-events:none;">
    <h3>One Hour Weekly</h3>
    <p>One hour of Eucharistic Adoration each week &mdash; Wednesday evenings at St. Michael's.</p>
    <span class="more">Wednesday Evenings</span>
  </a>
  <a class="card" href="168.html" style="pointer-events:none;">
    <h3>Twenty Minutes Daily</h3>
    <p>Twenty minutes of personal prayer each day &mdash; at home, in a quiet moment, wherever you are.</p>
    <span class="more">Every Day</span>
  </a>
  <a class="card" href="168.html" style="pointer-events:none;">
    <h3>168 Hours a Year</h3>
    <p>Together, that is approximately 168 hours of prayer per person over the year.</p>
    <span class="more">One Year</span>
  </a>
</div>
<div class="prose">
  <p>Our beginning goal is <strong>30 commitments</strong> &mdash; about 5,040 hours of prayer offered over the year. But the deeper goal is changed lives: even one person encountering Christ more deeply makes this worthwhile.</p>
  <p>We believe God hears our prayers. We believe miracles can and do happen. We seek healing and trust in His perfect timing and presence during our challenges.</p>
</div>

<div style="max-width:760px;margin:36px auto 0;background:#fff;border:1px solid var(--line);border-radius:14px;box-shadow:0 10px 30px rgba(20,50,79,.08);padding:34px 32px;text-align:center;">
  <p class="lead" style="margin-bottom:10px;">Watch the parish prayer progress meter grow</p>
  <p style="margin:0 0 24px;color:var(--muted);max-width:520px;margin-left:auto;margin-right:auto;">Log the minutes you spend in prayer &mdash; Adoration time, daily prayer, family prayer: it all counts &mdash; and watch our parish total climb toward 5,040 hours.</p>
  <a class="btn btn-primary" href="168-progress.html">See the Progress &amp; Log Your Prayer Time</a>
</div>

<div class="prose">
  <h2>How to Join</h2>
  <p>Begin by choosing a seven-day prayer candle &mdash; <strong>$20 each</strong> &mdash; and bring it to the opening gathering for a special blessing:</p>
  <p><strong>Wednesday, December 2, 2026</strong><br>the first Wednesday of Advent &mdash; opening gathering &amp; candle blessing<br>Wednesday evenings at St. Michael's</p>
  <p>Call the parish office at <a href="tel:9038217511">903-821-7511</a> to reserve your candle or ask any questions.</p>
  <p>We also encourage you to purchase a <strong>second candle for someone else</strong> and personally invite them to join you. Donated candles will be available, so cost never prevents anyone from participating. And you can join at any time throughout the year.</p>

  <h2>Watching God Work</h2>
  <p>A candle poster at the parish will show the commitments being made, one flame at a time. As the year goes on, gold flame stickers will be added to a shared display &mdash; a quiet way to recognize answered prayers and blessings without anyone having to share private details.</p>
  <p>It is a visible reminder that God is working through the time we give Him.</p>
  <p>And there is a second way to watch: the <a href="168-progress.html"><strong>Progress &amp; Prayer Log</strong></a> page shows a live parish progress meter &mdash; the combined minutes of prayer logged by parishioners, climbing week by week toward our 5,040-hour goal. Every time you log your own prayer time there, the meter rises for the whole parish to see.</p>

  <h2>Weekly Reflections</h2>
  <p>Each week we post a short Scripture reflection and prayer encouragement &mdash; something to carry with you into your hour of Adoration and your daily prayer. The growing collection lives on its own page: <a href="168-reflections.html">Read the Weekly Reflections</a>.</p>
</div>

<div class="prose">
  <h2>Why, Because I Love You Jesus</h2>
  <p>Why do we pray? Why give an hour, or a half, or whatever we have? Fr. Mike Schmitz puts words to the heart of it &mdash; not a duty to perform, but a love to answer. Take a few minutes with this; it is the "why" behind everything 16:8 is about.</p>
</div>
<div style="max-width:880px;margin:8px auto 0;">
  <div class="video-embed">
    <iframe src="https://www.youtube-nocookie.com/embed/DJpH1kqnJ3Y?rel=0&start=955" title="Why, Because I Love You — Fr. Mike Schmitz" loading="lazy" allowfullscreen allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin"></iframe>
  </div>
  <p class="video-caption">Watch: <strong>Monday Mass, Celebrated by Fr. Mike Schmitz</strong> &mdash; with thanks to <a href="https://www.youtube.com/@SaintPatricksCathedralNYC" target="_blank" rel="noopener">St. Patrick's Cathedral NYC</a> on YouTube.</p>
</div>""")

P("168-progress.html", "16:8 — Progress & Prayer Log",
  "Live parish prayer progress for 16:8 at St. Michael's — watch the progress meter climb and log your own prayer minutes.",
  "16:8", "16:8 Parish Prayer Progress",
  """<div class="prose">
  <p class="lead">Every minute of prayer offered by our parishioners raises the progress meter below &mdash; Adoration time, daily prayer, family prayer: it all counts toward our goal of <strong>5,040 hours</strong> of prayer offered over the year.</p>
  <p>Missed the introduction? <a href="168-introduction.html">Learn about 16:8 and how to join</a>.</p>
</div>

<div class="fund-meter-card">
  <div class="fund-meter-head">
    <span class="fund-meter-title">16:8 Parish Prayer Meter</span>
    <span class="fund-meter-tag">Live Progress</span>
  </div>
  <div class="fund-meter-body thermo">
    <div class="fund-nums">
      <div><span class="fund-cap">Goal</span><span class="fund-big" id="prayer-goal">5,040 hrs</span></div>
      <div><span class="fund-pct" id="prayer-pct">0%</span> <span class="fund-cap">of goal</span><br><span class="fund-big" id="prayer-total">0 hrs</span><span class="fund-cap" id="prayer-people">logged so far</span></div>
      <div><span class="fund-remaining" id="prayer-remaining">5,040 hrs</span><span class="fund-cap">to go</span></div>
    </div>
    <div class="thermo-scale">
      <div class="thermo-track" id="prayer-track" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="0">
        <div class="thermo-fill" id="prayer-fill"></div>
      </div>
      <span class="thermo-mark" style="bottom:25%">25%</span>
      <span class="thermo-mark" style="bottom:50%">50%</span>
      <span class="thermo-mark" style="bottom:75%">75%</span>
    </div>
  </div>
  <div class="fund-meter-foot">
    <p>Live from the parish prayer log &mdash; updated whenever a parishioner logs time.</p>
    <a class="btn btn-primary" href="https://scheduler.stmichaelsallangels.com/?view=prayer" target="_blank" rel="noopener">Log Your Prayer Time</a>
    <p class="fund-updated" id="prayer-updated">Sign in with your Church Hub account &mdash; takes less than a minute.</p>
  </div>
</div>

<script>
(function () {
  fetch('https://scheduler.stmichaelsallangels.com/api/prayer/total')
    .then(function (r) { return r.json(); })
    .then(function (d) {
      var fmt = function (h) { return Number(h).toLocaleString('en-US', { maximumFractionDigits: 1 }); };
      var goal = d.goal_hours || 5040;
      var hours = (d.total_minutes || 0) / 60;
      var pct = goal > 0 ? Math.min(100, Math.round(hours / goal * 100)) : 0;
      document.getElementById('prayer-goal').textContent = fmt(goal) + ' hrs';
      document.getElementById('prayer-total').textContent = fmt(hours) + ' hrs';
      document.getElementById('prayer-pct').textContent = pct + '%';
      document.getElementById('prayer-track').setAttribute('aria-valuenow', pct);
      document.getElementById('prayer-fill').style.height = pct + '%';
      var rem = Math.max(0, goal - hours);
      if (pct >= 100) {
        document.getElementById('prayer-remaining').textContent = 'Goal reached!';
        document.getElementById('prayer-people').textContent = 'thank you!';
      } else {
        document.getElementById('prayer-remaining').textContent = fmt(rem) + ' hrs';
      }
      if (d.participants) {
        document.getElementById('prayer-updated').textContent = d.participants + ' parishioner' + (d.participants === 1 ? '' : 's') + ' logging prayer time.';
      }
    })
    .catch(function () {
      document.getElementById('prayer-remaining').textContent = '&mdash;';
    });
})();
</script>

<div class="cards give-grid" style="max-width:900px;margin:36px auto 0;">
  <div class="give-card">
    <h3>1 &middot; Already Have an Account?</h3>
    <p><strong>You already have a Church Hub account</strong> &mdash; the same login you use to sign up for Mass roles. Just sign in and tap <strong>Prayer Log</strong>. <a href="https://scheduler.stmichaelsallangels.com/?view=prayer" target="_blank" rel="noopener">Sign in &rarr;</a></p>
  </div>
  <div class="give-card">
    <h3>2 &middot; New Account</h3>
    <p>Create a free account with your email. The <strong>16:8 Coordinator</strong> approves new logins &mdash; you will get an email the moment yours is enabled. <a href="https://scheduler.stmichaelsallangels.com/#/register" target="_blank" rel="noopener">Create your account &rarr;</a></p>
  </div>
  <div class="give-card">
    <h3>3 &middot; Log and Grow</h3>
    <p>Enter the minutes you prayed and what you prayed. Every entry lifts the parish progress meter &mdash; and your own running total.</p>
  </div>
</div>

<div class="prose" style="margin-top:36px;">
  <p style="color:var(--muted);font-size:.9rem;">Your individual entries stay private &mdash; the parish sees only the combined total and how many people are praying.</p>
</div>""")

P("168-reflections.html", "16:8 — Weekly Reflections",
  "Weekly Scripture reflections and prayer encouragement for the 16:8 initiative at Saint Michael & All Angels.",
  "16:8", "Weekly Reflections",
  """<div class="prose">
  <p class="lead">Each week we post a short Scripture reflection and prayer encouragement &mdash; something to carry with you into your hour of Adoration and your daily prayer.</p>
  <p>New to 16:8? <a href="168-introduction.html">Learn about the initiative</a> &middot; <a href="168-progress.html">See the parish progress &amp; log your prayer time</a>.</p>
</div>
<div id="reflections-list"></div>
<div class="placeholder" id="reflections-empty" style="display:none;max-width:760px;margin:28px auto;">
  <h3>No reflections posted yet</h3>
  <p>The first reflection will appear here at the start of Advent.</p>
</div>
<script>
(function () {
  var esc = function (s) {
    var d = document.createElement('div');
    d.textContent = s == null ? '' : String(s);
    return d.innerHTML;
  };
  fetch('https://scheduler.stmichaelsallangels.com/api/reflections')
    .then(function (r) { return r.json(); })
    .then(function (rows) {
      var wrap = document.getElementById('reflections-list');
      if (!Array.isArray(rows) || rows.length === 0) {
        document.getElementById('reflections-empty').style.display = 'block';
        return;
      }
      rows.forEach(function (r) {
        var card = document.createElement('div');
        card.className = 'prose reflection-card';
        var head = document.createElement('p');
        head.className = 'lead';
        head.textContent = r.title;
        card.appendChild(head);
        var isFirst = r.id === 1 || /^First Reflection/.test(r.title || '');
        if (isFirst) {
          var wreath = document.createElement('img');
          wreath.src = 'assets/images/advent-wreath.jpg';
          wreath.alt = 'Advent wreath with purple candles and the Christ candle';
          wreath.style.cssText = 'display:block;width:100%;max-width:360px;height:auto;margin:16px auto 12px;border:1px solid var(--line);padding:8px;background:#fff;box-shadow:0 8px 28px rgba(15,24,32,.10);';
          card.appendChild(wreath);
          var verse = document.createElement('p');
          verse.style.cssText = "font-family:'Cormorant Garamond',Georgia,serif;font-style:italic;font-size:1.3rem;color:var(--burgundy);text-align:center;margin:0 0 14px;";
          verse.innerHTML = '&ldquo;I keep the Lord always before me.&rdquo; &mdash; <a href="https://www.biblegateway.com/passage/?search=Psalm%2016%3A8&version=RSVCE" target="_blank" rel="noopener">Psalm 16:8</a>';
          card.appendChild(verse);
        }
        var body = document.createElement('p');
        body.textContent = r.body;
        card.appendChild(body);
        var meta = document.createElement('p');
        meta.style.color = 'var(--muted)';
        meta.style.fontSize = '.85rem';
        var bits = [];
        if (r.week_label) bits.push(r.week_label);
        if (r.created_at) bits.push('Posted ' + new Date(r.created_at).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' }));
        meta.textContent = bits.join(' \u00b7 ');
        card.appendChild(meta);
        wrap.appendChild(card);
      });
    })
    .catch(function () {
      document.getElementById('reflections-empty').style.display = 'block';
    });
})();
</script>""")

P("contact.html", "Contact Us",
  "Contact Saint Michael & All Angels Catholic Church — address, phone, and a contact form.",
  "Resources", "Contact Us",
  """<div class="info-grid" style="margin-bottom: 40px;">
  <div class="info-card">
    <h3>Visit</h3>
    <p>101 E Texas St<br>Denison, TX 75020</p>
    <a class="btn btn-ghost" href="https://maps.google.com/?q=101+E+Texas+St+Denison+TX+75020" target="_blank" rel="noopener">Get Directions</a>
  </div>
  <div class="info-card">
    <h3>Call</h3>
    <p><a href="tel:9038217511">903-821-7511</a><br>Father Randall</p>
    <p style="margin-top:8px;">For sacraments, appointments, and alternate confession times.</p>
  </div>
  <div class="info-card">
    <h3>Connect</h3>
    <p>Join our mailing list for parish news and special Mass schedules.</p>
    <a class="btn btn-ghost" href="flocknote.html">Join Flocknote</a>
  </div>
</div>
<div class="contact-form">
  <form id="contactForm" name="contact" method="POST">
    <label for="c-name">Your Name *</label>
    <input id="c-name" name="name" type="text" required placeholder="Your name">
    <label for="c-email">Email *</label>
    <input id="c-email" name="email" type="email" required placeholder="you@example.com">
    <label for="c-msg">Message *</label>
    <textarea id="c-msg" name="message" rows="6" required placeholder="How can we help?"></textarea>
    <button class="btn btn-primary" type="submit">Send Message</button>
  </form>
  <div id="contactThanks" style="display:none;background:rgba(176,122,42,.12);border:1px solid var(--gold);padding:16px 18px;margin-top:12px;">
    <strong>Thank you!</strong> Please call the parish office at <a href="tel:9038217511">903-821-7511</a> to be sure we received your message, or reach us through <a href="https://www.facebook.com/stmichaelallangel" target="_blank" rel="noopener">Facebook</a>.
  </div>
</div>
<script>
document.getElementById("contactForm").addEventListener("submit", function (e) {
  e.preventDefault();
  this.style.display = "none";
  document.getElementById("contactThanks").style.display = "block";
});
</script>""")

P("ocia.html", "OCIA — Becoming Catholic",
  "The Order of Christian Initiation of Adults — the journey by which adults enter the Catholic Church at Saint Michael & All Angels, Denison TX.",
  "Resources", "OCIA — Becoming Catholic",
  """<div class="prose">
  <p class="lead">"From the time of the apostles, becoming a Christian has been accomplished by a journey and initiation in several stages and regions to which the individual can commit himself for the rest of his life."</p>
  <h2>What OCIA Is</h2>
  <p>The <strong>Order of Christian Initiation of Adults (OCIA)</strong> is the Church's ancient process of formation for adults who wish to become Catholic — a journey of listening, study, prayer, and liturgical rites that unfolds over the course of a year and culminates in receiving the sacraments at the Easter Vigil. (It was known for decades as RCIA, the Rite of Christian Initiation of Adults; the Church renamed it in 2021 with a renewed emphasis on ongoing conversion rather than a class to be passed.)</p>
  <p>At Saint Michael's the experience is personal and unhurried: meetings with the parish coordinator, a sponsor who walks the way with you, study of the faith as it is lived and prayed in our Ordinariate liturgy, and rites celebrated in the presence of the parish, which prays for and supports each inquirer by name.</p>
  <p style="color:var(--muted);font-size:.86rem;"><a href="https://www.vatican.va/archive/ENG0015/__P3J.HTM" target="_blank" rel="noopener">— Catechism of the Catholic Church, 1229</a></p>
  <h2>Who Participates</h2>
  <p>OCIA serves three kinds of seekers, each on a formation track suited to where they begin:</p>
  <ul>
    <li><strong>Adults who have never been baptized</strong> — the full journey of Christian initiation: catechumenate, the rites of Lent, and the sacraments of initiation (Baptism, Confirmation, Eucharist) at the Easter Vigil.</li>
    <li><strong>Christians baptized in another tradition</strong> who are seeking full communion with the Catholic Church — their baptism is already valid and is never repeated; they prepare for Confirmation and the Eucharist.</li>
    <li><strong>Baptized Catholics</strong> who have not yet received Confirmation or First Communion and wish to complete their initiation through adult formation.</li>
  </ul>
  <p>Spouses, fiancés preparing for marriage, and parents of children in the parish are especially welcome — many come because of someone they love, and find God waiting.</p>
  <h2>The Stages of the Journey</h2>
  <p>The Church names the stages of initiation precisely, because each is a real period of growth marked by a rite at the parish altar:</p>
  <ol>
    <li><strong>Period of Inquiry (Precatechumenate)</strong> — the no-obligation beginning. Come ask questions, share your story, and get to know the parish. At its close, those who wish to continue celebrate the <em>Rite of Acceptance into the Order of Catechumens</em> and become catechumens.</li>
    <li><strong>The Catechumenate</strong> — the longest stage, usually running from autumn through Lent. Catechumens study the Creed and the sacraments, hear the Scriptures proclaimed and explained each Sunday (they are dismissed after the Liturgy of the Word for further catechesis), learn Christian prayer, and are accompanied by a sponsor chosen for the journey.</li>
    <li><strong>Purification and Enlightenment (Lent)</strong> — the bishop (or his delegate) celebrates the <em>Rite of Election</em>, the Church "elects" the catechumens for the sacraments, and the Lenten Sundays bring the Scrutinies: prayers for deliverance and strengthening as the elect enter a season of recollection before Easter.</li>
    <li><strong>Initiation at the Easter Vigil</strong> — the elect receive Baptism, Confirmation, and the Holy Eucharist in one unwinding act at the great Vigil of Easter, made members of Christ and of His Church.</li>
    <li><strong>Mystagogy (Easter season into Pentecost)</strong> — the neophytes, newly initiated, reflect on the sacraments received and learn to live them: the whole season is spent "unwrapping the mysteries," joining the full parish life of worship and service.</li>
  </ol>
  <h2>Joining Us</h2>
  <p>Inquiries are welcome at any time of year — you do not need to be sure of anything to begin. Call the parish at <a href="tel:9038217511">903-821-7511</a> or use the <a href="contact.html">contact form</a> and Father Randall or the OCIA coordinator will meet with you. There is never a cost.</p>
</div>""")

# FAQ entries: (question, answer) tuples -> rendered as an exclusive accordion
FAQ_ITEMS = [
  ('Q. What is Saint Michael &amp; All Angels Catholic Church?', 'A. Saint Michael &amp; All Angels is a Roman Catholic <strong>community-in-formation</strong> in Denison, Texas, serving North Texas and southern Oklahoma under the jurisdiction of the <a href="https://ordinariate.net/" target="_blank" rel="noopener">Personal Ordinariate of the Chair of Saint Peter</a>. Unlike most other Catholic churches in the area, we are not under the <a href="https://www.catholicedallas.org/" target="_blank" rel="noopener">Diocese of Dallas</a>; however, we are in full communion with the diocese, and we work in close cooperation with local parishes, serving the Catholic faithful together in a complementary way. The Personal Ordinariate of the Chair of Saint Peter is a canonical jurisdiction within the Catholic Church that covers the United States and Canada. It is one of three similar ordinariates in the English-speaking world, and operates directly under the Pope and the Vatican <a href="https://www.vatican.va/content/romancuria/en/dicasteri/dicastero-dottrina-fede.index.html" target="_blank" rel="noopener">Dicastery for the Doctrine of the Faith</a>. Each ordinariate has many local churches within its canonical jurisdiction &mdash; Saint Michael &amp; All Angels is one of those churches, not yet large enough to be canonically established as a parish.'),
  ('Q. Is Saint Michael &amp; All Angels a Catholic Church?', 'A. YES! Saint Michael &amp; All Angels is a Roman Catholic church, which is part of the <a href="https://ordinariate.net/" target="_blank" rel="noopener">Personal Ordinariate of the Chair of Saint Peter</a>. This Ordinariate operates directly under the Pope of Rome and the Vatican Dicastery for the Doctrine of the Faith (DDF). All members of Saint Michael &amp; All Angels are Roman Catholics. We are in full communion with the <a href="https://www.catholicedallas.org/" target="_blank" rel="noopener">Diocese of Dallas</a> and with the <a href="https://www.usccb.org" target="_blank" rel="noopener">United States Conference of Catholic Bishops</a> (USCCB), and our community is listed with the <a href="https://ordinariate.net/parishfinder" target="_blank" rel="noopener">Ordinariate parish finder</a>. If you have any questions or concerns about this, feel free to contact the Diocese or the USCCB.'),
  ('Q. What is the Ordinariate?', 'A. The Ordinariate is a special canonical jurisdiction (like a super-diocese) within the Roman Catholic Church. The <a href="https://ordinariate.net/" target="_blank" rel="noopener">Personal Ordinariate of the Chair of Saint Peter</a> spans the entire United States and Canada, overlapping regular territorial dioceses but applying only to certain persons and parishes, and is governed by our own bishop in Houston, Texas, who is familiar with our Medieval English Patrimony. This is somewhat like a personal prelature or religious order. Saint Michael &amp; All Angels is established and formed as part of this jurisdiction. If we likened the Ordinariate to a religious order, then think of Saint Michael &amp; All Angels as one community within that order.'),
  ('Q. How large is the Ordinariate?', 'A. There are three ordinariates in total. The first is called the <a href="http://www.ordinariate.org.uk/" target="_blank" rel="noopener">Personal Ordinariate of Our Lady of Walsingham</a>, founded in 2011, with jurisdiction in the United Kingdom. The second is the <a href="https://ordinariate.net/" target="_blank" rel="noopener">Personal Ordinariate of the Chair of Saint Peter</a>, founded in 2012, with jurisdiction in the United States and Canada &mdash; Saint Michael &amp; All Angels is under this ordinariate, which is growing rapidly. The third is the <a href="http://www.ordinariate.org.au/" target="_blank" rel="noopener">Personal Ordinariate of Our Lady of the Southern Cross</a>, founded in 2012, with jurisdiction in Australia and Oceania. To see all the communities in our ordinariate, visit the <a href="https://ordinariate.net/parishfinder" target="_blank" rel="noopener">Ordinariate parish finder</a>.'),
  ('Q. Who may attend Holy Mass at Saint Michael &amp; All Angels?', 'A. Anyone may attend Holy Mass at Saint Michael &amp; All Angels, and all are welcome. One does not need to be a member to attend Mass here. All of our sacraments are valid and legal Roman Catholic sacraments, and our priest is a validly and legally ordained Roman Catholic priest. Any Catholic may receive the sacraments offered by our clergy. Non-Catholics are welcome to attend and pray with us as well, but should not receive communion.'),
  ('Q. What form of liturgy does Saint Michael &amp; All Angels use?', 'A. There is only one Holy Mass in the Catholic Church, but that same Holy Mass can take on different liturgical rites and forms. We use <strong>Divine Worship</strong>, a third form of the Roman Rite, sometimes called the Medieval "English Form" or "English Use" of the Roman Rite. The Roman Rite has three main forms. The first is the <strong>Ordinary Form</strong>, also known as the 1970 Roman Missal &mdash; the usual Mass celebrated in vernacular languages, typically seen in most Catholic churches around the world, including here in North Texas. The second is the <strong>Extraordinary Form</strong>, also known as the 1962 Roman Missal &mdash; the all-Latin form that was the norm until 1970, still celebrated in some churches. The third is <strong>Divine Worship</strong>: a unique liturgy based on sacral English and traditions brought back into the Catholic Church by Anglican converts. It has many similarities to how Catholics worshipped in England during the Middle Ages, before the Protestant Reformation, and is designed to appeal to English-speaking people. You may have noticed that the Our Father is exactly the same at Divine Worship Mass as in the Ordinary Form &mdash; that heritage runs deep.'),
  ('Q. Are the liturgies at Saint Michael &amp; All Angels a separate rite?', 'A. No. This is a very common question. Many people are under the impression that we have our own rite apart from the Roman Rite. This is not the case. Saint Michael &amp; All Angels uses Divine Worship, which is part of the Roman Rite &mdash; a special third form brought back into the Catholic Church by Anglican converts. Its roots reach back to the Medieval English liturgy preserved by Anglicans for centuries; it has now returned to the Catholic Church and is 100% fully Roman Catholic. We believe all the same doctrines that Roman Catholics have always believed, and we keep the same traditions Roman Catholics have always kept. Because we are part of the Roman Rite, we fall under the same <a href="https://www.vatican.va/archive/cod-iuris-canonici/cic_index_en.html" target="_blank" rel="noopener">Code of Canon Law</a>. Our bishop is a member of the <a href="https://www.usccb.org" target="_blank" rel="noopener">U.S. Conference of Catholic Bishops</a>, his cathedral is in Houston, Texas, and he answers directly to the Pope and the Vatican Dicastery for the Doctrine of the Faith (DDF).'),
  ('Q. Who may receive communion at Saint Michael &amp; All Angels?', "A. Any Catholic who is properly disposed and in a state of grace may receive the sacrament of Holy Eucharist at our Divine Worship Mass. We encourage reception of the sacrament of reconciliation (confession) before Mass if there is any doubt or question about a state of grace. Non-Catholics should not receive communion. If you believe there is a special circumstance that would make an exception to this, please discuss it with our priest privately before receiving communion. Those who will not be receiving communion may still approach the altar rail for a blessing. This is done by placing one's hands on opposite shoulders, arms crossed, to signal to the priest that one will be receiving a blessing in place of the Holy Eucharist. The priest will always understand what this means."),
  ('Q. How is communion received at Saint Michael &amp; All Angels?', "A. For those Catholics who are properly disposed and in a state of grace, communion is received on the tongue while kneeling at the altar rail. This will always be the case, unless one has a physical disability that makes this impossible, in which case another accommodation will be made. You kneel at the communion rail, and Father Randall comes to each communicant and administers communion by <strong>intinction</strong> &mdash; the Eucharistic host is dipped into the precious blood by the priest immediately before it is placed on the communicant's tongue. This method of receiving communion puts emphasis on the sacred act itself, drawing attention to what is happening: God Almighty, hidden under the mere appearance of bread and wine, is coming into physical communion with human beings. Many Catholics who have received communion this way often report a heightened sense of reverence and solemnity. It should also be noted that according to Rome, reception of communion on the tongue, while kneeling, is the default way (the normal way) of receiving communion throughout the Catholic Church worldwide. Communion given in the hand, while standing, is a practice that is allowed in the United States only by special permission from Rome, on the condition that communicants may still receive on the tongue while kneeling if they so choose. While many Catholic churches in the United States distribute communion in the hand, we at Saint Michael &amp; All Angels do not; bodily position is accommodated according to medical needs."),
  ('Q. Why do some women at Saint Michael &amp; All Angels wear hats or veils?', 'A. The tradition is Biblical in origin. It comes from St. Paul\'s instruction in <a href="https://www.biblegateway.com/passage/?search=1+Corinthians+11%3A1-16&version=RSVCE" target="_blank" rel="noopener">1 Corinthians 11:1-16</a>, and it has been the tradition of Catholic churches in antiquity &mdash; both East and West. Wearing a veil or hat is not mandatory, but many women do it as a sign of Mary-like humility, especially when in prayer. Some women prefer lace veils or regular shawls; others prefer hats, as is consistent with English custom. Christian head-covering differs from head-covering in other religions: in Christianity, women cover their heads primarily in the presence of God during prayer and worship, usually for no other reason. While head-coverings are not required, we fully support women who choose to keep this Biblical custom. We are a "head-covering friendly" community. We ask only that all head-coverings be modest and not distracting, and that all women be respected in their personal choice on this matter. Some cover, some do not &mdash; both choices are to be respected here. If you have concerns, please bring it up with our priest privately.'),
  ('Q. How should I dress at Saint Michael &amp; All Angels?', 'A. We do not have a strict dress code. Some enjoy putting on their "Sunday best," while others (for various reasons) do not. Your attire does not need to be formal, but overly casual attire is not truly respectful toward the Lord when we are at Mass. It is important to maintain a non-judgmental atmosphere when it comes to clothing. We ask only that, in all things, personal modesty is kept a top priority &mdash; this applies to both men and women. We ask that worshipers cover their full torso, including shoulders, and avoid deep necklines; that legs be covered at least to the knee; and that regular shoes or proper sandals be worn. In all things, come clean, modest, and suitable for worship of Almighty God.'),
  ('Q. Why does the priest turn his back to the people during Mass?', 'A. During the Holy Mass, the priest never "turns his back to the people," but rather he faces the Lord together with the people, leading them into worship. This position is called <em>ad orientem</em>, which in Latin means "facing toward the east." The "east" is not always literal, and the priest does not always face literal east; it comes from Scripture: "For as lightning cometh out of the east, and appeareth even into the west: so shall the coming of the Son of man be" (Matthew 24:27). The Latin term <em>versus Dominum</em> &mdash; "facing the Lord" &mdash; is also used. The idea is that the priest always leads the people into the worship of God. This position is the usual one for Eastern Catholics and had been the normal position for Western Catholics up until the 1970s, when the position of <em>versus populum</em> ("facing the people") was introduced. Many High Church Anglicans preserved the <em>ad orientem</em> tradition, and in keeping with that Medieval English Patrimony, we do the same at Saint Michael &amp; All Angels.'),
  ('Q. Why are some Ordinariate priests married?', 'A. The Catholic Church has always allowed married men to become priests (though not bishops) &mdash; this is especially noticeable in the Eastern Catholic churches. In the West, celibacy became the norm for candidates to the priesthood nearly 900 years ago, which is why most Western Catholic priests are celibate. That said, Rome still allows married men to become Catholic priests in the Western Church in special circumstances, with special permission from the Pope. Some Ordinariate priests are celibate and some are married; the married priests within the Ordinariate were once married Catholic laymen &mdash; usually converts from Anglican ministry &mdash; who were given special permission by the Pope to be ordained as Catholic priests. Ordinariate bishops, however, are always celibate, as is the norm for all bishops throughout the Catholic Church, East and West.'),
  ('Q. Do Catholics in the Ordinariate honor Mary?', 'A. Yes, Catholics in the Ordinariate are regular Catholics. Honor of Mary is part of both our Catholic Faith and our Medieval English Patrimony. To be clear, no Catholic worships Mary &mdash; the worship of Mary is forbidden in the Catholic Church. Rather, Catholics honor Mary and show her great love, even asking for her prayers and intercessions, much like we would ask our friends and family for theirs. Catholics in the Ordinariate are no different. For nearly a thousand years, Mary has been honored under the title of Our Lady of Walsingham, recognized by both Catholics and Anglicans alike. In AD 1061, Our Lady appeared to Richeldis de Faverches, a pious English noblewoman in the village of Walsingham in Norfolk, England; Lady Richeldis built a small structure named "The Holy House," which later became a shrine and place of pilgrimage. In 2015, Pope Francis raised her sanctuary to the status of a minor basilica. Catholics in the Ordinariate are very fond of Marian devotion, and many frequently pray the rosary, wear the brown scapular, and visit approved Marian shrines.'),
  ('Q. Does one need to be a member of the Ordinariate to be part of Saint Michael &amp; All Angels?', 'A. No. Church membership is entirely different from Ordinariate membership. Many Ordinariate communities have "mixed membership," meaning some members are part of the local Diocese while others are part of the Ordinariate &mdash; Saint Michael &amp; All Angels is like this too. Becoming a member of the Ordinariate is not required to be part of our community, though many of our members are also Ordinariate members. Ordinariate membership fully unites Catholics to the Medieval English Patrimony we celebrate here and places one under the canonical jurisdiction of the bishop of the Ordinariate in Houston, Texas. This has some advantages for those who wish to receive other sacraments using our liturgy &mdash; confirmation and matrimony, for example. If you think you might be eligible for Ordinariate membership, or are unsure, simply talk with Father Randall about it privately.'),
  ('Q. How does one become a member of Saint Michael &amp; All Angels?', 'A. If you would like to become a member of our community, speak with Father Randall after Mass or call the parish office at <a href="tel:9038217511">903-821-7511</a>. If you are not yet Catholic and would like to join the Catholic Church through our community, you will want our <a href="ocia.html">OCIA</a> program (the Order of Christian Initiation of Adults, sometimes called RCIA) &mdash; a journey of formation and rites that culminates in receiving the sacraments at the Easter Vigil. You can learn all about it on our <a href="ocia.html">OCIA page</a>, and inquiries are welcome at any time of year.'),
]
faq_body = """<div class="prose">
  <p class="lead">The questions we hear most often &mdash; about who we are, our liturgy, and how to join us &mdash; answered plainly. Tap a question to read the answer; only one is open at a time.</p>
</div>
<div class="faq-list">
"""
for _q, _a in FAQ_ITEMS:
    faq_body += f'<details class="faq-item" name="faq"><summary>{_q}</summary><div class="faq-a"><p>{_a}</p></div></details>'
    faq_body += '\n'
faq_body += """<p style="color:var(--muted);font-size:.86rem;margin-top:14px;">More questions? Call the office at <a href="tel:9038217511">903-821-7511</a> or use the <a href="contact.html">contact form</a>.</p></div>
<script>
(function () {
  var probe = document.createElement("details");
  if ("name" in probe) return; /* native exclusive accordion */
  var items = document.querySelectorAll('details[name="faq"]');
  items.forEach(function (det) {
    det.addEventListener("toggle", function () {
      if (!det.open) return;
      items.forEach(function (other) { if (other !== det) other.open = false; });
    });
  });
})();
</script>"""

P("faq.html", "Frequently Asked Questions",
  "Frequently asked questions about Saint Michael & All Angels Catholic Church — a Roman Catholic community-in-formation (Ordinariate) in Denison, Texas.",
  "About Us", "Frequently Asked Questions",
  faq_body)


# ================================================================ EXAMINATION OF CONSCIENCE
# Three pages built from the parish's "A Detailed Catholic Examination of
# Conscience" (2nd ed.) document, rendered in the site's exclusive-accordion style.
EXAM_CMD_ITEMS = [
  ("First Commandment &mdash; &ldquo;I am the LORD your God. You shall worship the Lord your God and Him only shall you serve.&rdquo;",
   """<p>Have I&hellip;</p><ul>
   <li>Reserved or harbored hatred for God?</li>
   <li>Disobeyed the commandments of God or the Church?</li>
   <li>Refused to accept what God has revealed as true, or what the Catholic Church proclaims for belief?</li>
   <li>Denied the existence of God?</li>
   <li>Neglected to nourish and protect my faith?</li>
   <li>Neglected to reject everything opposed to a sound faith?</li>
   <li>Deliberately misled others about doctrine or the faith?</li>
   <li>Rejected the Catholic faith, joined another Christian denomination, or joined or practiced another religion?</li>
   <li>Joined a group forbidden to Catholics (Masons, communists, etc.)?</li>
   <li>Despaired about my salvation or the forgiveness of my sins?</li>
   <li>Presumed God&rsquo;s mercy? (Committing a sin in expectation of forgiveness, or asking for forgiveness without interior conversion and practicing virtue.)</li>
   <li>Loved someone or something more than God (money, power, sex, ambition, etc.)?</li>
   <li>Let someone or something influence my choices more than God?</li>
   <li>Engaged in superstitious practices? (Including horoscopes, fortune tellers, etc.)</li>
   <li>Been involved in the occult or occult practices? (S&eacute;ances, Ouija board, worship of Satan, etc.)</li>
   <li>Formally attempted to leave the Catholic Church?</li>
   <li>Hidden a serious sin or told a lie in Confession?</li></ul>"""),
  ("Second Commandment &mdash; &ldquo;You shall not take the name of the Lord your God in vain.&rdquo;",
   """<p>Have I&hellip;</p><ul>
   <li>Used the name of God in cursing or blasphemy?</li>
   <li>Failed to keep vows, promises, or resolutions that I have made to God? <em>(Specify in the confessional which one; the Priest has authority to remove the obligations of promises and resolutions if they are too rash or unjust.)</em></li>
   <li>Spoken about the Faith, the Church, the saints, or sacred things with irreverence, hatred or defiance?</li>
   <li>Watched television or movies, or listened to music that treated God, the Church, the saints, or sacred things irreverently?</li>
   <li>Used vulgar, suggestive or obscene speech?</li>
   <li>Belittled others in my speech?</li>
   <li>Behaved disrespectfully in the church building (e.g., talking immoderately in church before, during, or after holy Mass)?</li>
   <li>Misused places or things set apart for the worship of God?</li>
   <li>Committed perjury? (Breaking an oath or lying under oath.)</li>
   <li>Blamed God for my failings?</li></ul>"""),
  ("Third Commandment &mdash; &ldquo;Remember to keep holy the Sabbath day.&rdquo;",
   """<p>Have I&hellip;</p><ul>
   <li>Missed Mass on Sunday or Holy Days (through my own fault, without sufficient reason)?</li>
   <li>Neglected to set time aside each day for personal prayer to God?</li>
   <li>Committed a sacrilege against the Blessed Sacrament (thrown Him away; brought Him home; treated Him carelessly, etc.)?</li>
   <li>Received any sacrament while in the state of mortal sin?</li>
   <li>Habitually come late to and/or leave early from Mass?</li>
   <li>Shopped, labored, practiced sports or done business unnecessarily on Sunday or other Holy Days of Obligation?</li>
   <li>Failed to attend to taking my children to Mass?</li>
   <li>Failed to provide proper instruction in the Faith to my children?</li>
   <li>Knowingly eaten meat on a forbidden day (or not fasted on a fast day)?</li>
   <li>Eaten or drunk within one hour of receiving Communion (other than medical need)?</li></ul>"""),
  ("Fourth Commandment &mdash; &ldquo;Honor your father and your mother.&rdquo;",
   """<p>Have I&hellip;</p><ul>
   <li>(If still under my parents&rsquo; care) Obeyed all that my parents reasonably asked of me?</li>
   <li>Shown disregard for my parents&rsquo; wishes, displayed contempt of their demands, and/or disdained their very being?</li>
   <li>Neglected the needs of my parents in their old age or in their time of need?</li>
   <li>Harbored hatred for my parents?</li>
   <li>Brought shame on them?</li>
   <li>(If still in school) Obeyed the reasonable demands of my teachers?</li>
   <li>Disrespected my teachers?</li>
   <li>(If I have children) Neglected to give my children proper food, clothing, shelter, education, discipline and care (even after Confirmation)?</li>
   <li>Provided for the religious education and formation of my children for as long as they are under my care?</li>
   <li>Ensured that my children still under my care regularly frequent the sacraments of Penance and Holy Communion?</li>
   <li>Educated my children in a way that corresponds to Catholic religious disciplines?</li>
   <li>Provided my children with a positive, prudent and personalized education in the Catholic teaching on human sexuality?</li>
   <li>Been to my children a good example of how to live the Catholic Faith?</li>
   <li>Prayed with and for my children?</li>
   <li>(For everyone) Lived in humble obedience to those who legitimately exercise authority over me?</li>
   <li>Broken any just law?</li>
   <li>Supported or voted for a politician whose positions are opposed to the teachings of Christ and the Catholic Church?</li>
   <li>Failed to pray for the deceased members of my family &mdash; the Poor Souls of Purgatory included?</li></ul>"""),
  ("Fifth Commandment &mdash; &ldquo;You shall not murder.&rdquo;",
   """<p>Have I&hellip;</p><ul>
   <li>Unjustly and intentionally killed a human being (murder)?</li>
   <li>Been guilty, through negligence and/or lack of intention, of the death of another?</li>
   <li>Been involved in an abortion, directly or indirectly (through advice, encouragement, providing money, or facilitating it in any other way)?</li>
   <li>Seriously considered or attempted suicide?</li>
   <li>Supported, promoted, or encouraged the practice of assisted suicide or mercy killing (euthanasia)?</li>
   <li>Deliberately desired to kill an innocent human being?</li>
   <li>Unjustly inflicted bodily harm on another person?</li>
   <li>Unjustly threatened another person with bodily harm?</li>
   <li>Verbally or emotionally abused another person?</li>
   <li>Gossiped, slandered, detracted, calumniated?</li>
   <li>Hated another person, or wished him or her evil?</li>
   <li>Been prejudiced, or unjustly discriminated against others because of their race, color, nationality, sex or religion?</li>
   <li>Joined a hate group?</li>
   <li>Purposely provoked another by teasing or nagging?</li>
   <li>Recklessly endangered my life or health, or that of another, by my actions?</li>
   <li>Driven recklessly or under the influence of alcohol or other drugs?</li>
   <li>Abused alcohol or other drugs?</li>
   <li>Sold or given drugs to others to use for non-therapeutic purposes?</li>
   <li>Used tobacco immoderately?</li>
   <li>Over-eaten?</li>
   <li>Encouraged others to sin by giving scandal?</li>
   <li>Helped another to commit a mortal sin (through advice, driving them somewhere, dressing and/or acting immodestly, etc.)?</li>
   <li>Caused serious injury of another by criminal neglect?</li>
   <li>Indulged in unjust anger?</li>
   <li>Refused to control my temper?</li>
   <li>Been fateful to, quarreled with, or willfully hurt someone?</li>
   <li>Been unforgiving of others, especially when mercy or pardon was requested?</li>
   <li>Sought revenge or hoped something bad would happen to someone?</li>
   <li>Delighted to see someone else get hurt or suffer?</li>
   <li>Treated animals cruelly, causing them to suffer or die needlessly?</li></ul>"""),
  ("Sixth &amp; Ninth Commandments &mdash; &ldquo;You shall not commit adultery. You shall not covet your neighbor&rsquo;s wife.&rdquo;",
   """<p>Have I&hellip;</p><ul>
   <li>Neglected to practice and grow in the virtue of chastity?</li>
   <li>Given in to lust? (The desire for sexual pleasure unrelated to spousal love in marriage.)</li>
   <li>Used an artificial means of birth control (including withdrawal)?</li>
   <li>Refused to be open to conception, without just cause? (Catechism, 2368)</li>
   <li>Participated in immoral techniques such as in vitro fertilization or artificial insemination?</li>
   <li>Sterilized my sex organs for contraceptive purposes?</li>
   <li>Deprived my spouse of the marital right, without just cause?</li>
   <li>Claimed my own marital right without concern for my spouse?</li>
   <li>Deliberately caused male climax outside of normal sexual intercourse?</li>
   <li>Masturbated? (Deliberate stimulation of one&rsquo;s own sexual organs for sexual pleasure outside of the conjugal act.) (Catechism, 2366)</li>
   <li>Willfully entertained impure thoughts?</li>
   <li>Purchased, viewed, or made use of pornography?</li>
   <li>Watched or promoted movies and television that involve sex and nudity?</li>
   <li>Listened to music or jokes that are harmful to purity? Read books that are immoral?</li>
   <li>Committed adultery? (Sexual relations with someone who is married, or with someone other than my spouse.)</li>
   <li>Committed incest? (Sexual relations with a relative closer than the third degree or an in-law.)</li>
   <li>Committed fornication? (Sexual relations with someone of the opposite sex when the two are not married to one another or any others.)</li>
   <li>Engaged in homosexual activity?</li>
   <li>Committed rape?</li>
   <li>Engaged in sexual foreplay (e.g., &ldquo;petting&rdquo;, or excessive touching) reserved for marriage?</li>
   <li>Preyed upon children or youth for my sexual pleasure?</li>
   <li>Engaged in unnatural sexual activities?</li>
   <li>Engaged in prostitution, or paid for the services of a prostitute?</li>
   <li>Seduced someone, or allowed myself to be seduced?</li>
   <li>Made uninvited and unwelcome sexual advances toward another?</li>
   <li>Purposely dressed immodestly?</li></ul>"""),
  ("Seventh &amp; Tenth Commandments &mdash; &ldquo;You shall not steal. You shall not covet your neighbor&rsquo;s goods.&rdquo;",
   """<p>Have I&hellip;</p><ul>
   <li>Stolen? (Taken something that doesn&rsquo;t belong to me against the reasonable will of the owner.)</li>
   <li>Envied others on account of their possessions?</li>
   <li>Neglected to live in a spirit of Gospel poverty and simplicity?</li>
   <li>Neglected to give generously to others in need?</li>
   <li>Failed to consider that God has provided me with money so that I might use it to benefit others, as well as for my own legitimate needs?</li>
   <li>Allowed myself to be conformed to a consumer mentality (buy, buy, buy; throw away, waste; spend, spend, spend)?</li>
   <li>Neglected to practice the corporal works of mercy?</li>
   <li>Deliberately defaced, destroyed or lost another&rsquo;s property?</li>
   <li>Cheated on a test, taxes, sports, games, or in business?</li>
   <li>Squandered money in compulsive gambling?</li>
   <li>Made a false claim to an insurance company?</li>
   <li>Failed to pay my employees a just wage, or failed to give a full day&rsquo;s work for a full day&rsquo;s pay?</li>
   <li>Failed to honor my part of a contract?</li>
   <li>Failed to make good on a debt?</li>
   <li>Overcharged someone, especially to take advantage of another&rsquo;s hardship or ignorance?</li>
   <li>Misused natural resources?</li></ul>"""),
  ("Eighth Commandment &mdash; &ldquo;You shall not bear false witness against your neighbor.&rdquo;",
   """<p>Have I&hellip;</p><ul>
   <li>Lied?</li>
   <li>Knowingly and willfully deceived another?</li>
   <li>Perjured myself under oath?</li>
   <li>Gossiped?</li>
   <li>Committed detraction? (Destroying a person&rsquo;s reputation by telling others about his faults for no good reason.)</li>
   <li>Committed slander or calumny? (Telling lies about another person in order to destroy his reputation.)</li>
   <li>Committed libel? (Writing lies about another person in order to destroy his reputation &mdash; the written word has a longer &ldquo;life&rdquo; of damage.)</li>
   <li>Been guilty of rash judgment? (Assuming the worst of another person based on circumstantial evidence.)</li>
   <li>Failed to make reparation for a lie I told, or for harm done to a person&rsquo;s reputation?</li>
   <li>Failed to speak out in defense of the Catholic Faith, the Church, or of another person?</li>
   <li>Betrayed another&rsquo;s confidence through speech, deed, or in writing?</li></ul>"""),
]

exam_body = """<div class="prose">
  <p class="lead">A good examination of conscience helps us call to mind our sins and failings during a period of quiet reflection before approaching the Priest in Confession. Set aside some quiet time, begin with a prayer to the Holy Spirit, and work honestly through each of the Ten Commandments below. Tap a Commandment to open its questions.</p>
  <p><strong>When is a sin mortal?</strong> A mortal sin is committed when three conditions are met: <strong>(1) grave matter</strong> &mdash; the act is contrary to God&rsquo;s will under the Ten Commandments and the Precepts of the Church; <strong>(2) full knowledge</strong> that the act was sinful; and <strong>(3) full consent</strong> &mdash; it was committed with intentionality, not forced. If any of these three conditions is not met, the sin is venial. It is still a very good idea to confess venial sins, since all sin offends God, Who deserves all of our love.</p>
</div>
<div class="faq-list">
"""
for _q, _a in EXAM_CMD_ITEMS:
    exam_body += f'<details class="faq-item" name="exam"><summary>{_q}</summary><div class="faq-a">{_a}</div></details>'
    exam_body += '\n'
exam_body += """<p style="color:var(--muted);font-size:.86rem;margin-top:14px;">After the Ten Commandments, continue with the <a href="precepts-of-the-church.html">Precepts of the Church</a>, then see <a href="how-to-go-to-confession.html">How to Go to Confession</a>.</p></div>
<script>
(function () {
  var probe = document.createElement("details");
  if ("name" in probe) return; /* native exclusive accordion */
  var items = document.querySelectorAll('details[name="exam"]');
  items.forEach(function (det) {
    det.addEventListener("toggle", function () {
      if (!det.open) return;
      items.forEach(function (other) { if (other !== det) other.open = false; });
    });
  });
})();
</script>"""

P("examination-of-conscience.html", "Examination of Conscience",
  "A detailed Catholic examination of conscience through the Ten Commandments — preparation for the Sacrament of Confession at Saint Michael & All Angels.",
  "Confession", "Examination of Conscience",
  exam_body)

# --- Precepts of the Church page -------------------------------------------
PRECEPT_ITEMS = [
  ("First Precept of the Church &mdash; &ldquo;You shall attend Mass on Sundays and Holy Days of Obligation and rest from servile labor.&rdquo;",
   "<p>(See the Third Commandment in the <a href=\"examination-of-conscience.html\">Examination of Conscience</a>.)</p>"),
  ("Second Precept of the Church &mdash; &ldquo;You shall confess your sins to a Priest at least once a year.&rdquo;",
   """<p>Have I&hellip;</p><ul>
   <li>Made a good Confession of my mortal sins at least once a year?</li>
   <li>Purposely omitted telling my mortal sins in my last Confession?</li>
   <li>Neglected to perform the penance I was given?</li>
   <li>Neglected to make reparation for any harm I have done to others?</li></ul>"""),
  ("Third Precept of the Church &mdash; &ldquo;You shall humbly receive your Creator in Holy Communion at least once during the Easter season.&rdquo;",
   """<p>Have I&hellip;</p><ul>
   <li>Neglected to fulfill my Easter duty to receive Holy Communion at least once between the First Sunday of Lent and Trinity Sunday?</li>
   <li>Received Holy Communion while in the state of mortal sin?</li>
   <li>Failed to fast for at least one hour before receiving Holy Communion?</li>
   <li>Received Holy Communion more than twice in one day?</li></ul>"""),
  ("Fourth Precept of the Church &mdash; &ldquo;You shall observe the prescribed days of fasting and abstinence established by the Church.&rdquo;",
   """<p>Have I&hellip;</p><ul>
   <li>Neglected to do penance every Friday of the year, if not abstaining from meat?</li>
   <li>Neglected to abstain from meat on Ash Wednesday and the Fridays of Lent (if I am 14 years of age or older)?</li>
   <li>Neglected to fast on Ash Wednesday and Good Friday (if I am between the ages of 18 and 59)?</li>
   <li>Participated in diversions on days of penance (e.g., attended crawfish boils and fish fries, ballgames, movies, shopping on Ash Wednesday &amp; Good Friday)?</li>
   <li>Neglected to spend time in prayer, do spiritual and corporal works of mercy, and practice self-denial?</li></ul>"""),
  ("Fifth Precept of the Church &mdash; &ldquo;You shall contribute to the support of the Church.&rdquo;",
   """<p>Have I&hellip;</p><ul>
   <li>Neglected to contribute a just amount of my time, talents and money to support my parish and the work of the Church?</li>
   <li>Neglected to support the Church by not trying to become a saint or by not striving to make sincere progress each day in sanctity?</li></ul>"""),
  ("An Additional Precept of the Church &mdash; &ldquo;You shall observe the laws of the Church concerning marriage.&rdquo;",
   """<p>Have I&hellip;</p><ul>
   <li>Been living in an invalid and/or illicit marriage according to the laws of the Catholic Church?</li>
   <li>Abandoned my spouse and/or family by separation or divorce?</li>
   <li>Kept company with someone whom I cannot marry in the Catholic Church?</li>
   <li>Given scandal by living with a member of the opposite sex without the benefit of a marriage blessed by the Catholic Church?</li>
   <li>Entered into marriage with more than one person at the same time?</li>
   <li>Failed to embrace the teachings given by the Catholic Church, which are supported by the Natural Law: that marriage can only exist between one man and one woman, and that no other union can be a valid natural and/or sacramental marriage?</li>
   <li>Supported pro same-sex union politicians?</li>
   <li>Publicly proclaimed that the Church&rsquo;s teaching on marriage is wrong and, as such, taught others to reject it?</li></ul>
   <p style="color:var(--muted);font-size:.86rem;"><em>The Catechism of the Catholic Church officially lists five Precepts. This additional precept is counted among those teachings so fundamental to Catholicism that they must be observed in order to consider oneself a faithful and practicing Catholic.</em></p>"""),
]

precepts_body = """<div class="prose">
  <p class="lead">The Precepts of the Church are the minimum obligations required of every Catholic in matters of worship, penance, and support of the Church. Work through each one honestly as part of your examination of conscience. Tap a Precept to open its questions.</p>
</div>
<div class="faq-list">
"""
for _q, _a in PRECEPT_ITEMS:
    precepts_body += f'<details class="faq-item" name="precepts"><summary>{_q}</summary><div class="faq-a">{_a}</div></details>'
    precepts_body += '\n'
precepts_body += """<p style="color:var(--muted);font-size:.86rem;margin-top:14px;">Begin with the <a href="examination-of-conscience.html">Ten Commandments</a>, then see <a href="how-to-go-to-confession.html">How to Go to Confession</a>.</p></div>
<script>
(function () {
  var probe = document.createElement("details");
  if ("name" in probe) return; /* native exclusive accordion */
  var items = document.querySelectorAll('details[name="precepts"]');
  items.forEach(function (det) {
    det.addEventListener("toggle", function () {
      if (!det.open) return;
      items.forEach(function (other) { if (other !== det) other.open = false; });
    });
  });
})();
</script>"""

P("precepts-of-the-church.html", "Precepts of the Church",
  "The Precepts of the Church — the minimum obligations of every Catholic — as an examination of conscience for Confession at Saint Michael & All Angels.",
  "Confession", "Precepts of the Church",
  precepts_body)

# --- How to Go to Confession page -------------------------------------------
QUOTES_ITEMS = [
  ("The Bible on Confession",
   """<ul>
   <li>&ldquo;I give you the keys to the kingdom of heaven, and whatever you bind on earth shall be bound in heaven and whatever you loose on earth shall be loosed in heaven&rdquo; (Matthew 16:19).</li>
   <li>&ldquo;Truly I say to you, whatever you bind on earth shall be bound in heaven, and whatever you loose on earth shall be loosed in heaven&rdquo; (Matthew 18:18).</li>
   <li>&ldquo;Receive the Holy Spirit. If you forgive the sins of any, they are forgiven; if you retain the sins of any, they are retained&rdquo; (John 20:22-23).</li>
   <li>&ldquo;Go, show yourself to the Priest&rdquo; (Luke 5:14; 17:14; Matthew 8:4).</li>
   <li>&ldquo;If you love Me, you will keep My commandments&rdquo; (John 14:15).</li>
   <li>&ldquo;He who believes in the Son has eternal life; but he who does not obey the Son will not see life, but the wrath of God abides on him&rdquo; (John 3:36).</li></ul>"""),
  ("The Catechism of the Catholic Church on Confession",
   """<ul>
   <li>&ldquo;You shall confess your sins (to a Priest) at least once a year&rdquo; (2042).</li>
   <li>&ldquo;Christ instituted the sacrament of Penance for all sinful members of His Church: above all for those who, since Baptism, have fallen into grave sin, and have thus lost their baptismal grace and wounded ecclesial communion. It is to them that the sacrament of Penance offers a new possibility to convert and to recover the grace of justification. The Fathers of the Church present this sacrament as <strong>&lsquo;the second plank [of salvation] after the shipwreck which is the loss of grace&rsquo;</strong>&rdquo; (1446).</li>
   <li>&ldquo;All mortal sins of which penitents after a diligent self-examination are conscious must be recounted by them in confession, even if they are most secret and have been committed against the last two precepts of the Decalogue; for these sins sometimes wound the soul more grievously and are more dangerous than those which are committed openly&rdquo; (1456; Council of Trent, DS 1680).</li></ul>"""),
  ("The Saints on Confession",
   """<ul>
   <li>&ldquo;Confession is an act of honesty and courage &mdash; an act of entrusting ourselves, beyond sin, to the mercy of a loving and forgiving God&rdquo; (Pope St. John Paul II).</li>
   <li>&ldquo;The confession of evil works is the first beginning of good works&rdquo; (St. Augustine).</li>
   <li>&ldquo;Go to your confessor; open your heart to him; display to him all the recesses of your soul; take the advice that he will give you with the utmost humility and simplicity. For God, Who has an infinite love for obedience, frequently renders profitable the counsels we take from others, but especially from those who are the guides of our souls&rdquo; (St. Francis de Sales).</li>
   <li>&ldquo;In failing to confess, Lord, I would only hide You from myself, not myself from You&rdquo; (St. Augustine).</li>
   <li>&ldquo;Confession is like a bridle that keeps the soul which reflects on it from committing sin, but anything left unconfessed we continue to do without fear as if in the dark&rdquo; (St. John Climacus).</li>
   <li>&ldquo;A soul does not benefit from the sacrament of confession if it is not humble. Pride keeps it in darkness. The soul neither knows how, nor is it willing, to probe with precision the depths of its own misery. It puts on a mask and avoids everything that might bring it recovery&rdquo; (St. Faustina).</li>
   <li>&ldquo;At the time of your examination (of sins) beware of the devil that ties your tongue&rdquo; (St. Josemaria Escriva).</li>
   <li>&ldquo;The devil does not bring sinners to hell with their eyes open: he first blinds them with the malice of their own sins. Before we fall into sin, the enemy labors to blind us, that we may not see the evil we do and the ruin we bring upon ourselves by offending God. After we commit sin, he seeks to make us dumb [i.e., silent], that, through shame, we may conceal our guilt in confession&rdquo; (St. Alphonsus Liguori).</li>
   <li>&ldquo;The want of proper examination, true contrition, and a firm purpose of amendment, is the cause of bad confessions, and of the ruin of souls&rdquo; (St. Benedict Joseph Labre).</li>
   <li>&ldquo;Obedience to a confessor is the most acceptable offering which we can make to God, and the most secure way of doing the divine will&rdquo; (St. Alphonsus Liguori).</li></ul>"""),
  ("Pope Francis on Confession",
   """<ul>
   <li>&ldquo;Someone can say, &lsquo;I confess my sins only to God.&rsquo; Yes, you can say to God, &lsquo;forgive me,&rsquo; and say your sins. But our sins are also against our brothers, against the Church. This is why it is necessary to ask forgiveness of the Church and of our brothers, in the person of the Priest &hellip; Forgiveness is not something we can give ourselves.&rdquo;</li>
   <li>&ldquo;Father, I am embarrassed! Even embarrassment is good. It&rsquo;s healthy to have a bit of shame &hellip; it does us good, because it makes us more humble. Don&rsquo;t be afraid of confession &hellip; When someone is in line for confession he feels all these things &mdash; even shame &mdash; but then, when he finishes confessing, he leaves free, great, beautiful, forgiven, clean, happy. The sacrament of reconciliation is a sacrament of healing.&rdquo;</li>
   <li>&ldquo;Be courageous, and go to confession.&rdquo;</li></ul>"""),
]

howto_body = """<div class="prose">
  <p class="lead">Forgotten how to go to confession, or never learned? Here is the &ldquo;How To&rdquo; for the Sacrament of Penance. Confession is offered <strong>Saturdays from 10:00 &ndash; 11:00 am</strong> at the parish, or by appointment with <a href="tel:9038217511">Father Randall</a>.</p>
  <p><span style="color:var(--muted);font-size:.9rem;"><strong>Penitent</strong> &mdash; the person confessing his sins. &nbsp;<strong>Confessor</strong> &mdash; the Priest administering the Sacrament.</span></p>
</div>
<div class="faq-list">"""
HOWTO_STEPS = [
  ("1. Enter the confessional",
   "<p>The Penitent enters the confessional and kneels down at the screen.</p>"),
  ("2. Begin with the Sign of the Cross",
   "<p>The Penitent, making the sign of the cross, says: <em>&ldquo;Bless me, Father, for I have sinned. It has been ________ (state amount of time) since my last confession. These are my sins.&rdquo;</em></p>"),
  ("3. Confess your sins",
   "<p>The Penitent confesses his sins. The Confessor listens, but he may ask questions if something is unclear or in order to lead the Penitent to a more thorough examination of conscience. All mortal sins &mdash; each kind and the number of times committed &mdash; must be confessed. All venial sins should be confessed.</p>"),
  ("4. Finish your confession",
   "<p>When the Penitent finishes confessing, he signifies this by saying: <em>&ldquo;For these and all my sins, I ask forgiveness of God and absolution from you, Father.&rdquo;</em> The Confessor may offer some advice or counsel, so that the Penitent may take the necessary steps to amend his life.</p>"),
  ("5. Receive your penance",
   "<p>The Confessor gives a penance (usually a prayer or a good work) and then instructs the Penitent to make an Act of Contrition. There are different formulas; an Act of Contrition is usually printed in the confessional.</p>"),
  ("6. Pray the Act of Contrition",
   "<p>After the Penitent has made an Act of Contrition, the Confessor imparts absolution with the sacramental formula. The Penitent makes the Sign of the Cross at the absolution.</p>"),
  ("7. Go in peace",
   "<p>The Confessor concludes with these or similar words: <em>&ldquo;Your sins are forgiven. Go in peace.&rdquo;</em> The Penitent responds: <em>&ldquo;Thanks be to God.&rdquo;</em></p>"),
  ("8. Fulfill your penance",
   "<p>The Penitent leaves the confessional and fulfills the penance as soon as possible.</p>"),
]
for _t, _b in HOWTO_STEPS:
    howto_body += f'<details class="faq-item" name="howto"><summary><strong>{_t}</strong></summary><div class="faq-a">{_b}</div></details>'
    howto_body += '\n'
howto_body += "</div>\n"

contrition_block = """<div class="prose">
  <h2>The Act of Contrition</h2>
  <p style="margin-bottom:6px;"><em>O my God, I am heartily sorry for having offended Thee. And I detest all my sins because I dread the loss of heaven and the pains of hell but, most of all, because they offend Thee, my God, Who art all good and deserving of all my love. And I firmly resolve with the help of Thy grace to confess my sins, to do penance and to amend my life. Amen.</em></p>
  <p style="margin-bottom:6px;"><em>Or:</em></p>
  <p><em>O my God, I am heartily sorry for having offended Thee, and I detest all my sins because of Thy just punishments, but most of all because they offend Thee, my God, Who art all good and deserving of all my love. And I firmly resolve, with the help of Thy grace, to sin no more and to avoid the near occasions of sin. Amen.</em></p>
</div>
<div class="faq-list">"""
for _q, _a in QUOTES_ITEMS:
    contrition_block += f'<details class="faq-item" name="quotes"><summary>{_q}</summary><div class="faq-a">{_a}</div></details>'
    contrition_block += '\n'
contrition_block += """</div>
<p style="color:var(--muted);font-size:.86rem;margin-top:14px;">Prepare with the <a href="examination-of-conscience.html">Examination of Conscience &mdash; Ten Commandments</a> and the <a href="precepts-of-the-church.html">Precepts of the Church</a>.</p>
<script>
(function () {
  var probe = document.createElement("details");
  if ("name" in probe) return; /* native exclusive accordion */
  var items = document.querySelectorAll('details[name="howto"], details[name="quotes"]');
  items.forEach(function (det) {
    det.addEventListener("toggle", function () {
      if (!det.open) return;
      items.forEach(function (other) { if (other !== det && other.name === det.name) other.open = false; });
    });
  });
})();
</script>"""

P("how-to-go-to-confession.html", "How to Go to Confession",
  "A step-by-step guide to the Sacrament of Penance with the Act of Contrition — Scripture, Catechism, and the Saints on Confession. Saint Michael & All Angels, Denison, Texas.",
  "Confession", "How to Go to Confession",
  howto_body + contrition_block)

# Order of the Mass — the Divine Worship form of the Roman Rite, rendered as an
# exclusive accordion built on the same styles as the FAQ page.
MASS_SECTIONS = [
  ("The Introductory Rites", """<p class="lit"><span class="role">Priest:</span> In the Name of the Father &hellip; and of the Holy Spirit</p>
<p class="lit"><span class="role">People:</span> <span class="resp">Amen.</span></p>
<p class="lit rubric">The Priest offers the Collect for Purity and may add the Summary of the Law.</p>
<p class="lit rubric">Then is sung or said, the People responding after the Priest:</p>
<p class="lit"><span class="role">Kyrie eleison.</span> Lord, have mercy upon us.</p>
<p class="lit"><span class="role">Christe eleison.</span> <em>or</em> Christ, have mercy upon us.</p>
<p class="lit"><span class="role">Kyrie eleison.</span> Lord, have mercy upon us.</p>
<p class="lit rubric">On Sundays and Holy Days appointed, the following is sung or said:</p>
<div class="lit-prayers">
<p>Glory be to God on high, and on earth peace, good will towards men.</p>
<p>We praise thee, we bless thee, we worship thee, we glorify thee, we give thanks to thee for thy great glory, O Lord God, heavenly King, God the Father Almighty.</p>
<p>O Lord, the only begotten Son, Jesus Christ; O Lord God, Lamb of God, Son of the Father, that takest away the sins of the world, have mercy upon us.</p>
<p>Thou that takest away the sins of the world, receive our prayer.</p>
<p>Thou that sittest at the right hand of God the Father, have mercy upon us.</p>
<p>For thou only art holy; thou only art the Lord; thou only, O Christ, with the Holy Ghost, ✠ art the Most High in the glory of God the Father. Amen.</p>
</div>
<p class="lit"><span class="role">Priest:</span> The Lord be with you.</p>
<p class="lit"><span class="role">People:</span> <span class="resp">And with thy spirit.</span></p>
<p class="lit"><span class="role">Priest:</span> Let us pray.</p>
<p class="lit rubric">The Priest says the Collect of the Day.</p>"""),
  ("The Liturgy of the Word", """<p class="lit rubric">At the end of each reading the People respond:</p>
<p class="lit"><span class="role">People:</span> <span class="resp">Thanks be to God.</span></p>
<p class="lit"><span class="role">Deacon or Priest:</span> The Lord be with you.</p>
<p class="lit"><span class="role">People:</span> <span class="resp">And with thy spirit.</span></p>
<p class="lit"><span class="role">Deacon or Priest:</span> A reading from the Holy Gospel according to &hellip;</p>
<p class="lit"><span class="role">People:</span> <span class="resp">Glory be to thee, O Lord.</span></p>
<p class="lit rubric">After the Gospel reading:</p>
<p class="lit"><span class="role">Deacon or Priest:</span> The Gospel of the Lord.</p>
<p class="lit"><span class="role">People:</span> <span class="resp">Praise be to thee, O Christ.</span></p>
<p class="lit rubric">After the Homily, on Sundays and Holy Days, the following is sung or said, all standing:</p>
<div class="lit-prayers">
<p>I believe in one God, the Father Almighty, maker of heaven and earth, and of all things visible and invisible;</p>
<p>And in one Lord Jesus Christ, the only-begotten Son of God, begotten of his Father before all worlds, God of God, Light of Light, very God of very God, begotten, not made, being of one substance with the Father; by whom all things were made;</p>
<p>who for us men and for our salvation came down from heaven, <span class="rubric">(Genuflect)</span> and was incarnate by the Holy Ghost of the Virgin Mary, and was made man; <span class="rubric">(Stand)</span> and was crucified also for us under Pontius Pilate; he suffered and was buried; and the third day he rose again according to the Scriptures, and ascended into heaven, and sitteth on the right hand of the Father;</p>
<p>and he shall come again, with glory, to judge both the quick and the dead; whose kingdom shall have no end.</p>
<p>And I believe in the Holy Ghost the Lord, the Giver of Life, who proceedeth from the Father and the Son; who with the Father and the Son together is worshiped and glorified; who spake by the Prophets.</p>
<p>And I believe one holy Catholic and Apostolic Church; I acknowledge one Baptism for the remission of sins; and I look for the resurrection of the dead, ✠ and the life of the world to come. Amen.</p>
</div>
<p class="lit rubric">The Prayers of the People are offered.</p>"""),
  ("The Penitential Rite", """<p class="lit rubric">After the bidding, the People kneel. Silence may be kept, and then the Priest and People say:</p>
<div class="lit-prayers">
<p>Almighty God, Father of our Lord Jesus Christ, maker of all things, judge of all men: We acknowledge and bewail our manifold sins and wickedness, which we from time to time most grievously have committed, by thought, word, and deed, against thy divine Majesty, provoking most justly thy wrath and indignation against us.</p>
<p>We do earnestly repent, and are heartily sorry for these our misdoings; the remembrance of them is grievous unto us, the burden of them is intolerable.</p>
<p>Have mercy upon us, have mercy upon us, most merciful Father; for thy Son our Lord Jesus Christ&rsquo;s sake, forgive us all that is past; and grant that we may ever hereafter serve and please thee in newness of life, to the honour and glory of thy Name; through Jesus Christ our Lord. Amen.</p>
</div>
<p class="lit rubric">The Priest offers a prayer for absolution.</p>"""),
  ("The Liturgy of the Eucharist", """<p class="lit rubric">The altar is prepared, and then the Priest says:</p>
<p class="lit"><span class="role">Priest:</span> Pray, brethren &hellip; the Father almighty.</p>
<p class="lit rubric">The People stand and respond:</p>
<p class="lit"><span class="role">People:</span> <span class="resp">May the Lord accept the sacrifice at thy hands, for the praise and glory of his Name, for our good and the good of all his holy Church.</span></p>
<p class="lit rubric">The Priest says the Prayer over the Offerings, and then follows the Eucharistic Prayer.</p>
<p class="lit"><span class="role">Priest:</span> The Lord be with you.</p>
<p class="lit"><span class="role">People:</span> <span class="resp">And with thy spirit.</span></p>
<p class="lit"><span class="role">Priest:</span> Lift up your hearts.</p>
<p class="lit"><span class="role">People:</span> <span class="resp">We lift them up unto the Lord.</span></p>
<p class="lit"><span class="role">Priest:</span> Let us give thanks unto the Lord our God.</p>
<p class="lit"><span class="role">People:</span> <span class="resp">It is meet and right so to do.</span></p>
<p class="lit rubric">After the Preface, all continue:</p>
<div class="lit-prayers">
<p>Holy, holy, holy, Lord God of Hosts: Heaven and earth are full of thy glory. Glory be to thee, O Lord Most High. Blessed is he that cometh in the Name of the Lord. Hosanna in the Highest.</p>
</div>
<p class="lit rubric">The People kneel, and the prayer continues.</p>
<p class="lit"><span class="role">Priest:</span> The mystery of faith.</p>
<p class="lit rubric">The People with the Priest (one of the following):</p>
<p class="lit"><span class="resp">We proclaim thy Death, O Lord, and profess thy Resurrection until thou come again.</span></p>
<p class="lit"><em>or</em></p>
<p class="lit"><span class="resp">When we eat this Bread and drink this Cup, we proclaim thy Death, O Lord, until thou come again.</span></p>
<p class="lit"><em>or</em></p>
<p class="lit"><span class="resp">O Saviour of the world, who by thy Cross and precious Blood hast redeemed us: save us and help us, we humbly beseech thee, O Lord.</span></p>"""),
  ("The Communion Rite", """<p class="lit rubric">The People standing, all say the Our Father.</p>
<p class="lit rubric">The Priest continues: &ldquo;Deliver us &hellip; and safe from all distress.&rdquo;</p>
<p class="lit"><span class="role">People:</span> <span class="resp">For thine is the kingdom, and the power, and the glory, for ever and ever. Amen.</span></p>
<p class="lit rubric">The Priest offers a prayer for the peace of Christ, and then says:</p>
<p class="lit"><span class="role">Priest:</span> The peace of the Lord be always with you.</p>
<p class="lit"><span class="role">People:</span> <span class="resp">And with thy spirit.</span></p>
<p class="lit rubric">The People may offer one another a sign of peace.</p>
<p class="lit rubric">The People kneel.</p>
<p class="lit rubric">Breaking the Host, the Priest says:</p>
<p class="lit"><span class="role">Priest:</span> [Alleluia.] Christ our Passover is sacrificed for us;</p>
<p class="lit"><span class="role">People:</span> <span class="resp">Therefore let us keep the feast. [Alleluia.]</span></p>
<p class="lit rubric">The following anthem is sung or said here:</p>
<div class="lit-prayers">
<p>O Lamb of God, that takest away the sins of the world, <span class="resp">have mercy upon us.</span></p>
<p>O Lamb of God, that takest away the sins of the world, <span class="resp">have mercy upon us.</span></p>
<p>O Lamb of God, that takest away the sins of the world, <span class="resp">grant us thy peace.</span></p>
</div>
<p class="lit rubric">The People join in saying this prayer:</p>
<div class="lit-prayers">
<p>We do not presume to come to this thy Table, O merciful Lord, trusting in our own righteousness, but in thy manifold and great mercies. We are not worthy so much as to gather up the crumbs under thy Table. But thou art the same Lord whose property is always to have mercy. Grant us therefore, gracious Lord, so to eat the flesh of thy dear Son Jesus Christ, and to drink his Blood, that our sinful bodies may be made clean by his Body, and our souls washed through his most precious Blood, and that we may evermore dwell in him, and he in us. Amen.</p>
</div>
<p class="lit"><span class="role">Priest:</span> Behold the Lamb of God, behold him that taketh away the sins of the world. Blessed are those who are called to the Supper of the Lamb.</p>
<p class="lit rubric">The People respond thrice:</p>
<p class="lit"><span class="resp">Lord, I am not worthy that thou shouldest come under my roof, but speak the word only, and my soul shall be healed.</span></p>
<p class="lit rubric">The Liturgy continues with the communion of the faithful. At Saint Michael &amp; All Angels, communicants kneel at the altar rail and Father Randall administers communion by intinction, on the tongue. Those not receiving Holy Communion may approach with arms crossed for a blessing &mdash; see <a href="communion.html">Holy Communion</a>.</p>
<p class="lit rubric">After Communion, silence may be kept.</p>
<p class="lit rubric">Then the Priest standing and the People kneeling, all say the following:</p>
<div class="lit-prayers">
<p>Almighty and everliving God, we most heartily thank thee for that thou dost feed us, in these holy mysteries, with the spiritual food of the most precious Body and Blood of thy Son our Saviour Jesus Christ; and dost assure us thereby of thy favour and goodness towards us; and that we are very members incorporate in the mystical body of thy Son, the blessed company of all faithful people; and are also heirs, through hope, of thy everlasting kingdom, by the merits of the most precious death and Passion of thy dear Son. And we humbly beseech thee, O heavenly Father, so to assist us with thy grace, that we may continue in that holy fellowship, and do all such good works as thou hast prepared for us to walk in; through Jesus Christ our Lord, to whom, with thee and the Holy Spirit, be all honour and glory, world without end. Amen.</p>
</div>
<p class="lit rubric">The People remain kneeling and the Postcommunion Prayer follows.</p>"""),
  ("The Concluding Rite", """<p class="lit"><span class="role">Priest:</span> The Lord be with you.</p>
<p class="lit"><span class="role">People:</span> <span class="resp">And with thy spirit.</span></p>
<p class="lit rubric">The Priest gives the blessing.</p>
<p class="lit rubric">The Deacon or Priest dismisses the People, and they respond:</p>
<p class="lit"><span class="role">People:</span> <span class="resp">Thanks be to God.</span></p>
<p class="lit rubric">The People stand for the recessional hymn.</p>"""),
]

mass_body = """<div class="prose">
  <p class="lead">Holy Mass at Saint Michael &amp; All Angels is celebrated in the <strong>Divine Worship</strong> form of the Roman Rite &mdash; the Mass in sacral English, rooted in the Medieval English liturgy. This page follows the order of the Mass from beginning to end, so you can pray along with the priest and the responses. Tap a section to open it; only one is open at a time.</p>
</div>
<div class="faq-list">
"""
for _t, _h in MASS_SECTIONS:
    mass_body += f'<details class="faq-item" name="mass"><summary>{_t}</summary><div class="faq-a">{_h}</div></details>'
    mass_body += '\n'
mass_body += """<p style="color:var(--muted);font-size:.86rem;margin-top:14px;">The text of Holy Mass follows <strong>Divine Worship: The Missal</strong> of the <a href="https://ordinariate.net/" target="_blank" rel="noopener">Personal Ordinariate of the Chair of Saint Peter</a>. Questions? Call the office at <a href="tel:9038217511">903-821-7511</a> or use the <a href="contact.html">contact form</a>.</p></div>
<script>
(function () {
  var probe = document.createElement("details");
  if ("name" in probe) return; /* native exclusive accordion */
  var items = document.querySelectorAll('details[name="mass"]');
  items.forEach(function (det) {
    det.addEventListener("toggle", function () {
      if (!det.open) return;
      items.forEach(function (other) { if (other !== det) other.open = false; });
    });
  });
})();
</script>"""

P("order-of-mass.html", "Order of the Mass",
  "The order of Holy Mass at Saint Michael & All Angels — the Divine Worship form of the Roman Rite in sacral English, with the priest's parts and the People's responses.",
  "Resources", "The Order of the Mass",
  mass_body,
  hero_sub="Follow along with Holy Mass as it is celebrated at Saint Michael & All Angels")


P("daily-readings.html", "Daily Mass Readings",
  "The daily Mass readings at Saint Michael & All Angels — today's readings from the Ordinariate Ordo, linked to Bible Gateway (RSVCE).",
  "Resources", "Daily Mass Readings",
  """<div class="prose">
  <p class="lead">Each day the Church feeds us from Scripture at Mass. The readings below follow today's Mass in the lectionary of the Personal Ordinariate of the Chair of Saint Peter &mdash; tap any citation to read the passage at Bible Gateway (RSVCE).</p>
</div>
<div class="prose" id="readings-card">
  <p>Fetching today's readings&hellip;</p>
</div>

<div class="prose" style="margin-top: 26px;">
  <p>Join us for Holy Mass &mdash; see <a href="mass-times.html">Mass Times</a> for our weekly schedule. Prefer to follow the whole liturgy? See the <a href="order-of-mass.html">Order of the Mass</a>.</p>
</div>

<script>
(function () {
  var wrap = document.getElementById('readings-card');
  fetch('https://scheduler.stmichaelsallangels.com/api/ordo/today', { cache: 'no-store' })
    .then(function (r) { if (!r.ok) throw new Error('no entry for today'); return r.json(); })
    .then(function (d) {
      wrap.textContent = '';
      var h2 = document.createElement('h2');
      h2.textContent = d.title || 'Holy Mass';
      wrap.appendChild(h2);
      var bits = [];
      if (d.date) {
        var dt = new Date(d.date + 'T12:00:00');
        bits.push(dt.toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric', year: 'numeric' }));
      }
      if (d.season) bits.push(d.season);
      if (d.rank) bits.push(d.rank);
      if (d.color) bits.push('Liturgical color: ' + d.color);
      var meta = document.createElement('p');
      meta.style.color = 'var(--muted)';
      meta.textContent = bits.join(' \\u00b7 ');
      wrap.appendChild(meta);
      if (d.notes) {
        var n = document.createElement('p');
        n.style.fontStyle = 'italic';
        n.textContent = d.notes;
        wrap.appendChild(n);
      }
      var readings = d.readings || [];
      if (readings.length) {
        var sched = document.createElement('div');
        sched.className = 'sched';
        sched.style.marginTop = '14px';
        var tbl = document.createElement('table');
        var hr = document.createElement('tr');
        var th1 = document.createElement('th'); th1.textContent = 'Reading';
        var th2 = document.createElement('th'); th2.textContent = 'Citation';
        hr.appendChild(th1); hr.appendChild(th2); tbl.appendChild(hr);
        readings.forEach(function (r) {
          var tr = document.createElement('tr');
          var td1 = document.createElement('td'); td1.textContent = r.label;
          var td2 = document.createElement('td');
          if (r.url) {
            var a = document.createElement('a');
            a.href = r.url; a.target = '_blank'; a.rel = 'noopener';
            a.textContent = r.citation;
            td2.appendChild(a);
          } else { td2.textContent = r.citation; }
          tr.appendChild(td1); tr.appendChild(td2);
          tbl.appendChild(tr);
        });
        sched.appendChild(tbl);
        wrap.appendChild(sched);
      }
      var foot = document.createElement('p');
      foot.style.color = 'var(--muted)'; foot.style.fontSize = '.86rem'; foot.style.marginTop = '14px';
      foot.textContent = 'Citations open at Bible Gateway in the Revised Standard Version, Catholic Edition.';
      wrap.appendChild(foot);
    })
    .catch(function () {
      wrap.textContent = '';
      var p = document.createElement('p');
      p.textContent = "Today's readings are not published on this page yet \\u2014 the daily Ordo data currently begins with the First Sunday of Advent (November 29), and will appear here automatically each day from then on.";
      wrap.appendChild(p);
      var p2 = document.createElement('p');
      var a = document.createElement('a');
      a.href = 'https://ordinariate.net/ordo';
      a.target = '_blank'; a.rel = 'noopener';
      a.textContent = "Meanwhile, see the Ordinariate Ordo for today's readings";
      p2.appendChild(a);
      wrap.appendChild(p2);
    });
})();
</script>""")

P("advent-2026.html", "Advent 2026",
  "Advent 2026 at Saint Michael & All Angels — the season of watching and waiting: Mass times, the 16:8 candle blessing, daily readings, and what Advent is all about.",
  "Resources", "Advent 2026",
  """<div class="prose">
  <p class="lead">Advent 2026 begins <strong>Sunday, November 29</strong> &mdash; the Church's new year &mdash; and runs a full <strong>26 days</strong>, from the First Sunday of Advent to Christmas Eve. Four weeks of quiet, hopeful watching for the coming of Christ: in Bethlehem, at the end of time, and into our hearts each day.</p>
</div>

<div class="advent-grid">
  <div class="advent-card">
    <span class="sun">First Sunday &middot; Nov 29</span>
    <h3>Hope</h3>
    <div class="advent-candles"><span></span></div>
    <p>One candle lit. "Be watchful, be ready."</p>
  </div>
  <div class="advent-card">
    <span class="sun">Second Sunday &middot; Dec 6</span>
    <h3>Peace</h3>
    <div class="advent-candles"><span></span><span></span></div>
    <p>Two candles lit. Prepare the way of the Lord.</p>
  </div>
  <div class="advent-card rose">
    <span class="sun">Third Sunday &middot; Dec 13</span>
    <h3>Joy</h3>
    <div class="advent-candles"><span></span><span></span><span></span></div>
    <p>Three candles &mdash; the rose candle of Gaudete Sunday.</p>
  </div>
  <div class="advent-card">
    <span class="sun">Fourth Sunday &middot; Dec 20</span>
    <h3>Love</h3>
    <div class="advent-candles"><span></span><span></span><span></span><span></span></div>
    <p>All four burning. The King is very near.</p>
  </div>
</div>

<div class="prose">
  <h2>What Is Advent?</h2>
  <p><em>Adventus</em> &mdash; "the coming." Advent is the season the Church sets aside to prepare for the coming of Christ: His coming in history at Bethlehem, His coming in glory at the end of time, and His quiet daily coming into our hearts through grace. The Church dresses her altars in violet, restrains her songs to a holy longing, and asks us simply to make room.</p>
  <p>It is a season of beginnings &mdash; and this year it is also long: 26 days rather than the usual 24, because Christmas falls late in the week. More time to watch. More time to pray.</p>
</div>

<div style="max-width:880px;margin:8px auto 0;">
  <div class="video-embed">
    <iframe src="https://www.youtube-nocookie.com/embed/oA51p5e6RbE?rel=0" title="What Is Advent? Advent 2026 Explained for Catholics" loading="lazy" allowfullscreen allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin"></iframe>
  </div>
  <p class="video-caption">Watch: <strong>What Is Advent? Advent 2026 Explained for Catholics</strong> &mdash; with thanks to <a href="https://www.youtube.com/@holyreels333" target="_blank" rel="noopener">HolyReels</a> on YouTube.</p>
</div>

<div class="prose">
  <h2>Advent at Saint Michael's</h2>
  <p>Weekday Mass is offered <strong>Wednesdays at 6:30 pm</strong>; the <strong>Saturday Vigil at 6:00 pm</strong> and <strong>Sunday Masses at 8:00 &amp; 10:00 am</strong> carry us through each week of the season. <strong>Confession</strong> is Saturdays from 10:00 &ndash; 11:00 am.</p>
  <p>The <strong>16:8 prayer initiative opens Wednesday, December 2</strong> &mdash; the first Wednesday of Advent &mdash; with an opening gathering and blessing of the prayer candles. Bring your candle and begin the year of prayer with us: <a href="168-introduction.html">learn about 16:8</a>.</p>
  <p>The <strong>Solemnity of the Immaculate Conception</strong> falls on Tuesday, December 8 &mdash; Holy Day Mass at 6:30 pm.</p>
  <p><strong>Christmas at Saint Michael's:</strong> Midnight Mass on Friday, December 25 at 12:00 am, and Christmas Day Mass at 10:00 am. This year the Mass takes the place as usual at midnight on the 24th &mdash; plan your arrival with the family for the great Midnight celebration.</p>
  <p>Keep the season day by day: the <a href="daily-readings.html">Daily Mass Readings</a> page follows the Ordo with each day's readings linked to Bible Gateway, and the <a href="order-of-mass.html">Order of the Mass</a> page helps you follow along at Mass. And keep Advent at home &mdash; an Advent wreath on the table, one more candle each Sunday, exactly as our cards above light the way.</p>
</div>

<div class="prose">
  <h2>The Advent Calendar</h2>
  <p>One more way to keep the season: our <a href="advent-calendar.html"><strong>Advent Calendar 2026</strong></a> lays out all 26 days of Advent, from November 29 through Christmas. Each date carries a short daily Bible reading &mdash; from the watchmen waiting for dawn to the shepherds keeping watch by night &mdash; and a simple daily practice drawn from the USCCB&rsquo;s Advent calendar: blessing the wreath, the O Antiphons, planning a confession, inviting the lonely, and more. Hover or tap any date to see the day.</p>
  <p style="text-align:center;margin-top:22px;"><a class="btn btn-primary" href="advent-calendar.html">Open the Advent Calendar &rarr;</a></p>
</div>""")


# ================================================================ ADVENT CALENDAR 2026
# Daily readings: 26-day plan from Christian Pure (christianpure.com/learn/advent-readings/).
# Daily practices: USCCB Advent Calendar 2026 PDF (attributed below).
# kind: '' plain · 'sun' Sunday · 'rose' Gaudete · 'feast' holy day · 'xmas' Christmas
ADV_DAYS = [
  ("sun", "29 <span class=\"m\">Nov</span>", "Ps 130:5–6", "Psalm 130:5-6",
   "<strong>First Sunday of Advent.</strong> Begin your Advent journey by blessing your Advent wreath. Light the first violet candle and sing &ldquo;O Come, O Come, Emmanuel.&rdquo;"),
  ("", "30", "Gen 15:5–6", "Genesis 15:5-6",
   "Today is the Feast of Saint Andrew, the first-called apostle. Pray today for all those who help bring others to Christ."),
  ("", "1 <span class=\"m\">Dec</span>", "2 Sam 7:16", "2 Samuel 7:16",
   "What can you do this Advent to prepare your heart and life for the coming of Christ?"),
  ("", "2", "Ps 80:3", "Psalm 80:3",
   "Make plans to receive the gift of God&rsquo;s mercy in the Sacrament of Penance during this Advent season &mdash; <a href=\"confession.html\">Confession is heard here Saturdays, 10:00&ndash;11:00 am</a>."),
  ("", "3", "Lam 3:25–26", "Lamentations 3:25-26",
   "&ldquo;God is faithful, and by him you were called to fellowship with his Son, Jesus Christ our Lord.&rdquo; &mdash; 1 Corinthians 1:9"),
  ("", "4", "Isa 64:4", "Isaiah 64:4",
   "&ldquo;We journey as if on a bridge that connects earth to Heaven, a bridge that the Lord has built for us.&rdquo; &mdash; Pope Leo XIV, Homily, November 29, 2025"),
  ("", "5", "Hab 2:3", "Habakkuk 2:3",
   "Spend some time writing Christmas cards or sending Christmas greetings. Before bed, say a prayer of thanksgiving for all the people who have enriched your life and strengthened your faith."),
  ("sun", "6", "Isa 40:3", "Isaiah 40:3",
   "<strong>Second Sunday of Advent.</strong> Light two violet candles and ask God for the strength to be like John the Baptist, preparing the way of the Lord."),
  ("", "7", "Isa 40:11", "Isaiah 40:11",
   "&ldquo;The Lord does not delay his promise&hellip; not wishing that any should perish but that all should come to repentance.&rdquo; &mdash; 2 Peter 3:9"),
  ("feast", "8", "Isa 11:1–2", "Isaiah 11:1-2",
   "<strong>Solemnity of the Immaculate Conception</strong> &mdash; a holy day of obligation. Offer your Mass intention today that the nation will live up to its founding principles, established 250 years ago."),
  ("", "9", "Isa 9:2", "Isaiah 9:2",
   "Juan Diego carried the message of Our Lady of Guadalupe to his community. How can you share your faith by word or in action?"),
  ("", "10", "Isa 9:6", "Isaiah 9:6",
   "In the bustle of the holiday season, spend some time this week in silence and prayer, possibly before the Blessed Sacrament, to prepare your heart to receive the Lord at Christmas."),
  ("", "11", "Mic 5:2", "Micah 5:2",
   "&ldquo;Nothing is impossible to God. Let us prepare ourselves for his Kingdom&hellip; The little child, Jesus of Nazareth, will lead us!&rdquo; &mdash; Pope Leo XIV, Angelus, December 7, 2025"),
  ("feast", "12", "Mal 3:1", "Malachi 3:1",
   "<strong>Feast of Our Lady of Guadalupe.</strong> Pray for those who are experiencing difficult pregnancies, and for those who are experiencing child loss or infertility."),
  ("rose", "13", "Phil 4:4–5", "Philippians 4:4-5",
   "<strong>Gaudete Sunday.</strong> At the halfway point of Advent, light two violet candles and the rose candle &mdash; Rejoice! For the Lord is near!"),
  ("", "14", "Zeph 3:17", "Zephaniah 3:17",
   "&ldquo;Let us rejoice, since Jesus is our hope, especially in times of trial&hellip;&rdquo; &mdash; Pope Leo XIV, Angelus, December 14, 2025"),
  ("", "15", "Isa 35:5–6", "Isaiah 35:5-6",
   "According to custom the Christmas tree is set up before Christmas and remains until Epiphany &mdash; share the Church&rsquo;s blessing of a Christmas tree with your family and friends."),
  ("", "16", "Lk 1:57–58", "Luke 1:57-58",
   "&ldquo;Rejoice always. Pray without ceasing. In all circumstances give thanks, for this is the will of God for you in Christ Jesus. Do not quench the Spirit.&rdquo; &mdash; 1 Thessalonians 5:16–19"),
  ("", "17", "Mt 3:1–2", "Matthew 3:1-2",
   "<strong>The O Antiphons begin.</strong> A tradition of Evening Prayer since at least the eighth century &mdash; make each day&rsquo;s antiphon part of your evening meal or bedtime prayers."),
  ("", "18", "Jn 1:35–36", "John 1:35-36",
   "Use the Church&rsquo;s blessing to bless the Nativity Scene in your home: the <em>Blessing of a Christmas Manger or Nativity Scene</em>."),
  ("", "19", "Jn 3:30", "John 3:30",
   "Invite someone who may be alone during the holidays to join you for Mass or another event at your church."),
  ("sun", "20", "Lk 1:38", "Luke 1:38",
   "<strong>Fourth Sunday of Advent.</strong> Light all three violet candles and the rose candle; pray that the light of Christ will enter your heart so that you may share the warmth of God&rsquo;s love with those you meet."),
  ("", "21", "Mt 1:20–21", "Matthew 1:20-21",
   "&ldquo;I will sing forever; through all generations my mouth shall proclaim your faithfulness.&rdquo; &mdash; Psalm 89:2–3"),
  ("", "22", "Lk 1:46–47", "Luke 1:46-47",
   "&ldquo;Piety and charity, mercy and abandonment&hellip; a welcoming manger, a hospitable home, a sign of God&rsquo;s presence.&rdquo; &mdash; Pope Leo XIV, Angelus, December 21, 2025"),
  ("", "23", "Lk 2:4–5", "Luke 2:4-5",
   "In the bustle of Christmas celebrations, take a moment of silence to reflect on the gift of Jesus&rsquo; Incarnation and prepare to receive his Body and Blood in the Holy Eucharist at Christmas Mass."),
  ("", "24", "Lk 2:11", "Luke 2:11",
   "&ldquo;To find the Savior, one must not gaze upward, but look below: the omnipotence of God shines forth in the powerlessness of a newborn.&rdquo; &mdash; Pope Leo XIV, Homily, December 24, 2025"),
  ("xmas", "25", "Lk 2:14", "Luke 2:14",
   "<strong>Christmas.</strong> &ldquo;Glory to God in the highest and on earth peace to those on whom his favor rests.&rdquo; &mdash; Luke 2:14"),
]

def _prayer_item(title, body_html):
    return ('<details class="faq-item" name="advent"><summary>' + title
            + '</summary><div class="faq-a">' + body_html + "</div></details>")

WREATH_ACCORDION = (
    '<div class="prose">'
    "<h2>Advent Wreath and Prayers</h2>"
    '<p class="lead">Blessing the wreath, and the prayer for each week of Advent. The Advent wreath is a family&rsquo;s calendar of light: an evergreen circle with four candles, three violet and one rose, lit one more each week until the room is bright and Christmas arrives. Bless the wreath when it is first set out; pray the week&rsquo;s prayer at the evening meal &mdash; in many families the youngest child lights the candles and the oldest reads the prayer. The circle has no beginning and no end; the evergreen does not die in winter; the growing light answers the shortening days. The rose candle is lit on Gaudete Sunday, the third week, when the Church relaxes the penitential violet for a day because Christmas is close.</p>'
    "</div>"
    '<div class="faq-list">'
    + _prayer_item("Blessing of the Wreath",
        '<div class="lit-prayers"><p>Lord God, Your Church joyfully awaits the coming of its Saviour, who enlightens our hearts and dispels the darkness of ignorance and sin. Pour forth Your blessings upon us as we light the candles of this wreath. May their light reflect the splendour of Christ, who is Lord, for ever and ever. Amen.</p></div>')
    + _prayer_item("First Week &mdash; the candle of hope",
        '<div class="lit-prayers"><p>Lord, stir up Your power and come. Protect us by Your strength and save us from the threatening dangers of our sins, for You are our help and our redeemer. Amen.</p></div>')
    + _prayer_item("Second Week &mdash; the candle of peace",
        '<div class="lit-prayers"><p>Lord, let Your light shine on those who dwell in darkness and in the shadow of death, and guide our feet into the way of peace. Amen.</p></div>')
    + _prayer_item("Third Week &mdash; the rose candle, of joy",
        '<div class="lit-prayers"><p>Lord God, may we, Your people, who look forward to the birthday of Christ, experience the joy of salvation and celebrate that feast with love and thanksgiving. Amen.</p></div>')
    + _prayer_item("Fourth Week &mdash; the candle of love",
        '<div class="lit-prayers"><p>Come, Lord Jesus, do not delay; give new courage to Your people who trust in Your love. By Your coming, raise us to the joy of Your kingdom, where You live and reign for ever and ever. Amen.</p></div>')
    + "</div>"
    + '<script>'
    + '(function () {'
    + '  var probe = document.createElement("details");'
    + '  if ("name" in probe) return; /* native exclusive accordion */'
    + '  var items = document.querySelectorAll(\'details[name="advent"]\');'
    + '  items.forEach(function (det) {'
    + '    det.addEventListener("toggle", function () {'
    + '      if (!det.open) return;'
    + '      items.forEach(function (other) { if (other !== det) other.open = false; });'
    + '    });'
    + '  });'
    + '})();'
    + "</script>")

def advent_calendar_body():
    cells = []
    for i, (kind, date_html, cite, bg_search, tip) in enumerate(ADV_DAYS):
        col = i % 7
        cls = "adv-day" + ((" adv-" + kind) if kind else "")
        if col <= 1:
            tip_cls = " adv-tip-l"
        elif col >= 5:
            tip_cls = " adv-tip-r"
        else:
            tip_cls = ""
        url = ("https://www.biblegateway.com/passage/?search="
               + bg_search.replace(" ", "+").replace(":", "%3A")
               + "&version=RSVCE")
        cells.append(
            '<div class="' + cls + '" tabindex="0">'
            '<span class="adv-date">' + date_html + "</span>"
            '<div class="adv-tip' + tip_cls + '"><span class="adv-tip-tag">Daily Practice</span>' + tip + "</div>"
            '<a class="adv-read" href="' + url + '" target="_blank" rel="noopener">' + cite + "</a>"
            "</div>"
        )
    cells.append('<div class="adv-day adv-blank"></div>')
    grid = '<div class="adv-cal">' + "".join(cells) + "</div>"
    legend = ('<div class="adv-legend">'
              '<span><i style="background:#F3F0F8;"></i> Sunday</span>'
              '<span><i style="background:#FBF1F4;"></i> Gaudete Sunday</span>'
              '<span><i style="background:#FCF6E8;"></i> Holy Days &amp; Christmas</span>'
              "</div>")
    sources = ('<p style="color:var(--muted);font-size:.86rem;margin-top:22px;">'
               "Daily readings follow the 26-day plan from "
               '<a href="https://christianpure.com/learn/advent-readings/" target="_blank" rel="noopener">Christian Pure</a>'
               " &mdash; every citation opens the passage at Bible Gateway (RSVCE). "
               "Daily practices are drawn from the "
               '<a href="https://www.usccb.org/resources/Advent-Calendar-2026-%20English_0.pdf" target="_blank" rel="noopener">USCCB Advent Calendar 2026</a>'
               " (hover or tap any date). Quotations from Pope Leo XIV retain their original attributions.</p>")
    return (WREATH_ACCORDION
            + '<div class="prose">'
            '<p class="lead">Twenty-six days, one short reading each &mdash; from the watchmen waiting for dawn to the shepherds keeping watch by night. Hover or tap any date for that day&rsquo;s practice; tap the reading to open the passage.</p>'
            "</div>" + grid + legend + sources
            + '<div class="prose" style="margin-top:30px;">'
            "<p>Keep it simple: a verse or two a day, read aloud &mdash; alone in the morning, or with the family at supper or bedtime with the wreath lit. If a day slips past, read it with the next day&rsquo;s verse and carry on. And keep the season close at hand: the <a href=\"advent-2026.html\">Advent 2026</a> page has our parish schedule, <a href=\"168-introduction.html\">16:8</a> offers a candle and a year of prayer, and <a href=\"adoration.html\">Saturday adoration</a> pairs with confession all season long.</p>"
            "</div>")

P("advent-calendar.html", "Advent Calendar",
  "Advent Calendar 2026 — a daily Bible reading and a daily practice for every day from the First Sunday of Advent through Christmas.",
  "Resources", "Advent Calendar 2026",
  advent_calendar_body())

P("flocknote.html", "Flocknote",
  "Join the parish email and text list through Flocknote.",
  "Resources", "Stay Connected — Flocknote",
  f"""<div class="prose">
  <p><a href="{CHURCH['flocknote']}"{tgt(True)}>Flocknote</a> is an email and text messaging tool for the parishioners of St Michael &amp; All Angels. It's a smart way for us all to communicate — sign up to receive parish news, special Mass schedules, and event notices.</p>
  <p>Give it a try by clicking below. It takes less than a minute.</p>
</div>
<div style="text-align:center;margin-top: 32px;">
  <a class="btn btn-primary" style="font-size:1.05rem;padding:16px 36px;" href="{CHURCH['flocknote']}"{tgt(True)}>Join Flocknote &rarr;</a>
</div>""")

P("forms.html", "Forms",
  "Parish forms — registration and hall use (PDF downloads).",
  "Resources", "Parish Forms",
  """<div class="prose">
  <p>Download the parish forms below. Complete and return them to the parish office, or place them in the collection basket at Mass.</p>
</div>
<div class="pdf-list" style="margin-top: 28px;">
  <a class="pdf-card" href="assets/downloads/parish-registration-form.pdf" download>
    <div class="badge">PDF</div>
    <div>
      <div class="t">Parish Registration Form</div>
      <div class="d">Register your household with the parish so we can serve you better.</div>
    </div>
  </a>
  <a class="pdf-card" href="assets/downloads/parish-hall-use-form.pdf" download>
    <div class="badge">PDF</div>
    <div>
      <div class="t">Parish Hall Use Form</div>
      <div class="d">Request use of the parish hall for your event or gathering.</div>
    </div>
  </a>
</div>""")

# ---------------------------------------------------------------- write everything
def main():
    os.makedirs(SITE, exist_ok=True)
    made = [build_home()]
    for fname, title, desc, eyebrow, hero_title, body, hero_sub in PAGES:
        made.append(subpage(fname, title, desc, eyebrow, hero_title, body, hero_sub))
    # 404 shim: GitHub Pages has no native pretty URLs; this turns missing
    # paths like /mass-times into /mass-times.html so old links keep working.
    with open(os.path.join(SITE, "404.html"), "w", encoding="utf-8") as f:
        f.write('<!DOCTYPE html><html><head><meta charset="utf-8"><title>Saint Michael &amp; All Angels</title></head><body>'
                '<script>var p=location.pathname.replace(/\\/+$/,"");'
                'if(!p.endsWith(".html")&&!p.endsWith("/")&&!/\\.\\w+$/.test(p))location.replace(p+".html");'
                'else location.replace("/stmichael-site/");</script></body></html>')
    # Legacy redirect: 168.html used to be the single 16:8 page
    with open(os.path.join(SITE, "168.html"), "w", encoding="utf-8") as f:
        f.write('<!DOCTYPE html><html><head><meta charset="utf-8">'
                '<meta http-equiv="refresh" content="0; url=168-introduction.html">'
                '<title>16:8 — Saint Michael &amp; All Angels</title></head>'
                '<body><p>This page has moved. <a href="168-introduction.html">Go to 16:8 Introduction</a>'
                ' &middot; <a href="168-progress.html">Progress &amp; Prayer Log</a></p></body></html>')
    # Retired pages: redirect stubs so old links keep working
    with open(os.path.join(SITE, "newsletter.html"), "w", encoding="utf-8") as f:
        f.write('<!DOCTYPE html><html><head><meta charset="utf-8">'
                '<meta http-equiv="refresh" content="0; url=flocknote.html">'
                '<title>Faithful Focus — Saint Michael &amp; All Angels</title></head>'
                '<body><p>Newsletters are shared through Flocknote. <a href="flocknote.html">Go to Flocknote</a></p></body></html>')
    with open(os.path.join(SITE, "novena.html"), "w", encoding="utf-8") as f:
        f.write('<!DOCTYPE html><html><head><meta charset="utf-8">'
                '<meta http-equiv="refresh" content="0; url=prayers.html">'
                '<title>Holy Spirit Novena — Saint Michael &amp; All Angels</title></head>'
                '<body><p>This page has moved. <a href="prayers.html">Go to Prayers &amp; Intentions</a></p></body></html>')
    print(f"built {len(made) + 2} pages:")
    for f in made:
        size = os.path.getsize(os.path.join(SITE, f))
        print(f"  {f:28s} {size//1024:>4} KB")

if __name__ == "__main__":
    main()
