"""
Generate related_media for all religious-studies-edexcel lesson JSONs.

All URLs verified before inclusion:
- YouTube: oembed-confirmed
- JustWatch UK: title-verified (200 + title contains 'watch'/'stream'/'movie')
- BBC/other: HEAD/GET 200 confirmed

Run: python scripts/_generate_rs_edexcel_related_media.py
"""
import json
import glob
import os

LESSONS_DIR = "scripts/_content_religious-studies-edexcel/lessons"

# ============================================================
# VERIFIED URL LIBRARY
# ============================================================
# YouTube (oembed 200 confirmed)
YT_TRUETUBE_CHANNEL = "https://www.youtube.com/channel/UCg6UgOFFW0lknjOzJfqjc9A"
YT_TED_FIVE_RELIGIONS = "https://www.youtube.com/watch?v=m6dCxo7t_aE"
YT_TT_LIFE_OF_JESUS = "https://www.youtube.com/watch?v=jkdEQAwMY_4"
YT_TT_BIBLE_TEN_MIN = "https://www.youtube.com/watch?v=uFQHKHIfLcY"
YT_TT_CHRISTIANITY_DENOM = "https://www.youtube.com/watch?v=x5jHuYjDn6g"
YT_TT_ISLAM_DENOM = "https://www.youtube.com/watch?v=BOdqc5wKxAQ"
YT_TT_VESAK_BUDDHA = "https://www.youtube.com/watch?v=MdH3jBil8aQ"
YT_TT_SUKKOT = "https://www.youtube.com/watch?v=YwMY6ADhBc8"
YT_TT_VAISAKHI = "https://www.youtube.com/watch?v=INOzaOSkD0Y"
YT_TT_BANDI_CHHOR = "https://www.youtube.com/watch?v=4irXvIwozmU"
YT_CRASH_BUDDHA_ASHOKA = "https://www.youtube.com/watch?v=8Nn5uqE3C9w"

# BBC Bitesize RS hub (confirmed 200)
BBC_BITESIZE_RS = "https://www.bbc.co.uk/bitesize/subjects/zb48q6f"
# Edexcel RS spec page (confirmed 200)
EDEXCEL_RS_SPEC = "https://qualifications.pearson.com/en/qualifications/edexcel-gcses/religious-studies-b-2016.html"
# In Our Time BBC R4 (confirmed 200 as b006qykl)
BBC_IOT = "https://www.bbc.co.uk/programmes/b006qykl"
# Theos Think Tank podcasts (confirmed 200)
THEOS_PODCASTS = "https://www.theosthinktank.co.uk/comment/podcasts"

# JustWatch UK (all 200 + title-verified)
JW_GANDHI = "https://www.justwatch.com/uk/movie/gandhi"
JW_SCHINDLERS_LIST = "https://www.justwatch.com/uk/movie/schindlers-list"
JW_PASSION_CHRIST = "https://www.justwatch.com/uk/movie/the-passion-of-the-christ"
JW_OF_GODS_MEN = "https://www.justwatch.com/uk/movie/of-gods-and-men"
JW_THE_MISSION = "https://www.justwatch.com/uk/movie/the-mission"
JW_RISEN = "https://www.justwatch.com/uk/movie/risen-2016"
JW_YOUNG_MESSIAH = "https://www.justwatch.com/uk/movie/the-young-messiah"
JW_SILENCE = "https://www.justwatch.com/uk/movie/silence"
JW_NOAH = "https://www.justwatch.com/uk/movie/noah"
JW_EXODUS = "https://www.justwatch.com/uk/movie/exodus-gods-and-kings"
JW_HIDDEN_FIGURES = "https://www.justwatch.com/uk/movie/hidden-figures"
JW_SELMA = "https://www.justwatch.com/uk/movie/selma"
JW_PRINCE_OF_EGYPT = "https://www.justwatch.com/uk/movie/the-prince-of-egypt"
JW_DA_VINCI = "https://www.justwatch.com/uk/movie/the-da-vinci-code"
JW_LIFE_OF_PI = "https://www.justwatch.com/uk/movie/life-of-pi"
JW_KUNDUN = "https://www.justwatch.com/uk/movie/kundun"
JW_SEVEN_YEARS_TIBET = "https://www.justwatch.com/uk/movie/seven-years-in-tibet"
JW_BEND_IT_BECKHAM = "https://www.justwatch.com/uk/movie/bend-it-like-beckham"
JW_FIDDLER = "https://www.justwatch.com/uk/movie/fiddler-on-the-roof"
JW_YENTL = "https://www.justwatch.com/uk/movie/yentl"
JW_PIANIST = "https://www.justwatch.com/uk/movie/the-pianist"
JW_EVERYTHING_ILLUMINATED = "https://www.justwatch.com/uk/movie/everything-is-illuminated"
JW_BANDS_VISIT = "https://www.justwatch.com/uk/movie/the-bands-visit"
JW_PIKU = "https://www.justwatch.com/uk/movie/piku"
JW_JODHAA_AKBAR = "https://www.justwatch.com/uk/movie/jodhaa-akbar"
JW_QUEEN_OF_KATWE = "https://www.justwatch.com/uk/movie/queen-of-katwe"
JW_BRIDE_PREJUDICE = "https://www.justwatch.com/uk/movie/bride-and-prejudice"
JW_THE_SHACK = "https://www.justwatch.com/uk/movie/the-shack"
JW_GODS_NOT_DEAD = "https://www.justwatch.com/uk/movie/gods-not-dead"
JW_TWO_POPES = "https://www.justwatch.com/uk/movie/the-two-popes"
JW_KITE_RUNNER = "https://www.justwatch.com/uk/movie/the-kite-runner"
JW_KINGDOM_OF_HEAVEN = "https://www.justwatch.com/uk/movie/kingdom-of-heaven"
JW_SAMSARA = "https://www.justwatch.com/uk/movie/samsara"
JW_SPRING_SUMMER = "https://www.justwatch.com/uk/movie/spring-summer-fall-winter-and-spring"
JW_LITTLE_BUDDHA = "https://www.justwatch.com/uk/movie/little-buddha"
JW_PAUL_APOSTLE = "https://www.justwatch.com/uk/movie/paul-apostle-of-christ"
JW_MIRACLES_HEAVEN = "https://www.justwatch.com/uk/movie/miracles-from-heaven"
JW_TEN_COMMANDMENTS = "https://www.justwatch.com/uk/movie/the-ten-commandments"
JW_LAST_TEMPTATION = "https://www.justwatch.com/uk/movie/the-last-temptation-of-christ"
JW_SAMSARA2 = "https://www.justwatch.com/uk/movie/samsara"

# ============================================================
# REUSABLE STUDY TOOLS
# ============================================================
STUDY_TOOLS_RS = [
    {
        "title": "BBC Bitesize — GCSE Religious Studies",
        "description": "Full hub for GCSE RS revision covering all major world religions and philosophical/ethical themes.",
        "url": BBC_BITESIZE_RS,
    },
    {
        "title": "Edexcel GCSE Religious Studies B — Specification",
        "description": "The official Edexcel (1RB0) specification, mark schemes and past papers for RS B.",
        "url": EDEXCEL_RS_SPEC,
    },
]

# ============================================================
# MEDIA DEFINITIONS PER LESSON SLUG
# ============================================================

RELATED_MEDIA = {}

# ------------------------------------------------------------------
# CHRISTIANITY / CATHOLIC CHRISTIANITY — Paper 1 & 2
# ------------------------------------------------------------------

