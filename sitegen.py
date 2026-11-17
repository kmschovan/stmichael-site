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
        ("Mass Times", "mass-times.html", False),
        ("Holy Days of Obligation", "holy-days.html", False),
        ("Finding Us", "finding-us.html", False),
        ("Prayers & Intentions", "prayers.html", False),
        ("Parish Calendar", "calendar.html", False),
        ("Ministry Schedules", "https://parish.key-three.com", True),
        ("Volunteer Signup", "https://signup.com/go/LBAHSJn", True),
        ("Finance Council", "finance-council.html", False),
        ("Parish Council", "parish-council.html", False),
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
        ("Contact Us", "contact.html", False),
        ("OCIA — Becoming Catholic", "ocia.html", False),
        ("Newsletter Archive", "newsletter.html", False),
        ("Flocknote", "flocknote.html", False),
        ("Holy Spirit Novena", "novena.html", False),
        ("Forms", "forms.html", False),
        ("Mass Details", "https://scheduler.stmichaelsallangels.com/display.html", True),
        ("Mass Details (mobile)", "https://scheduler.stmichaelsallangels.com/display_mobile.html", True),
    ]),
]

FOOTER_COLS = [
    ("Our Parish", [
        ("Prayers & Intentions", "prayers.html", False),
        ("Parish Calendar", "calendar.html", False),
        ("Volunteer Signup", "https://signup.com/go/LBAHSJn", True),
        ("Finance Council", "finance-council.html", False),
        ("Parish Council", "parish-council.html", False),
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
        ("Newsletter Archive", "newsletter.html", False),
        ("Flocknote", "flocknote.html", False),
        ("Facebook", HARVEST["site"]["facebook"], True),
        ("Forms", "forms.html", False),
    ]),
]

CHURCH = HARVEST["site"]
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

def footer():
    cols = "".join(
        '<div><h4>' + t + '</h4>' + "".join(link(l, h, e) for l, h, e in links) + '</div>'
        for t, links in FOOTER_COLS)
    return f"""<footer>
  <div class="foot-grid">
    <div>
      <h4>{CHURCH['name']}</h4>
      <p class="mission">A parish of the Personal Ordinariate of the Chair of Saint Peter — fully Catholic, enriched by our Anglican heritage. All are welcome.</p>
      <p class="mission">{CHURCH['address']}<br>{CHURCH['phone']}</p>
    </div>
    {cols}
  </div>
  <div class="foot-bottom">
    <span>&copy; 2026 {CHURCH['name']} &middot; Denison, Texas</span>
    <span>Ordinariate of the Chair of Saint Peter</span>
  </div>
</footer>"""

