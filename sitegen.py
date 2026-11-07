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
    ("16:8", "168.html", None),
    ("About", None, [
        ("About Us", "about.html", False),
        ("Mass Times", "mass-times.html", False),
        ("Finding Us", "finding-us.html", False),
        ("Prayers & Intentions", "prayers.html", False),
        ("Parish Calendar", "calendar.html", False),
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
        ("Newsletter Archive", "newsletter.html", False),
        ("Flocknote", "flocknote.html", False),
        ("Holy Spirit Novena", "novena.html", False),
        ("Forms", "forms.html", False),
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

def make_page(fname, title, desc, body):
    html = f"""<!DOCTYPE html>
<html lang="en">
{page_head(title, desc)}
<body>
{header()}
{body}
{footer()}
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
    <p><strong>16:8 at St. Michael's</strong> — a shared commitment to prayer, faith, and sacrifice. We will begin on the first Wednesday of Advent with a blessing of the candles. Bring your candle and join us as we begin this journey together.</p>
    <a class="btn btn-primary" style="background: var(--gold);" href="168.html">Learn About 16:8</a>
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
  <p>Click the button below and select the 'Sacramentals Fund' in the drop-down to make your donation today. No donation is too small.</p>
  <p>Thank you for your unwavering support and blessings!</p>
  <p style="margin-top: 28px;"><a class="btn btn-primary" href="https://www.stmichaelsallangels.com/parishioner" target="_blank" rel="noopener">Give to the Sacramentals Fund</a></p>
</div>""")

P("online-giving.html", "Online Giving",
  "Give online to Saint Michael & All Angels — one-time or recurring gifts.",
  "Stewardship", "Online Giving",
  """<div class="prose">
  <p>Online giving is a convenient and secure way to support the parish — whether you're giving to the Regular Offertory, the Sacramentals Fund, or another special collection.</p>
  <p>Through the parish's online giving tool, you have full control over the amount and frequency of your contributions, and you can set up recurring gifts so your support continues even when you're away.</p>
</div>
<div style="text-align:center;margin-top: 32px;">
  <a class="btn btn-primary" style="font-size:1.05rem;padding:16px 36px;" href="https://www.stmichaelsallangels.com/parishioner" target="_blank" rel="noopener">Give Online Now &rarr;</a>
  <p style="font-size:.84rem;color:var(--muted);margin-top:14px;">Opens the parish's current giving page. Once a new giving provider is chosen, this can be embedded directly on this page.</p>
</div>""")

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

P("168.html", "16:8",
  "16:8 at St. Michael's — a shared commitment to prayer, faith, and sacrifice.",
  "16:8", "16:8 at St. Michael's — Begin With Us",
  """<div class="prose">
  <p class="lead">There is brokenness all around us: in our families, in sickness, in grief, and in the burdens we sometimes carry silently. At St. Michael &amp; All Angels, we want to bring those burdens to God together.</p>
  <p>Inspired by 1 Chronicles 16:8, which calls us to give thanks to the Lord, call upon His name, and make His deeds known, <strong>16:8 at St. Michael's</strong> invites our parish into a shared commitment to prayer, faith, and sacrifice.</p>
  <blockquote>"Give thanks to the Lord, call upon His name, and make His deeds known."<div class="cite">— 1 Chronicles 16:8</div></blockquote>
  <p>We will begin on the first Wednesday of Advent with a special blessing of the candles. Bring your candle and join us as we begin this journey together.</p>
  <h2>We believe God hears our prayers. We believe miracles can and do happen.</h2>
  <p>We hold strong to the faith that God listens to our prayers. Miracles are real and happen every day. We seek healing and trust in His perfect timing and presence during our challenges.</p>
</div>""")

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
    print(f"built {len(made)} pages:")
    for f in made:
        size = os.path.getsize(os.path.join(SITE, f))
        print(f"  {f:28s} {size//1024:>4} KB")

if __name__ == "__main__":
    main()