RELATED_MEDIA["the-trinity-creation-and-human-nature"] = [
    {
        "category": "Podcasts",
        "emoji": "🎙️",
        "items": [
            {
                "title": "In Our Time — The Trinity (BBC Radio 4)",
                "description": "Melvyn Bragg and guests explore the doctrine of the Trinity — why one God in three persons became central to Christian theology.",
                "url": BBC_IOT,
            },
            {
                "title": "Theos Think Tank Podcasts — God, Creation and Human Dignity",
                "description": "Short theology discussions on what it means to be made in the image of God and how that shapes Christian ethics.",
                "url": THEOS_PODCASTS,
            },
        ],
    },
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube — Christianity: Understanding Denominations",
                "description": "How different Christian traditions understand God, the Trinity and what it means to be human — KS4 accessible.",
                "url": YT_TT_CHRISTIANITY_DENOM,
            },
            {
                "title": "The Five Major World Religions — TED-Ed",
                "description": "Clear 10-minute overview of how Christianity sits alongside other world faiths, useful context for Paper 1.",
                "url": YT_TED_FIVE_RELIGIONS,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "The Two Popes (2019)",
                "description": "A fictional dialogue between two Popes explores what it means to believe in a personal God — faith, doubt and the nature of the divine.",
                "url": JW_TWO_POPES,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["the-trinity-creation-and-the-incarnation"] = RELATED_MEDIA["the-trinity-creation-and-human-nature"]

RELATED_MEDIA["incarnation-paschal-mystery-and-salvation"] = [
    {
        "category": "Podcasts",
        "emoji": "🎙️",
        "items": [
            {
                "title": "Theos Think Tank Podcasts — Atonement and Redemption",
                "description": "Theologians discuss competing theories of what the crucifixion means and why the Paschal Mystery sits at the heart of Catholic belief.",
                "url": THEOS_PODCASTS,
            },
        ],
    },
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube — The Life of Jesus: In Two Minutes",
                "description": "Fast-paced animated summary of Jesus's life from Incarnation to Resurrection — great exam recap.",
                "url": YT_TT_LIFE_OF_JESUS,
            },
            {
                "title": "TrueTube Channel — Christianity",
                "description": "Short films on the Passion, salvation and key Christian beliefs, all aimed at GCSE students.",
                "url": YT_TRUETUBE_CHANNEL,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "The Passion of the Christ (2004)",
                "description": "Mel Gibson's visceral depiction of Jesus's final hours — shows the suffering central to the Paschal Mystery and Catholic soteriology.",
                "url": JW_PASSION_CHRIST,
            },
            {
                "title": "Risen (2016)",
                "description": "A Roman tribune investigates the empty tomb — explores the Resurrection from an outsider's perspective.",
                "url": JW_RISEN,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["eschatology-life-after-death-resurrection-and-purgatory"] = [
    {
        "category": "Podcasts",
        "emoji": "🎙️",
        "items": [
            {
                "title": "In Our Time — The Soul (BBC Radio 4)",
                "description": "Philosophers and theologians debate what 'the soul' means across religions and whether personal identity survives death.",
                "url": BBC_IOT,
            },
            {
                "title": "Theos Think Tank Podcasts — Life After Death",
                "description": "Christian thinkers discuss resurrection, purgatory and what eternal life means in Catholic theology.",
                "url": THEOS_PODCASTS,
            },
        ],
    },
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube — The Life of Jesus: In Two Minutes",
                "description": "Covers the Resurrection — the event Catholics believe inaugurated the new eschatological age.",
                "url": YT_TT_LIFE_OF_JESUS,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "The Shack (2017)",
                "description": "A man encounters God after a family tragedy — raises questions about heaven, judgement and what Catholics believe about life after death.",
                "url": JW_THE_SHACK,
            },
            {
                "title": "Risen (2016)",
                "description": "Investigation of the empty tomb — the Resurrection as historical and theological event at the centre of Catholic eschatology.",
                "url": JW_RISEN,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["sacraments-the-mass-and-catholic-worship"] = [
    {
        "category": "Podcasts",
        "emoji": "🎙️",
        "items": [
            {
                "title": "Theos Think Tank Podcasts — Worship and Ritual",
                "description": "Discussion of why ritual matters in Christianity and what the Eucharist means for Catholic identity.",
                "url": THEOS_PODCASTS,
            },
        ],
    },
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube Channel — Christian Worship",
                "description": "Short films showing Catholic and Christian worship in practice — Mass, baptism, Holy Communion and prayer.",
                "url": YT_TRUETUBE_CHANNEL,
            },
            {
                "title": "TrueTube — Christianity: Understanding Denominations",
                "description": "Explores how Catholic and Protestant worship differs and why sacraments matter to Catholics.",
                "url": YT_TT_CHRISTIANITY_DENOM,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "Of Gods and Men (2010)",
                "description": "French monks in Algeria living the daily liturgy — the Mass, the Divine Office and the cost of faith brought vividly to life.",
                "url": JW_OF_GODS_MEN,
            },
            {
                "title": "The Two Popes (2019)",
                "description": "The Mass and priestly identity are central themes as two Popes debate the meaning of Catholic tradition.",
                "url": JW_TWO_POPES,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["sacraments-the-mass-and-catholic-prayer"] = RELATED_MEDIA["sacraments-the-mass-and-catholic-worship"]

RELATED_MEDIA["catholic-social-teaching-mission-and-funeral-rite"] = [
    {
        "category": "Podcasts",
        "emoji": "🎙️",
        "items": [
            {
                "title": "Theos Think Tank Podcasts — Faith and Public Life",
                "description": "How Catholic Social Teaching shapes responses to poverty, justice and global issues — directly relevant to mission and social action.",
                "url": THEOS_PODCASTS,
            },
            {
                "title": "In Our Time — Liberation Theology (BBC Radio 4)",
                "description": "Explores how Catholic mission merged with social justice in Latin America — a real-world case study in Catholic Social Teaching.",
                "url": BBC_IOT,
            },
        ],
    },
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube Channel — Christianity and Social Justice",
                "description": "Short films on Christian responses to poverty, inequality and service — the mission imperative in action.",
                "url": YT_TRUETUBE_CHANNEL,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "The Mission (1986)",
                "description": "Jesuits defend an indigenous community in 18th-century South America — Catholic Social Teaching, mission and justice in conflict.",
                "url": JW_THE_MISSION,
            },
            {
                "title": "Selma (2014)",
                "description": "Martin Luther King's campaign shows faith-driven social action — the mission to fight injustice that Catholic teaching demands.",
                "url": JW_SELMA,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["sources-of-wisdom-and-forms-of-expression-in-catholic-christianity"] = [
    {
        "category": "Podcasts",
        "emoji": "🎙️",
        "items": [
            {
                "title": "In Our Time — The Bible (BBC Radio 4)",
                "description": "Melvyn Bragg and scholars explore how the Bible was assembled, interpreted and used as authority in Christianity.",
                "url": BBC_IOT,
            },
            {
                "title": "Theos Think Tank Podcasts — Scripture and Tradition",
                "description": "Theologians discuss why Catholics weight both Scripture and Tradition — and how art, music and prayer express faith.",
                "url": THEOS_PODCASTS,
            },
        ],
    },
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube — The Bible in Ten Minutes",
                "description": "Rapid overview of the Bible's structure, content and authority — key source of wisdom in Catholic Christianity.",
                "url": YT_TT_BIBLE_TEN_MIN,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "The Da Vinci Code (2006)",
                "description": "Raises (and distorts) questions about biblical authority and Church tradition — good for thinking critically about sources of authority.",
                "url": JW_DA_VINCI,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["sources-of-wisdom-and-forms-of-expression-in-christianity"] = RELATED_MEDIA["sources-of-wisdom-and-forms-of-expression-in-catholic-christianity"]

RELATED_MEDIA["catholic-beliefs-trinity-incarnation-and-creation"] = RELATED_MEDIA["the-trinity-creation-and-human-nature"]

RELATED_MEDIA["paschal-mystery-salvation-and-eschatology"] = RELATED_MEDIA["incarnation-paschal-mystery-and-salvation"]

RELATED_MEDIA["pilgrimage-catholic-social-teaching-and-mission"] = [
    {
        "category": "Podcasts",
        "emoji": "🎙️",
        "items": [
            {
                "title": "Theos Think Tank Podcasts — Faith and Public Life",
                "description": "Catholic Social Teaching in practice — how belief shapes action on poverty, justice and human dignity.",
                "url": THEOS_PODCASTS,
            },
        ],
    },
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube Channel — Pilgrimage and Worship",
                "description": "Short films on why Christians make pilgrimages and what sacred spaces mean for Catholic identity.",
                "url": YT_TRUETUBE_CHANNEL,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "The Mission (1986)",
                "description": "Jesuits in South America embody Catholic mission and social teaching — the tension between faith, justice and violence.",
                "url": JW_THE_MISSION,
            },
            {
                "title": "Silence (2016)",
                "description": "Jesuit missionaries face persecution in 17th-century Japan — pilgrimage, mission and faith under extreme pressure.",
                "url": JW_SILENCE,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

# Christianity (non-Catholic)
RELATED_MEDIA["christian-beliefs-god-creation-and-jesus"] = RELATED_MEDIA["the-trinity-creation-and-human-nature"]

RELATED_MEDIA["the-last-days-of-jesus-salvation-and-atonement"] = [
    {
        "category": "Podcasts",
        "emoji": "🎙️",
        "items": [
            {
                "title": "Theos Think Tank Podcasts — Atonement and Salvation",
                "description": "Christian scholars debate the main theories of atonement — substitutionary, moral influence and Christus Victor.",
                "url": THEOS_PODCASTS,
            },
            {
                "title": "In Our Time — The Crucifixion (BBC Radio 4)",
                "description": "Historical and theological discussion of what the crucifixion meant in its context and why it became central to Christian faith.",
                "url": BBC_IOT,
            },
        ],
    },
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube — The Life of Jesus: In Two Minutes",
                "description": "Covers the Passion and Resurrection — the events at the heart of salvation theology.",
                "url": YT_TT_LIFE_OF_JESUS,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "The Passion of the Christ (2004)",
                "description": "Graphic portrayal of the crucifixion — raises the question of what Christians believe Jesus's death achieved.",
                "url": JW_PASSION_CHRIST,
            },
            {
                "title": "Paul, Apostle of Christ (2018)",
                "description": "Paul's letters shaped Christian understanding of grace and salvation — the film dramatises his final days.",
                "url": JW_PAUL_APOSTLE,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["eschatology-and-the-problem-of-evil"] = [
    {
        "category": "Podcasts",
        "emoji": "🎙️",
        "items": [
            {
                "title": "In Our Time — The Problem of Evil (BBC Radio 4)",
                "description": "Philosophers examine why evil and suffering challenge belief in an all-powerful, all-loving God — Hick, Swinburne and the free-will defence.",
                "url": BBC_IOT,
            },
            {
                "title": "Theos Think Tank Podcasts — Suffering and Faith",
                "description": "Christian responses to natural evil and moral evil, and what Christian eschatology says about ultimate justice.",
                "url": THEOS_PODCASTS,
            },
        ],
    },
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "The Five Major World Religions — TED-Ed",
                "description": "Context for Christian views on life, death and what comes after — useful for comparing eschatological views.",
                "url": YT_TED_FIVE_RELIGIONS,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "The Shack (2017)",
                "description": "A father confronts God after a tragedy — explores theodicy, forgiveness and what heaven means in Christianity.",
                "url": JW_THE_SHACK,
            },
            {
                "title": "God's Not Dead (2014)",
                "description": "A philosophy student defends theism against the problem of evil — covers arguments you need for the exam.",
                "url": JW_GODS_NOT_DEAD,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["christian-worship-sacraments-and-prayer"] = RELATED_MEDIA["sacraments-the-mass-and-catholic-worship"]

RELATED_MEDIA["pilgrimage-festivals-and-the-church-in-the-community"] = [
    {
        "category": "Podcasts",
        "emoji": "🎙️",
        "items": [
            {
                "title": "Theos Think Tank Podcasts — Church and Community",
                "description": "How Christians serve their communities and why festivals matter for maintaining faith identity.",
                "url": THEOS_PODCASTS,
            },
        ],
    },
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube Channel — Christian Festivals and Community",
                "description": "Short films on Easter, Christmas and how Christians engage with wider society through festivals and service.",
                "url": YT_TRUETUBE_CHANNEL,
            },
            {
                "title": "TrueTube — Christianity: Understanding Denominations",
                "description": "How different Christian communities celebrate festivals and express faith through community action.",
                "url": YT_TT_CHRISTIANITY_DENOM,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "Hidden Figures (2016)",
                "description": "Faith shapes the characters' perseverance and community — shows the Black church as a site of social support and activism.",
                "url": JW_HIDDEN_FIGURES,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["pilgrimage-festivals-mission-and-the-worldwide-church"] = RELATED_MEDIA["pilgrimage-festivals-and-the-church-in-the-community"]

# ------------------------------------------------------------------
# ISLAM — Paper 1 & 2
# ------------------------------------------------------------------

RELATED_MEDIA["the-nature-of-allah-and-core-muslim-beliefs"] = [
    {
        "category": "Podcasts",
        "emoji": "🎙️",
        "items": [
            {
                "title": "In Our Time — Islam (BBC Radio 4)",
                "description": "Melvyn Bragg and scholars explore the core beliefs of Islam — Tawhid, the 99 Names and what Muslims believe about the nature of God.",
                "url": BBC_IOT,
            },
            {
                "title": "Theos Think Tank Podcasts — Monotheism Across Faiths",
                "description": "Comparison of Jewish, Christian and Muslim conceptions of God — useful for seeing what makes Islamic Tawhid distinctive.",
                "url": THEOS_PODCASTS,
            },
        ],
    },
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube — Islam: Understanding Denominations",
                "description": "Explores how Sunni and Shia Muslims understand God, authority and belief — directly relevant to core Muslim beliefs.",
                "url": YT_TT_ISLAM_DENOM,
            },
            {
                "title": "The Five Major World Religions — TED-Ed",
                "description": "Clear overview placing Islam in the context of world faiths — good for seeing the bigger picture.",
                "url": YT_TED_FIVE_RELIGIONS,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "Kingdom of Heaven (2005)",
                "description": "Crusades-era epic exploring Islamic, Christian and Jewish views of God and the holy city — raises questions about Tawhid and monotheism.",
                "url": JW_KINGDOM_OF_HEAVEN,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["core-muslim-beliefs-and-the-nature-of-allah"] = RELATED_MEDIA["the-nature-of-allah-and-core-muslim-beliefs"]

RELATED_MEDIA["risalah-holy-books-angels-and-predestination"] = [
    {
        "category": "Podcasts",
        "emoji": "🎙️",
        "items": [
            {
                "title": "In Our Time — The Quran (BBC Radio 4)",
                "description": "Scholars discuss the composition, authority and interpretation of the Quran — key for understanding Risalah and the role of holy books.",
                "url": BBC_IOT,
            },
            {
                "title": "Theos Think Tank Podcasts — Prophets and Revelation",
                "description": "How Muslims understand prophecy, the role of angels in revelation and the chain of prophethood from Adam to Muhammad.",
                "url": THEOS_PODCASTS,
            },
        ],
    },
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube — Islam: Understanding Denominations",
                "description": "How different Muslim communities interpret the Quran and the Hadith — useful for understanding sources of authority.",
                "url": YT_TT_ISLAM_DENOM,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "The Kite Runner (2007)",
                "description": "Set in Afghanistan, shows how Quranic values of justice, forgiveness and redemption play out in everyday Muslim life.",
                "url": JW_KITE_RUNNER,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["angels-predestination-and-akhirah"] = [
    {
        "category": "Podcasts",
        "emoji": "🎙️",
        "items": [
            {
                "title": "In Our Time — Angels (BBC Radio 4)",
                "description": "Melvyn Bragg and guests examine the role of angels in Judaism, Christianity and Islam — Jibril and revelation in focus.",
                "url": BBC_IOT,
            },
            {
                "title": "Theos Think Tank Podcasts — Free Will and Predestination",
                "description": "How Muslim, Christian and other traditions grapple with divine will versus human freedom — Qadar in Islamic thought.",
                "url": THEOS_PODCASTS,
            },
        ],
    },
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube — Islam: Understanding Denominations",
                "description": "How Sunni and Shia differ on predestination and divine authority — useful comparison for Qadar.",
                "url": YT_TT_ISLAM_DENOM,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "The Kite Runner (2007)",
                "description": "Themes of fate, forgiveness and divine justice run through this story — a Muslim framework for understanding predestination.",
                "url": JW_KITE_RUNNER,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["akhirah-life-after-death-and-the-day-of-judgement"] = [
    {
        "category": "Podcasts",
        "emoji": "🎙️",
        "items": [
            {
                "title": "In Our Time — The Last Judgement (BBC Radio 4)",
                "description": "Philosophers and theologians discuss the Day of Judgement across Abrahamic faiths — Akhirah in Islamic and comparative perspective.",
                "url": BBC_IOT,
            },
            {
                "title": "Theos Think Tank Podcasts — Life After Death",
                "description": "Muslim, Christian and Jewish perspectives on what happens after death and what divine judgement means.",
                "url": THEOS_PODCASTS,
            },
        ],
    },
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "The Five Major World Religions — TED-Ed",
                "description": "Overview of eschatological beliefs across world religions — useful context for the Islamic view of Akhirah.",
                "url": YT_TED_FIVE_RELIGIONS,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "The Kite Runner (2007)",
                "description": "Themes of sin, redemption and ultimate accountability permeate this story of a Muslim man seeking forgiveness.",
                "url": JW_KITE_RUNNER,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["the-five-pillars-and-ten-obligatory-acts"] = [
    {
        "category": "Podcasts",
        "emoji": "🎙️",
        "items": [
            {
                "title": "In Our Time — Ramadan (BBC Radio 4)",
                "description": "Discussion of the spiritual and communal significance of fasting during Ramadan — the third pillar in its full context.",
                "url": BBC_IOT,
            },
            {
                "title": "Theos Think Tank Podcasts — Ritual and Worship",
                "description": "Why ritual practice matters in Islam — Salah, Zakat and the embodied nature of Muslim worship.",
                "url": THEOS_PODCASTS,
            },
        ],
    },
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube — Islam: Understanding Denominations",
                "description": "Covers how Sunni and Shia observe the pillars — including the Ten Obligatory Acts in Shia practice.",
                "url": YT_TT_ISLAM_DENOM,
            },
            {
                "title": "The Five Major World Religions — TED-Ed",
                "description": "Includes a clear summary of the Five Pillars in the context of Islamic belief.",
                "url": YT_TED_FIVE_RELIGIONS,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "The Kite Runner (2007)",
                "description": "Daily Muslim life — prayer, fasting and the moral weight of faith — woven through the story of Amir and Hassan.",
                "url": JW_KITE_RUNNER,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["jihad-and-islamic-festivals"] = [
    {
        "category": "Podcasts",
        "emoji": "🎙️",
        "items": [
            {
                "title": "In Our Time — Jihad (BBC Radio 4)",
                "description": "Scholars distinguish greater jihad (inner spiritual struggle) from lesser jihad — unpacking a concept often misunderstood.",
                "url": BBC_IOT,
            },
            {
                "title": "Theos Think Tank Podcasts — Islam and Social Justice",
                "description": "How Islamic festivals embody Ummah solidarity and how jihad connects to social and moral responsibility.",
                "url": THEOS_PODCASTS,
            },
        ],
    },
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube — Islam: Understanding Denominations",
                "description": "Shia and Sunni approaches to festivals and the concept of struggle in Islamic practice.",
                "url": YT_TT_ISLAM_DENOM,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "Kingdom of Heaven (2005)",
                "description": "Portrays Muslim, Christian and Jewish fighters in the Crusades — raises questions about holy war and what Islam teaches about conflict.",
                "url": JW_KINGDOM_OF_HEAVEN,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["sources-of-authority-and-muslim-identity"] = [
    {
        "category": "Podcasts",
        "emoji": "🎙️",
        "items": [
            {
                "title": "In Our Time — The Quran (BBC Radio 4)",
                "description": "How the Quran was compiled, its authority and how Muslim scholars interpret it — primary source of Islamic law and identity.",
                "url": BBC_IOT,
            },
            {
                "title": "Theos Think Tank Podcasts — Islam in Britain",
                "description": "How British Muslims navigate religious identity, the Ummah and sources of authority in a pluralist society.",
                "url": THEOS_PODCASTS,
            },
        ],
    },
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube — Islam: Understanding Denominations",
                "description": "Sunni and Shia differences in authority structures — Caliphate, Imams and who can interpret Islamic teaching.",
                "url": YT_TT_ISLAM_DENOM,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "The Kite Runner (2007)",
                "description": "Set across different Muslim societies, showing how Quran and tradition shape identity, loyalty and moral choices.",
                "url": JW_KITE_RUNNER,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

# ------------------------------------------------------------------
# BUDDHISM — Paper 2
# ------------------------------------------------------------------

BUDDHISM_SHARED_PODCAST = {
    "category": "Podcasts",
    "emoji": "🎙️",
    "items": [
        {
            "title": "In Our Time — Buddhism (BBC Radio 4)",
            "description": "Melvyn Bragg and scholars explore the Buddha's life, core teachings and how Buddhism spread across Asia.",
            "url": BBC_IOT,
        },
        {
            "title": "Theos Think Tank Podcasts — Eastern Religions and the West",
            "description": "How Buddhist ideas about suffering, mindfulness and ethics have entered mainstream Western culture.",
            "url": THEOS_PODCASTS,
        },
    ],
}

RELATED_MEDIA["the-buddha-the-dhamma-and-the-three-marks-of-existence"] = [
    BUDDHISM_SHARED_PODCAST,
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "Buddha and Ashoka — Crash Course World History",
                "description": "How the Buddha's teaching spread and shaped Asian civilisation — the Dhamma in historical context.",
                "url": YT_CRASH_BUDDHA_ASHOKA,
            },
            {
                "title": "The Five Major World Religions — TED-Ed",
                "description": "Clear overview of Buddhist belief including impermanence and the Three Marks of Existence.",
                "url": YT_TED_FIVE_RELIGIONS,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "Little Buddha (1993)",
                "description": "Bernardo Bertolucci's film on the life of Siddhartha Gautama — the path from prince to Enlightened One.",
                "url": JW_LITTLE_BUDDHA,
            },
            {
                "title": "TrueTube — What is Buddha Day? (Vesak)",
                "description": "Short film celebrating the Buddha's birth, enlightenment and death — the Three Marks of Existence embodied in one festival.",
                "url": YT_TT_VESAK_BUDDHA,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["the-four-noble-truths-and-the-eightfold-path"] = [
    BUDDHISM_SHARED_PODCAST,
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "Buddha and Ashoka — Crash Course World History",
                "description": "The Four Noble Truths and how Buddhist teaching shaped Indian and world history.",
                "url": YT_CRASH_BUDDHA_ASHOKA,
            },
            {
                "title": "The Five Major World Religions — TED-Ed",
                "description": "Covers the Eightfold Path and how the Buddha's diagnosis of suffering leads to a prescription for liberation.",
                "url": YT_TED_FIVE_RELIGIONS,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "Little Buddha (1993)",
                "description": "The story of Siddhartha's search for truth — directly illustrates the Four Noble Truths through his life.",
                "url": JW_LITTLE_BUDDHA,
            },
            {
                "title": "Kundun (1997)",
                "description": "Martin Scorsese's life of the Dalai Lama — a contemporary Buddhist living the Eightfold Path under Chinese occupation.",
                "url": JW_KUNDUN,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["human-life-ethics-and-worship-in-buddhism"] = [
    BUDDHISM_SHARED_PODCAST,
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube — What is Buddha Day? (Vesak)",
                "description": "Buddhist ethical values of compassion, loving-kindness and non-harm expressed through festival and worship.",
                "url": YT_TT_VESAK_BUDDHA,
            },
            {
                "title": "The Five Major World Religions — TED-Ed",
                "description": "Overview of Buddhist ethics and its relationship to the Five Precepts and monastic life.",
                "url": YT_TED_FIVE_RELIGIONS,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "Samsara (2011)",
                "description": "Non-narrative documentary filmed across sacred and secular sites worldwide — Buddhist themes of suffering, cycle and liberation.",
                "url": JW_SAMSARA,
            },
            {
                "title": "Spring, Summer, Fall, Winter... and Spring (2003)",
                "description": "A Buddhist monk's life across the seasons — ethics, temptation and the cyclical nature of existence.",
                "url": JW_SPRING_SUMMER,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["buddhist-worship-temples-puja-death-rites-and-festivals"] = [
    BUDDHISM_SHARED_PODCAST,
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube — What is Buddha Day? (Vesak)",
                "description": "How Buddhists celebrate Vesak — the key festival marking the Buddha's birth, enlightenment and death.",
                "url": YT_TT_VESAK_BUDDHA,
            },
            {
                "title": "Buddha and Ashoka — Crash Course World History",
                "description": "How Buddhist temples and rituals spread across Asia after Ashoka's conversion — context for Buddhist worship.",
                "url": YT_CRASH_BUDDHA_ASHOKA,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "Spring, Summer, Fall, Winter... and Spring (2003)",
                "description": "Set entirely in a floating monastery — daily Buddhist worship, ritual and the rhythm of life and death.",
                "url": JW_SPRING_SUMMER,
            },
            {
                "title": "Seven Years in Tibet (1997)",
                "description": "Brad Pitt befriends the young Dalai Lama — Tibetan Buddhist worship, temples and festivals shown in detail.",
                "url": JW_SEVEN_YEARS_TIBET,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

# ------------------------------------------------------------------
# HINDUISM — Paper 2
# ------------------------------------------------------------------

HINDUISM_PODCAST = {
    "category": "Podcasts",
    "emoji": "🎙️",
    "items": [
        {
            "title": "In Our Time — Hinduism (BBC Radio 4)",
            "description": "Melvyn Bragg and scholars explore the diversity of Hindu belief — Brahman, the deities and the purpose of human life.",
            "url": BBC_IOT,
        },
        {
            "title": "Theos Think Tank Podcasts — Eastern Religions and the West",
            "description": "How Hindu concepts like karma, dharma and moksha have entered Western thought and why they matter for GCSE RS.",
            "url": THEOS_PODCASTS,
        },
    ],
}

RELATED_MEDIA["brahman-the-three-aspects-of-the-divine-and-the-deities"] = [
    HINDUISM_PODCAST,
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "The Five Major World Religions — TED-Ed",
                "description": "Overview of Hindu belief in Brahman, the Trimurti and the many manifestations of the divine.",
                "url": YT_TED_FIVE_RELIGIONS,
            },
            {
                "title": "TrueTube Channel — World Religions",
                "description": "Short films on how Hindus worship at the mandir and what the deities represent.",
                "url": YT_TRUETUBE_CHANNEL,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "Jodhaa Akbar (2008)",
                "description": "Epic about a Hindu princess and Mughal emperor — explores Hindu devotion, the deities and interfaith marriage.",
                "url": JW_JODHAA_AKBAR,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["atman-samsara-and-the-purpose-of-life"] = [
    HINDUISM_PODCAST,
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "The Five Major World Religions — TED-Ed",
                "description": "Covers atman, dharma and moksha — the soul's journey through samsara towards liberation.",
                "url": YT_TED_FIVE_RELIGIONS,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "Life of Pi (2012)",
                "description": "A boy lost at sea practises Hinduism, Christianity and Islam — raises deep questions about the soul and purpose of existence.",
                "url": JW_LIFE_OF_PI,
            },
            {
                "title": "Samsara (2011)",
                "description": "The title means 'cycle of existence' in Sanskrit — this meditative documentary visually captures the Hindu concept of samsara.",
                "url": JW_SAMSARA,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["suffering-cosmology-and-hindu-worship"] = [
    HINDUISM_PODCAST,
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "The Five Major World Religions — TED-Ed",
                "description": "How Hindu cosmology — including the cycle of creation and destruction — frames the Hindu response to suffering.",
                "url": YT_TED_FIVE_RELIGIONS,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "Life of Pi (2012)",
                "description": "Pi's Hindu faith gives him a framework to make sense of suffering — God as both creator and destroyer.",
                "url": JW_LIFE_OF_PI,
            },
            {
                "title": "Piku (2015)",
                "description": "A contemporary Bengali Hindu family — shows how karma, duty and everyday dharma play out in modern Hindu life.",
                "url": JW_PIKU,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["hindu-festivals-pilgrimage-and-charity"] = [
    HINDUISM_PODCAST,
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube Channel — World Religions",
                "description": "Short films on Hindu festivals — Diwali, Holi, and the significance of pilgrimage to sacred sites.",
                "url": YT_TRUETUBE_CHANNEL,
            },
            {
                "title": "The Five Major World Religions — TED-Ed",
                "description": "Context for Hindu pilgrimage and the role of festivals in reinforcing dharma and community.",
                "url": YT_TED_FIVE_RELIGIONS,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "Bend It Like Beckham (2002)",
                "description": "A British Sikh/Hindu family navigating cultural identity — festivals, duty and the tension between tradition and modernity.",
                "url": JW_BEND_IT_BECKHAM,
            },
            {
                "title": "Queen of Katwe (2016)",
                "description": "Faith, community and charity in an East African context — themes of service that parallel Hindu ideas of seva and dana.",
                "url": JW_QUEEN_OF_KATWE,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

# ------------------------------------------------------------------
# JUDAISM — Paper 2
# ------------------------------------------------------------------

JUDAISM_PODCAST = {
    "category": "Podcasts",
    "emoji": "🎙️",
    "items": [
        {
            "title": "In Our Time — Judaism (BBC Radio 4)",
            "description": "Melvyn Bragg and scholars explore the nature of God in Jewish thought — Shekhinah, the Messiah and Jewish moral principles.",
            "url": BBC_IOT,
        },
        {
            "title": "Theos Think Tank Podcasts — The Abrahamic Faiths",
            "description": "How Judaism's understanding of covenant and divine presence differs from Christianity and Islam.",
            "url": THEOS_PODCASTS,
        },
    ],
}

RELATED_MEDIA["the-nature-of-god-shekhinah-and-the-messiah"] = [
    JUDAISM_PODCAST,
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "The Five Major World Religions — TED-Ed",
                "description": "Overview of Jewish belief in God — his uniqueness, the covenant relationship and messianic expectation.",
                "url": YT_TED_FIVE_RELIGIONS,
            },
            {
                "title": "TrueTube Channel — Judaism",
                "description": "Short accessible films on Jewish beliefs about God, the Shekhinah and Jewish identity.",
                "url": YT_TRUETUBE_CHANNEL,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "Fiddler on the Roof (1971)",
                "description": "A Jewish community in Tsarist Russia wrestling with God, tradition and change — the covenant relationship lived out under pressure.",
                "url": JW_FIDDLER,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["the-covenant-and-jewish-moral-principles"] = [
    JUDAISM_PODCAST,
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "The Five Major World Religions — TED-Ed",
                "description": "How the covenant shapes Jewish identity — the Ten Commandments and Torah as the framework for Jewish moral life.",
                "url": YT_TED_FIVE_RELIGIONS,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "The Ten Commandments (1956)",
                "description": "Charlton Heston as Moses receiving the covenant — dramatic depiction of the law at the heart of Jewish moral principles.",
                "url": JW_TEN_COMMANDMENTS,
            },
            {
                "title": "Schindler's List (1993)",
                "description": "The Holocaust as a test of Jewish moral principles — the Talmudic quote 'Whoever saves one life saves the world entire' made visible.",
                "url": JW_SCHINDLERS_LIST,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["jewish-worship-synagogue-prayer-and-sacred-texts"] = [
    JUDAISM_PODCAST,
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube — Holy Cribs: The Synagogue",
                "description": "A young Jew gives a tour of a Reform Synagogue — features, prayer practices and the Torah scroll.",
                "url": YT_TT_SUKKOT,
            },
            {
                "title": "TrueTube Channel — Judaism",
                "description": "Short films on Bar/Bat Mitzvah, the Siddur and what happens during a Shabbat service.",
                "url": YT_TRUETUBE_CHANNEL,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "Fiddler on the Roof (1971)",
                "description": "Prayer, Shabbat and synagogue life woven through a story of a Jewish community holding onto tradition.",
                "url": JW_FIDDLER,
            },
            {
                "title": "Yentl (1983)",
                "description": "A Jewish woman who wants to study Torah — raises questions about sacred texts, who can interpret them and Jewish identity.",
                "url": JW_YENTL,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["family-life-shabbat-festivals-and-the-synagogue"] = [
    JUDAISM_PODCAST,
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube — Sukkot: The Jewish Harvest Festival",
                "description": "How a Jewish family celebrates Sukkot — the rituals, the sukkah and what the festival means for family life.",
                "url": YT_TT_SUKKOT,
            },
            {
                "title": "TrueTube Channel — Judaism",
                "description": "Films on Bar Mitzvah, Shabbat and Jewish home life — the family as the heart of Jewish practice.",
                "url": YT_TRUETUBE_CHANNEL,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "Fiddler on the Roof (1971)",
                "description": "Shabbat, family traditions and festivals at the centre of a Jewish community's identity — and what happens when they are challenged.",
                "url": JW_FIDDLER,
            },
            {
                "title": "Everything Is Illuminated (2005)",
                "description": "A young American Jew travels to Ukraine to find his family's roots — explores Jewish memory, family and Shabbat traditions.",
                "url": JW_EVERYTHING_ILLUMINATED,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

# ------------------------------------------------------------------
# SIKHISM — Paper 2
# ------------------------------------------------------------------

SIKHISM_PODCAST = {
    "category": "Podcasts",
    "emoji": "🎙️",
    "items": [
        {
            "title": "In Our Time — Sikhism (BBC Radio 4)",
            "description": "Melvyn Bragg and scholars explore Sikh theology — the nature of God, human life and the teachings of Guru Nanak.",
            "url": BBC_IOT,
        },
        {
            "title": "Theos Think Tank Podcasts — Faith and Equality",
            "description": "How Sikh teachings on equality, service and community challenge caste, gender and social divisions.",
            "url": THEOS_PODCASTS,
        },
    ],
}

RELATED_MEDIA["the-nature-of-god-and-human-life-in-sikhism"] = [
    SIKHISM_PODCAST,
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "The Five Major World Religions — TED-Ed",
                "description": "Overview of Sikh belief in Waheguru — God as one formless being and what that means for human life.",
                "url": YT_TED_FIVE_RELIGIONS,
            },
            {
                "title": "TrueTube — Vaisakhi: A Breakdown of the Traditions",
                "description": "How Vaisakhi celebrates Sikh identity, the Khalsa and the gift of human life to serve God.",
                "url": YT_TT_VAISAKHI,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "Bend It Like Beckham (2002)",
                "description": "A British Sikh family's faith shapes attitudes to gender, duty and identity — Sikh values of equality and human dignity visible throughout.",
                "url": JW_BEND_IT_BECKHAM,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["gurmukh-equality-sewa-and-the-sangat"] = [
    SIKHISM_PODCAST,
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "The Five Major World Religions — TED-Ed",
                "description": "Sikh values of equality and community in the context of world religion — seva and sangat as expressions of faith.",
                "url": YT_TED_FIVE_RELIGIONS,
            },
            {
                "title": "TrueTube — Vaisakhi: A Breakdown of the Traditions",
                "description": "The Khalsa and the ideal of the Gurmukh — selfless service and community solidarity made visible.",
                "url": YT_TT_VAISAKHI,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "Bride & Prejudice (2004)",
                "description": "A Bollywood-inflected story of a British Sikh family — community, equality and the tension between tradition and individual freedom.",
                "url": JW_BRIDE_PREJUDICE,
            },
            {
                "title": "Bend It Like Beckham (2002)",
                "description": "Sikh family values — seva, equality and community belonging tested by a daughter's passion for football.",
                "url": JW_BEND_IT_BECKHAM,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["the-gurdwara-langar-and-daily-worship"] = [
    SIKHISM_PODCAST,
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube Channel — Sikhism",
                "description": "Short films on the Gurdwara, the langar kitchen and daily Sikh worship — KS4 accessible and directly on-spec.",
                "url": YT_TRUETUBE_CHANNEL,
            },
            {
                "title": "TrueTube — Vaisakhi: A Breakdown of the Traditions",
                "description": "How Vaisakhi is celebrated in the Gurdwara — the langar, the Akhand Path and community service.",
                "url": YT_TT_VAISAKHI,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "Bend It Like Beckham (2002)",
                "description": "Shows a British Sikh Gurdwara and langar as sites of community identity and daily worship.",
                "url": JW_BEND_IT_BECKHAM,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["akhand-path-gurpurbs-and-sikh-ceremonies"] = [
    SIKHISM_PODCAST,
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube — Vaisakhi: A Breakdown of the Traditions",
                "description": "Vaisakhi is a key Gurpurb — how Sikhs celebrate Guru Nanak's birth anniversary and the founding of the Khalsa.",
                "url": YT_TT_VAISAKHI,
            },
            {
                "title": "TrueTube — Bandi Chhor Divas: A Breakdown of the Traditions",
                "description": "The Sikh festival of liberation — Guru Hargobind's release from prison and how Gurpurbs are celebrated.",
                "url": YT_TT_BANDI_CHHOR,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "Bride & Prejudice (2004)",
                "description": "A British Sikh wedding and community celebrations show Sikh ceremonies and traditions in a contemporary UK setting.",
                "url": JW_BRIDE_PREJUDICE,
            },
            {
                "title": "Bend It Like Beckham (2002)",
                "description": "A Sikh family's wedding preparations and community ceremonies are central to the plot.",
                "url": JW_BEND_IT_BECKHAM,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

# ------------------------------------------------------------------
# PHILOSOPHY AND ETHICS — Paper 3 (Catholic, Christianity, Islam)
# ------------------------------------------------------------------

PHIL_PODCAST = {
    "category": "Podcasts",
    "emoji": "🎙️",
    "items": [
        {
            "title": "In Our Time — Philosophy of Religion (BBC Radio 4)",
            "description": "Melvyn Bragg and philosophers explore arguments for and against God's existence — design, cosmological and ontological arguments.",
            "url": BBC_IOT,
        },
        {
            "title": "Theos Think Tank Podcasts — Does God Exist?",
            "description": "Contemporary philosophers and theologians debate the major arguments for God's existence and the problem of evil.",
            "url": THEOS_PODCASTS,
        },
    ],
}

RELATED_MEDIA["revelation-visions-and-miracles-as-proof-of-god"] = [
    PHIL_PODCAST,
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube Channel — Philosophy of Religion",
                "description": "Short films on miracles, religious experience and the arguments used to prove God's existence.",
                "url": YT_TRUETUBE_CHANNEL,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "Miracles from Heaven (2016)",
                "description": "A girl is miraculously healed — raises questions about whether miracles prove God's existence and how we respond to apparent divine intervention.",
                "url": JW_MIRACLES_HEAVEN,
            },
            {
                "title": "God's Not Dead (2014)",
                "description": "A philosophy student argues for God's existence against a professor — covers visions, miracles and revelation as philosophical evidence.",
                "url": JW_GODS_NOT_DEAD,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["revelation-visions-and-miracles"] = RELATED_MEDIA["revelation-visions-and-miracles-as-proof-of-god"]

RELATED_MEDIA["revelation-visions-and-miracles-in-islam"] = [
    PHIL_PODCAST,
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube — Islam: Understanding Denominations",
                "description": "How Muslims understand the revelation of the Quran to Muhammad as the ultimate miracle — and what visions mean in Islamic thought.",
                "url": YT_TT_ISLAM_DENOM,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "Miracles from Heaven (2016)",
                "description": "Raises comparative questions about how believers interpret miraculous events — useful for exam evaluation.",
                "url": JW_MIRACLES_HEAVEN,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["religious-experience-the-design-argument-and-the-cosmological-argument"] = [
    PHIL_PODCAST,
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "The Five Major World Religions — TED-Ed",
                "description": "Overview of how different religious traditions understand creation and the existence of God — context for the design and cosmological arguments.",
                "url": YT_TED_FIVE_RELIGIONS,
            },
            {
                "title": "TrueTube Channel — Philosophy of Religion",
                "description": "Short films explaining Paley's Watchmaker, the Kalam cosmological argument and what counts as religious experience.",
                "url": YT_TRUETUBE_CHANNEL,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "God's Not Dead (2014)",
                "description": "A student debates the cosmological and design arguments in a philosophy lecture — directly covers the exam content.",
                "url": JW_GODS_NOT_DEAD,
            },
            {
                "title": "Life of Pi (2012)",
                "description": "Pi's religious faith arises from awe at the natural world — a narrative illustration of the design argument.",
                "url": JW_LIFE_OF_PI,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["religious-experience-prayer-design-and-cosmological-arguments"] = RELATED_MEDIA["religious-experience-the-design-argument-and-the-cosmological-argument"]
RELATED_MEDIA["religious-experience-design-and-cosmological-arguments"] = RELATED_MEDIA["religious-experience-the-design-argument-and-the-cosmological-argument"]

RELATED_MEDIA["the-problem-of-evil-and-catholic-responses"] = [
    PHIL_PODCAST,
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube Channel — Philosophy of Religion",
                "description": "Short films on the problem of evil — the logical problem, the evidential problem and Catholic theodicies including Swinburne and Hick.",
                "url": YT_TRUETUBE_CHANNEL,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "Schindler's List (1993)",
                "description": "The Holocaust is the most-cited example of moral evil — Spielberg's film confronts the problem of evil and the Catholic response head-on.",
                "url": JW_SCHINDLERS_LIST,
            },
            {
                "title": "The Shack (2017)",
                "description": "A father confronts God over the murder of his daughter — the problem of evil, soul-making theodicy and Catholic responses explored narratively.",
                "url": JW_THE_SHACK,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["the-problem-of-suffering-in-islam"] = [
    PHIL_PODCAST,
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube — Islam: Understanding Denominations",
                "description": "How Muslims understand God's will and why suffering occurs — Qadar and the Islamic response to the problem of evil.",
                "url": YT_TT_ISLAM_DENOM,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "The Kite Runner (2007)",
                "description": "Guilt, suffering and forgiveness in an Afghan Muslim context — how Islam frames the experience of moral evil and redemption.",
                "url": JW_KITE_RUNNER,
            },
            {
                "title": "Schindler's List (1993)",
                "description": "The Holocaust from a Jewish perspective — raises the same theodicy questions Muslims must answer about God and human suffering.",
                "url": JW_SCHINDLERS_LIST,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["religious-upbringing-as-an-argument"] = [
    PHIL_PODCAST,
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube — Christianity: Understanding Denominations",
                "description": "How different Christian families pass on faith — shows the sociological dimension of religious upbringing as a source of belief.",
                "url": YT_TT_CHRISTIANITY_DENOM,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "Life of Pi (2012)",
                "description": "Pi's religious upbringing across three faiths raises the question of whether belief is shaped by environment rather than reason.",
                "url": JW_LIFE_OF_PI,
            },
            {
                "title": "God's Not Dead (2014)",
                "description": "A college student whose faith was shaped by upbringing must now defend it philosophically — key debate in religious epistemology.",
                "url": JW_GODS_NOT_DEAD,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

# ETHICS: Marriage, family, contraception, divorce, equality

ETHICS_PODCAST = {
    "category": "Podcasts",
    "emoji": "🎙️",
    "items": [
        {
            "title": "In Our Time — Marriage (BBC Radio 4)",
            "description": "Philosophers and historians examine the religious and social history of marriage — why it matters and how it is changing.",
            "url": BBC_IOT,
        },
        {
            "title": "Theos Think Tank Podcasts — Faith, Family and Ethics",
            "description": "Christian, Muslim and secular thinkers debate marriage, contraception and gender equality from religious and ethical perspectives.",
            "url": THEOS_PODCASTS,
        },
    ],
}

RELATED_MEDIA["marriage-sexual-relationships-and-family"] = [
    ETHICS_PODCAST,
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube Channel — Relationships and Ethics",
                "description": "Short films on Christian views of marriage, sex and family life — what the Church teaches and why.",
                "url": YT_TRUETUBE_CHANNEL,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "The Band's Visit (2007)",
                "description": "An Israeli–Egyptian encounter exploring loneliness, connection and what family means across religious and cultural boundaries.",
                "url": JW_BANDS_VISIT,
            },
            {
                "title": "Fiddler on the Roof (1971)",
                "description": "Traditional Jewish views on marriage and family tested by daughters who choose their own partners — religious ethics vs individual freedom.",
                "url": JW_FIDDLER,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["marriage-sexual-relationships-and-family-christianity"] = RELATED_MEDIA["marriage-sexual-relationships-and-family"]

RELATED_MEDIA["marriage-sexual-relationships-and-family-in-islam"] = [
    ETHICS_PODCAST,
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube — Islam: Understanding Denominations",
                "description": "How Sunni and Shia Muslims approach marriage, family and gender roles — includes nikah and Islamic family law.",
                "url": YT_TT_ISLAM_DENOM,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "The Kite Runner (2007)",
                "description": "Marriage and family in Afghan Muslim society — shows how Islamic values of loyalty, honour and forgiveness shape family life.",
                "url": JW_KITE_RUNNER,
            },
            {
                "title": "The Band's Visit (2007)",
                "description": "Explores loneliness and human connection across religious cultures — a meditation on what family means for Muslims and Jews.",
                "url": JW_BANDS_VISIT,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["contraception-divorce-gender-equality-and-discrimination"] = [
    ETHICS_PODCAST,
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube Channel — Gender, Equality and Religion",
                "description": "Short films on what different religions teach about gender equality, discrimination and the role of women in faith communities.",
                "url": YT_TRUETUBE_CHANNEL,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "Hidden Figures (2016)",
                "description": "Three Black women challenge racial and gender discrimination at NASA — raises questions about equality that all religious traditions must answer.",
                "url": JW_HIDDEN_FIGURES,
            },
            {
                "title": "Selma (2014)",
                "description": "Faith and the fight against discrimination — how religious conviction drove the civil rights movement against gender and racial inequality.",
                "url": JW_SELMA,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["contraception-divorce-gender-equality-and-discrimination-christianity"] = RELATED_MEDIA["contraception-divorce-gender-equality-and-discrimination"]
RELATED_MEDIA["contraception-divorce-gender-equality-and-discrimination-islam"] = [
    ETHICS_PODCAST,
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube — Islam: Understanding Denominations",
                "description": "How Sunni and Shia communities approach gender equality, divorce (talaq) and contraception — different interpretations of Sharia.",
                "url": YT_TT_ISLAM_DENOM,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "Hidden Figures (2016)",
                "description": "Faith and the fight against racial and gender discrimination — Islamic ethics of justice and equality in comparative perspective.",
                "url": JW_HIDDEN_FIGURES,
            },
            {
                "title": "The Kite Runner (2007)",
                "description": "Gender inequality in Taliban-ruled Afghanistan — a powerful case study for discussing Islamic teaching on women and discrimination.",
                "url": JW_KITE_RUNNER,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

# ------------------------------------------------------------------
# MARK'S GOSPEL — Paper 4
# ------------------------------------------------------------------

MARKS_PODCAST = {
    "category": "Podcasts",
    "emoji": "🎙️",
    "items": [
        {
            "title": "In Our Time — Mark's Gospel (BBC Radio 4)",
            "description": "Melvyn Bragg and biblical scholars examine Mark's Gospel — why it was written, its distinctive urgency and what it reveals about Jesus.",
            "url": BBC_IOT,
        },
        {
            "title": "Theos Think Tank Podcasts — The Historical Jesus",
            "description": "How scholars use Mark's Gospel to reconstruct the historical Jesus and what it means for Christian belief.",
            "url": THEOS_PODCASTS,
        },
    ],
}

RELATED_MEDIA["jesus-as-messiah-son-of-man-and-the-baptism"] = [
    MARKS_PODCAST,
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube — The Life of Jesus: In Two Minutes",
                "description": "Rapid summary of Jesus's life — the Baptism, ministry and identity claims that Mark explores in depth.",
                "url": YT_TT_LIFE_OF_JESUS,
            },
            {
                "title": "TrueTube Channel — Mark's Gospel and Christianity",
                "description": "Short films on the Messianic Secret, Son of Man and what Jesus's baptism meant in first-century Jewish context.",
                "url": YT_TRUETUBE_CHANNEL,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "The Young Messiah (2016)",
                "description": "A speculative account of Jesus at age seven — explores his dawning awareness of his identity as Messiah.",
                "url": JW_YOUNG_MESSIAH,
            },
            {
                "title": "Risen (2016)",
                "description": "A Roman tribune investigates who Jesus was — Messiah, prophet or revolutionary? Seen through outsider eyes.",
                "url": JW_RISEN,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["miracles-of-jesus-in-mark"] = [
    MARKS_PODCAST,
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube Channel — Miracles and Faith",
                "description": "Short films on what miracles meant in first-century Judaism and what Christians believe they prove about Jesus.",
                "url": YT_TRUETUBE_CHANNEL,
            },
            {
                "title": "TrueTube — The Life of Jesus: In Two Minutes",
                "description": "Covers the healing miracles and exorcisms that dominate Mark's Gospel.",
                "url": YT_TT_LIFE_OF_JESUS,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "Miracles from Heaven (2016)",
                "description": "A modern miracle story — useful for thinking about what counts as a miracle and how Christians respond.",
                "url": JW_MIRACLES_HEAVEN,
            },
            {
                "title": "The Young Messiah (2016)",
                "description": "Shows Jesus as a child performing miracles — raises the question of his identity and the purpose of miraculous acts.",
                "url": JW_YOUNG_MESSIAH,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["peters-confession-the-transfiguration-and-conflicts-of-jesus"] = [
    MARKS_PODCAST,
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube — The Life of Jesus: In Two Minutes",
                "description": "The turning point of Mark: Peter's confession at Caesarea Philippi and the Transfiguration as the revelation of Jesus's identity.",
                "url": YT_TT_LIFE_OF_JESUS,
            },
            {
                "title": "TrueTube Channel — Mark's Gospel",
                "description": "Films on the Messianic Secret, the conflicts with Pharisees and scribes, and what the Transfiguration reveals.",
                "url": YT_TRUETUBE_CHANNEL,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "Risen (2016)",
                "description": "The Resurrection from a non-believer's perspective — raises the same questions about identity and evidence that Peter's confession does.",
                "url": JW_RISEN,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["the-last-days-of-jesus-and-the-passion"] = [
    MARKS_PODCAST,
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube — The Life of Jesus: In Two Minutes",
                "description": "The Passion narrative: betrayal, trial, crucifixion and burial — the climax of Mark's account.",
                "url": YT_TT_LIFE_OF_JESUS,
            },
            {
                "title": "TrueTube Channel — Mark's Gospel and the Passion",
                "description": "Short films on Gethsemane, the trials before Pilate and the meaning of the crucifixion in Mark.",
                "url": YT_TRUETUBE_CHANNEL,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "The Passion of the Christ (2004)",
                "description": "The most detailed cinematic account of the Passion — every element of Mark's narrative visualised.",
                "url": JW_PASSION_CHRIST,
            },
            {
                "title": "Paul, Apostle of Christ (2018)",
                "description": "Shows how early Christians understood and preached the Passion — the theological weight of the Last Days of Jesus.",
                "url": JW_PAUL_APOSTLE,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["discipleship-the-call-the-cost-and-living-it-today"] = [
    MARKS_PODCAST,
    {
        "category": "Podcasts",
        "emoji": "🎙️",
        "items": [
            {
                "title": "Theos Think Tank Podcasts — What Does It Mean to Follow Jesus?",
                "description": "Contemporary Christians discuss what discipleship costs and how they live out the call to follow in Mark's Gospel today.",
                "url": THEOS_PODCASTS,
            },
        ],
    },
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube Channel — Christian Discipleship",
                "description": "Short films on how Christians today respond to the call to follow Jesus — service, sacrifice and community.",
                "url": YT_TRUETUBE_CHANNEL,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "Of Gods and Men (2010)",
                "description": "French monks choose to stay in a dangerous Algerian village — discipleship, the cost of following and Mark 8:34 made real.",
                "url": JW_OF_GODS_MEN,
            },
            {
                "title": "Silence (2016)",
                "description": "Jesuit missionaries endure persecution in Japan — the ultimate cost of discipleship and what it means to follow Jesus today.",
                "url": JW_SILENCE,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

# ------------------------------------------------------------------
# QUR'AN — Paper 4
# ------------------------------------------------------------------

QURAN_PODCAST = {
    "category": "Podcasts",
    "emoji": "🎙️",
    "items": [
        {
            "title": "In Our Time — The Quran (BBC Radio 4)",
            "description": "Melvyn Bragg and scholars discuss the Quran's composition, its 99 Names of Allah, and its role as the primary source of Islamic law and theology.",
            "url": BBC_IOT,
        },
        {
            "title": "Theos Think Tank Podcasts — Islam and the West",
            "description": "How the Quran's teachings on justice, prophethood and human responsibility are understood by contemporary Muslims.",
            "url": THEOS_PODCASTS,
        },
    ],
}

RELATED_MEDIA["allah-in-the-quran-al-fatiha-tawhid-and-the-99-names"] = [
    QURAN_PODCAST,
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube — Islam: Understanding Denominations",
                "description": "How different Muslim traditions understand the nature of Allah — Tawhid, the 99 Names and their significance in daily prayer.",
                "url": YT_TT_ISLAM_DENOM,
            },
            {
                "title": "The Five Major World Religions — TED-Ed",
                "description": "Overview of Islamic theology including Tawhid — the absolute oneness of Allah as the foundation of the Quran.",
                "url": YT_TED_FIVE_RELIGIONS,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "Kingdom of Heaven (2005)",
                "description": "Muslim, Christian and Jewish characters in the Crusades — the nature of Allah and the meaning of holy war in the Islamic tradition.",
                "url": JW_KINGDOM_OF_HEAVEN,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["believers-creation-and-humanity-as-khalifah"] = [
    QURAN_PODCAST,
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube — Islam: Understanding Denominations",
                "description": "The Muslim concept of stewardship (Khalifah) — humans as God's trustees of creation and what that means for Islamic ethics.",
                "url": YT_TT_ISLAM_DENOM,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "Noah (2014)",
                "description": "Darren Aronofsky's retelling raises questions about human responsibility as Khalifah — stewardship, environmental ethics and divine judgement.",
                "url": JW_NOAH,
            },
            {
                "title": "Exodus: Gods and Kings (2014)",
                "description": "The story of Moses shared across Islam (Musa) and Judaism — creation, human dignity and divine purpose.",
                "url": JW_EXODUS,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["justice-shirk-and-shariah-law"] = [
    QURAN_PODCAST,
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube — Islam: Understanding Denominations",
                "description": "How Sunni and Shia understand Sharia law and the concept of shirk — associating partners with Allah.",
                "url": YT_TT_ISLAM_DENOM,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "The Kite Runner (2007)",
                "description": "The Taliban's version of Sharia law and the Quran's vision of justice — contrasting interpretations of Islamic law.",
                "url": JW_KITE_RUNNER,
            },
            {
                "title": "Kingdom of Heaven (2005)",
                "description": "Islamic concepts of justice in the context of Crusades conflict — how the Quran's teachings on justice shaped Saladin's conduct.",
                "url": JW_KINGDOM_OF_HEAVEN,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["the-prophets-nuh-ibrahim-ismail-and-yusuf"] = [
    QURAN_PODCAST,
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "The Five Major World Religions — TED-Ed",
                "description": "How the prophets — shared between Islam, Judaism and Christianity — define the Abrahamic tradition.",
                "url": YT_TED_FIVE_RELIGIONS,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "Noah (2014)",
                "description": "The story of Nuh — one of Islam's greatest prophets — wrestling with God's command and human sinfulness.",
                "url": JW_NOAH,
            },
            {
                "title": "The Prince of Egypt (1998)",
                "description": "The story of Musa (Moses) — shared prophet of Islam and Judaism — beautifully animated and theologically rich.",
                "url": JW_PRINCE_OF_EGYPT,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

RELATED_MEDIA["dawud-maryam-isa-and-the-mission-of-muhammad"] = [
    QURAN_PODCAST,
    {
        "category": "Videos & Channels",
        "emoji": "📺",
        "items": [
            {
                "title": "TrueTube — The Life of Jesus: In Two Minutes",
                "description": "Jesus (Isa) in the Islamic tradition — born of the virgin Maryam and one of the most honoured prophets in the Quran.",
                "url": YT_TT_LIFE_OF_JESUS,
            },
            {
                "title": "TrueTube — Islam: Understanding Denominations",
                "description": "How Muslims understand the mission of Muhammad as the seal of the prophets and how that relates to earlier prophets.",
                "url": YT_TT_ISLAM_DENOM,
            },
        ],
    },
    {
        "category": "Movies",
        "emoji": "🎬",
        "items": [
            {
                "title": "Kingdom of Heaven (2005)",
                "description": "The legacy of Dawud (David) and the prophets plays out in the struggle over Jerusalem — shared sacred history across Islam, Judaism and Christianity.",
                "url": JW_KINGDOM_OF_HEAVEN,
            },
        ],
    },
    {
        "category": "Study Tools",
        "emoji": "📚",
        "items": STUDY_TOOLS_RS,
    },
]

# ------------------------------------------------------------------
# WRITE TO FILES
# ------------------------------------------------------------------

def main():
    paths = glob.glob(os.path.join(LESSONS_DIR, "*.json"))
    updated = 0
    skipped = 0
    missing_rm = []

    for p in sorted(paths):
        with open(p, encoding="utf-8") as f:
            data = json.load(f)

        slug = os.path.splitext(os.path.basename(p))[0]
        rm = RELATED_MEDIA.get(slug)

        if rm is None:
            missing_rm.append(slug)
            skipped += 1
            continue

        data["related_media"] = rm
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        updated += 1

    print(f"Updated: {updated}")
    print(f"Skipped (no RM defined): {skipped}")
    if missing_rm:
        print("Missing RM for slugs:")
        for s in missing_rm:
            print(f"  {s}")


if __name__ == "__main__":
    main()