def page_head(title, desc):
    suffix = "" if "Saint Michael" in title else " — Saint Michael &amp; All Angels Catholic Church, Denison TX"
    return f"""<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}{suffix}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="assets/images/crest.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/site.css">
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
      <p class="welcome">A Parish of the Personal Ordinariate of the Chair of Saint Peter</p>
      <p class="sub">A small Roman Catholic church with a big heart, celebrating reverent liturgy and rich Anglican heritage in the heart of Denison, Texas.</p>
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
        <p>"The holy Eucharist completes Christian initiation." Received kneeling at the altar rail, per the Ordinariate tradition.</p>
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
        "A parish of the Personal Ordinariate of the Chair of Saint Peter in Denison, Texas. Mass times, sacraments, stewardship, and a warm welcome.",
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
  "About Saint Michael & All Angels Catholic Church — a parish of the Personal Ordinariate of the Chair of Saint Peter in Denison, Texas.",
  "About Us", "A small church with a big heart",
  f"""<div class="about-grid">
  <div class="text">
    <p class="lead">"We believe that the door to salvation is always open — and so are the doors to our church."</p>
    <p>We are a small Catholic church with a big heart. Our church is part of the <a href="https://ordinariate.net/"{tgt(True)}>Personal Ordinariate of the Chair of Saint Peter</a>, established by Pope Benedict XVI in 2012 to welcome Anglicans seeking full communion with the Roman Catholic Church. Ordinariate parishes and churches are fully Roman Catholic, while retaining elements of Anglican heritage, enriching the faith through reverent liturgy and historical sacred music.</p>
    <p>All Catholics are warmly invited to join our Divine Worship liturgy and receive Holy Communion. Following the traditions of the Ordinariate, Communion is received by kneeling (if able) at the altar rail and on the tongue.</p>
    <p>The parishioners generally come from across greater Grayson County, Texas, and Southern Bryan County, Oklahoma. United by our love for Christ and our steadfast commitment to the teachings of the Roman Catholic Church, we celebrate our faith with reverence, joy, and warm hospitality, forming a vibrant and diverse community.</p>
    <p>If you are searching for a church home, we warmly invite you to visit us. Saint Michael and All Angels is a welcoming and loving family.</p>
  </div>
  <div class="about-photo">
    <img src="assets/images/church-tall-a.jpg" alt="Parish life at Saint Michael &amp; All Angels">
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
    <tr><th>Date</th><th>Holy Day</th><th>What We Celebrate</th></tr>
    <tr>
      <td>January 1</td>
      <td>Solemnity of Mary, the Holy Mother of God</td>
      <td>The Octave Day of Christmas, honoring the Blessed Virgin Mary as the Mother of God.</td>
    </tr>
    <tr>
      <td>Ascension Thursday</td>
      <td>Solemnity of the Ascension of the Lord</td>
      <td>Forty days after Easter, the Risen Christ ascends into heaven and is seated at the right hand of the Father. In the Ordinariate it is kept on its traditional Thursday.</td>
    </tr>
    <tr>
      <td>August 15</td>
      <td>Solemnity of the Assumption of the Blessed Virgin Mary</td>
      <td>At the end of her earthly life, Mary was taken up body and soul into heavenly glory.</td>
    </tr>
    <tr>
      <td>November 1</td>
      <td>Solemnity of All Saints</td>
      <td>The Church honors all the saints in heaven &mdash; those known by name and the countless unnamed.</td>
    </tr>
    <tr>
      <td>December 8</td>
      <td>Solemnity of the Immaculate Conception</td>
      <td>God preserved the Blessed Virgin Mary from all stain of original sin from the first moment of her conception. She is the Patroness of the United States.</td>
    </tr>
    <tr>
      <td>December 25</td>
      <td>Solemnity of the Nativity of Our Lord Jesus Christ</td>
      <td>Christmas &mdash; the Word became flesh and dwelt among us.</td>
    </tr>
  </table>
</div>
<div class="prose">
  <h2>What the Obligation Means</h2>
  <p>Attending Holy Mass on Sundays and Holy Days of Obligation is one of the precepts of the Church &mdash; the minimum asked of every Catholic. On those days the faithful are bound to participate in the Mass just as on Sunday, unless prevented by serious reason or dispensed by their pastor.</p>
  <p class="cite">Catechism of the Catholic Church, <a href="https://www.vatican.va/archive/ENG0015/__P7O.HTM"{tgt(True)}>2180</a></p>
  <h2>The Holy Days in Our Ordinariate</h2>
  <p>Upon the recommendation of the Governing Council in 2016, Bishop Steven J. Lopes decreed that the six solemnities listed above are observed as Holy Days of Obligation throughout the Personal Ordinariate of the Chair of Saint Peter. Two customs are particular to us: the Ascension is kept on its traditional date, the Thursday forty days after Easter, and whenever January 1, August 15, or November 1 falls on a Saturday or a Monday, the obligation to attend Mass is abrogated &mdash; the feast is still joyfully celebrated, but attendance is no longer required.</p>
  <h2>Holy Day Masses at Saint Michael's</h2>
  <p>When a Holy Day falls on a weekday, Holy Mass is ordinarily offered at 6:30 pm; when it falls on a Sunday, the Sunday Masses of that day fulfill the observance. Please see <a href="mass-times.html">Mass Times</a> and our <a href="https://parish.key-three.com"{tgt(True)}>Ministry Schedules</a> for the exact Holy Day schedule, including Christmas and the Easter Triduum.</p>
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
  <form data-netlify="true" name="prayer-requests" method="POST">
    <input type="hidden" name="form-name" value="prayer-requests">
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
</div>""")

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
  <p>Our material treasure, like our time and talent, is entrusted to us by God. Returning a deliberate, planned portion to the parish supports the works of the Church and is an act of thanksgiving.</p>
  <p style="margin-top: 28px;"><a class="btn btn-primary" href="offertory.html">Ways to Give</a></p>
</div>""")

P("offertory.html", "Regular Offertory",
  "Contributions to the Regular Offertory of Saint Michael & All Angels.",
  "Stewardship", "Regular Offertory",
  """<div class="prose">
  <p>Contributions to the Regular Offertory are crucial in covering the expenses associated with the day-to-day operations of the parish and its programs. These expenses encompass Father's payroll, building maintenance, utilities, and daily supplies, along with supporting our sacramental preparation services and liturgical programs.</p>
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
  <p><strong>Saturdays from 10:00 – 11:00 am</strong> at the parish.</p>
  <p>For alternate times, please call Father Randall at <a href="tel:9038217511">903-821-7511</a>.</p>
</div>""", art="art-confession.webp")

P("communion.html", "Communion",
  "The Holy Eucharist — the source and summit of the Christian life.",
  "The Sacraments", "The Holy Eucharist",
  """<div class="prose">
  <p class="lead">"The holy Eucharist completes Christian initiation. Those who have been raised to the dignity of the royal priesthood by Baptism and configured to Christ by Confirmation participate with the whole community in the Lord's own sacrifice."</p>
  <p>The Eucharist is the source and summit of the Christian life. In the Blessed Sacrament, Christ is truly present — Body, Blood, Soul, and Divinity — under the appearances of bread and wine.</p>
  <p style="color:var(--muted);font-size:.86rem;"><a href="https://www.vatican.va/archive/ENG0015/__P3W.HTM" target="_blank" rel="noopener">— Catechism of the Catholic Church, 1322</a></p>
  <h2>Receiving Holy Communion at Saint Michael's</h2>
  <p>All Catholics free from grave sin and properly disposed are welcome to receive Holy Communion at our Masses. Following the traditions of the Ordinariate, Communion is received <strong>by kneeling (if able) at the altar rail and on the tongue</strong>.</p>
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
    <p class="fund-updated" id="prayer-updated">Sign in with your scheduler account &mdash; takes less than a minute.</p>
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
    <h3>1 &middot; Sign in</h3>
    <p>Use your Mass Scheduler account &mdash; the same one you use to sign up for Mass roles. <a href="https://scheduler.stmichaelsallangels.com/?view=prayer" target="_blank" rel="noopener">Go to the prayer log &rarr;</a></p>
  </div>
  <div class="give-card">
    <h3>2 &middot; New here?</h3>
    <p>Create a free account on the scheduler with your email &mdash; then tap <strong>Prayer Log</strong> at the top. <a href="https://scheduler.stmichaelsallangels.com/?view=prayer" target="_blank" rel="noopener">Create your account &rarr;</a></p>
  </div>
  <div class="give-card">
    <h3>3 &middot; Log &amp; grow</h3>
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
  <form data-netlify="true" name="contact" method="POST">
    <input type="hidden" name="form-name" value="contact">
    <label for="c-name">Your Name *</label>
    <input id="c-name" name="name" type="text" required placeholder="Your name">
    <label for="c-email">Email *</label>
    <input id="c-email" name="email" type="email" required placeholder="you@example.com">
    <label for="c-msg">Message *</label>
    <textarea id="c-msg" name="message" rows="6" required placeholder="How can we help?"></textarea>
    <button class="btn btn-primary" type="submit">Send Message</button>
  </form>
</div>""")

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
    <li><strong>1. Period of Inquiry (Precatechumenate)</strong> — the no-obligation beginning. Come ask questions, share your story, and get to know the parish. At its close, those who wish to continue celebrate the <em>Rite of Acceptance into the Order of Catechumens</em> and become catechumens.</li>
    <li><strong>2. The Catechumenate</strong> — the longest stage, usually running from autumn through Lent. Catechumens study the Creed and the sacraments, hear the Scriptures proclaimed and explained each Sunday (they are dismissed after the Liturgy of the Word for further catechesis), learn Christian prayer, and are accompanied by a sponsor chosen for the journey.</li>
    <li><strong>3. Purification and Enlightenment (Lent)</strong> — the bishop (or his delegate) celebrates the <em>Rite of Election</em>, the Church "elects" the catechumens for the sacraments, and the Lenten Sundays bring the Scrutinies: prayers for deliverance and strengthening as the elect enter a season of recollection before Easter.</li>
    <li><strong>4. Initiation at the Easter Vigil</strong> — the elect receive Baptism, Confirmation, and the Holy Eucharist in one unwinding act at the great Vigil of Easter, made members of Christ and of His Church.</li>
    <li><strong>5. Mystagogy (Easter season into Pentecost)</strong> — the neophytes, newly initiated, reflect on the sacraments received and learn to live them: the whole season is spent "unwrapping the mysteries," joining the full parish life of worship and service.</li>
  </ol>
  <h2>Joining Us</h2>
  <p>Inquiries are welcome at any time of year — you do not need to be sure of anything to begin. Call the parish at <a href="tel:9038217511">903-821-7511</a> or use the <a href="contact.html">contact form</a> and Father Randall or the OCIA coordinator will meet with you. There is never a cost.</p>
</div>""")

P("newsletter.html", "Newsletter Archive",
  "The Faithful Focus newsletter archive of Saint Michael & All Angels.",
  "Resources", "Faithful Focus — Newsletter Archive",
  """<div class="prose">
  <p>Our parish newsletter, <em>Faithful Focus</em>, shares news, devotions, and updates from the parish. Past issues will be archived here as they become available digitally.</p>
</div>
<div class="placeholder" style="margin-top: 28px;">
  <h3>Archive coming soon</h3>
  <p>Until the archive is populated, current newsletters are shared through <a href="flocknote.html">Flocknote</a>. Provide past issues (PDF or links) and Hermes will build the archive index.</p>
</div>""")

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

P("novena.html", "Novena to the Holy Spirit",
  "A nine-day novena to the Holy Spirit, prayed between Ascension and Pentecost.",
  "Resources", "Novena to the Holy Spirit",
  """<div class="prose">
  <p>A novena to the Holy Spirit is a nine-day prayer that invokes the third person of the Trinity and asks for His gifts and graces. It is usually prayed between Ascension Thursday and Pentecost Sunday, when the first disciples received the Holy Spirit.</p>
  <p>Each day of the novena focuses on one of the seven gifts of the Holy Spirit: Wisdom, Understanding, Counsel, Fortitude, Knowledge, Piety, and Fear of the Lord — crowned by the prayer for the fruits of the Spirit.</p>
  <p>The complete novena — with a reflection and audio recording for each day — is available at My Catholic Life:</p>
</div>
<div style="text-align:center;margin-top: 32px;">
  <a class="btn btn-primary" style="font-size:1.05rem;padding:16px 36px;" href="https://mycatholic.life/catholic-prayers/novena-to-the-holy-spirit/" target="_blank" rel="noopener">Pray the Novena &rarr;</a>
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
    # Legacy redirect: 168.html used to be the single 16:8 page
    with open(os.path.join(SITE, "168.html"), "w", encoding="utf-8") as f:
        f.write('<!DOCTYPE html><html><head><meta charset="utf-8">'
                '<meta http-equiv="refresh" content="0; url=168-introduction.html">'
                '<title>16:8 — Saint Michael &amp; All Angels</title></head>'
                '<body><p>This page has moved. <a href="168-introduction.html">Go to 16:8 Introduction</a>'
                ' &middot; <a href="168-progress.html">Progress &amp; Prayer Log</a></p></body></html>')
    print(f"built {len(made) + 1} pages:")
    for f in made:
        size = os.path.getsize(os.path.join(SITE, f))
        print(f"  {f:28s} {size//1024:>4} KB")

if __name__ == "__main__":
    main()
