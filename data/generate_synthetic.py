import json
import random
from pathlib import Path
from typing import Dict, List, Tuple

# Ustawienie ziarna losowości dla powtarzalności eksperymentów ML
random.seed(42)

# =====================================================================
# 1. SŁOWNIK FLEKSYJNY (Polska odmiana -> Rdzenie gygy zgodne z PDF)
# =====================================================================

ACTORS = [
    {"gy": "ku", "nom": "człowiek", "gen": "człowieka", "dat": "człowiekowi", "acc": "człowieka", "gender": "m"},
    {"gy": "ka", "nom": "kobieta", "gen": "kobiety", "dat": "kobiecie", "acc": "kobietę", "gender": "f"},
    {"gy": "kua", "nom": "mężczyzna", "gen": "mężczyzny", "dat": "mężczyźnie", "acc": "mężczyznę", "gender": "m"},
    {"gy": "kuoka", "nom": "matka", "gen": "matki", "dat": "matce", "acc": "matkę", "gender": "f"},
    {"gy": "kuokua", "nom": "ojciec", "gen": "ojca", "dat": "ojcu", "acc": "ojca", "gender": "m"},
    {"gy": "koka", "nom": "córka", "gen": "córki", "dat": "córce", "acc": "córkę", "gender": "f"},
    {"gy": "kokua", "nom": "syn", "gen": "syna", "dat": "synowi", "acc": "syna", "gender": "m"},
    {"gy": "kuokuokua", "nom": "dziadek", "gen": "dziadka", "dat": "dziadkowi", "acc": "dziadka", "gender": "m"},
    {"gy": "kuokuoka", "nom": "babcia", "gen": "babci", "dat": "babci", "acc": "babcię", "gender": "f"},
    {"gy": "gioku", "nom": "mędrzec", "gen": "mędrca", "dat": "mędrcowi", "acc": "mędrca", "gender": "m"},
    {"gy": "gyoku", "nom": "głupiec", "gen": "głupca", "dat": "głupcowi", "acc": "głupca", "gender": "m"},
    {"gy": "giopanuku", "nom": "uczeń", "gen": "ucznia", "dat": "uczniowi", "acc": "ucznia", "gender": "m"},
    {"gy": "giopaku", "nom": "nauczyciel", "gen": "nauczyciela", "dat": "nauczycielowi", "acc": "nauczyciela", "gender": "m"},
    {"gy": "gionuku", "nom": "student", "gen": "studenta", "dat": "studentowi", "acc": "studenta", "gender": "m"},
    {"gy": "giogioku", "nom": "profesor", "gen": "profesora", "dat": "profesorowi", "acc": "profesora", "gender": "m"},
    {"gy": "hoku", "nom": "lekarz", "gen": "lekarza", "dat": "lekarzowi", "acc": "lekarza", "gender": "m"},
    {"gy": "cyeku", "nom": "żołnierz", "gen": "żołnierza", "dat": "żołnierzowi", "acc": "żołnierza", "gender": "m"},
    {"gy": "pioku", "nom": "władca", "gen": "władcy", "dat": "władcy", "acc": "władcę", "gender": "m"},
    {"gy": "poku", "nom": "bogacz", "gen": "bogacza", "dat": "bogaczowi", "acc": "bogacza", "gender": "m"},
    {"gy": "puoku", "nom": "biedak", "gen": "biedaka", "dat": "biedakowi", "acc": "biedaka", "gender": "m"},
    {"gy": "luoku", "nom": "zabójca", "gen": "zabójcy", "dat": "zabójcy", "acc": "zabójcę", "gender": "m"},
    {"gy": "nulaku", "nom": "budowniczy", "gen": "budowniczego", "dat": "budowniczemu", "acc": "budowniczego", "gender": "m"},
    {"gy": "ciaku", "nom": "przyjaciel", "gen": "przyjaciela", "dat": "przyjacielowi", "acc": "przyjaciela", "gender": "m"},
    {"gy": "xyaku", "nom": "wróg", "gen": "wroga", "dat": "wrogowi", "acc": "wroga", "gender": "m"},
    {"gy": "coku", "nom": "klaun", "gen": "klauna", "dat": "klaunowi", "acc": "klauna", "gender": "m"},
    {"gy": "tieso", "nom": "kot", "gen": "kota", "dat": "kotu", "acc": "kota", "gender": "m"},
    {"gy": "dieso", "nom": "pies", "gen": "psa", "dat": "psu", "acc": "psa", "gender": "m"},
    {"gy": "xoso", "nom": "koń", "gen": "konia", "dat": "koniowi", "acc": "konia", "gender": "m"},
    {"gy": "mietieso", "nom": "tygrys", "gen": "tygrysa", "dat": "tygrysowi", "acc": "tygrysa", "gender": "m"},
    {"gy": "piotieso", "nom": "lew", "gen": "lwa", "dat": "lwu", "acc": "lwa", "gender": "m"},
]

OBJECTS = [
    {"gy": "lonu", "nom": "dom", "gen": "domu", "acc": "dom", "gender": "m_inanim"},
    {"gy": "nula", "nom": "budynek", "gen": "budynku", "acc": "budynek", "gender": "m_inanim"},
    {"gy": "gysue", "nom": "książka", "gen": "książki", "acc": "książkę", "gender": "f"},
    {"gy": "suotia", "nom": "chleb", "gen": "chleba", "acc": "chleb", "gender": "m_inanim"},
    {"gy": "sotia", "nom": "mięso", "gen": "mięsa", "acc": "mięso", "gender": "n"},
    {"gy": "fiotya", "nom": "piwo", "gen": "piwa", "acc": "piwo", "gender": "n"},
    {"gy": "fyotya", "nom": "kawa", "gen": "kawy", "acc": "kawę", "gender": "f"},
    {"gy": "syo", "nom": "woda", "gen": "wody", "acc": "wodę", "gender": "f"},
    {"gy": "po", "nom": "bogactwo", "gen": "bogactwa", "acc": "bogactwo", "gender": "n"},
    {"gy": "pora", "nom": "pieniądz", "gen": "pieniądza", "acc": "pieniądz", "gender": "m_inanim"},
    {"gy": "xara", "nom": "samochód", "gen": "samochodu", "acc": "samochód", "gender": "m_inanim"},
    {"gy": "mura", "nom": "komputer", "gen": "komputera", "acc": "komputer", "gender": "m_inanim"},
    {"gy": "hora", "nom": "lekarstwo", "gen": "lekarstwa", "acc": "lekarstwo", "gender": "n"},
    {"gy": "cyara", "nom": "broń", "gen": "broni", "acc": "broń", "gender": "f"},
    {"gy": "fosu", "nom": "kamień", "gen": "kamienia", "acc": "kamień", "gender": "m_inanim"},
    {"gy": "miesuo", "nom": "drzewo", "gen": "drzewa", "acc": "drzewo", "gender": "n"},
    {"gy": "biasuo", "nom": "kwiat", "gen": "kwiatu", "acc": "kwiat", "gender": "m_inanim"},
    {"gy": "syosya", "nom": "błoto", "gen": "błota", "acc": "błoto", "gender": "n"},
    {"gy": "sioduasy", "nom": "sadza", "gen": "sadzy", "acc": "sadzę", "gender": "f"},
    {"gy": "giogy", "nom": "wiedza", "gen": "wiedzy", "acc": "wiedzę", "gender": "f"},
]

ADJECTIVES = [
    {"gy": "rio", "m": "dobry", "f": "dobra", "n": "dobre", "m_acc_anim": "dobrego", "f_acc": "dobrą", "adv": "dobrze"},
    {"gy": "ryo", "m": "zły", "f": "zła", "n": "złe", "m_acc_anim": "złego", "f_acc": "złą", "adv": "źle"},
    {"gy": "gio", "m": "mądry", "f": "mądra", "n": "mądre", "m_acc_anim": "mądrego", "f_acc": "mądrą", "adv": "mądrze"},
    {"gy": "gyo", "m": "głupi", "f": "głupia", "n": "głupie", "m_acc_anim": "głupiego", "f_acc": "głupią", "adv": "głupio"},
    {"gy": "gie", "m": "roztropny", "f": "roztropna", "n": "roztropne", "m_acc_anim": "roztropnego", "f_acc": "roztropną", "adv": "roztropnie"},
    {"gy": "po", "m": "bogaty", "f": "bogata", "n": "bogate", "m_acc_anim": "bogatego", "f_acc": "bogatą", "adv": "bogato"},
    {"gy": "puo", "m": "biedny", "f": "biedna", "n": "biedne", "m_acc_anim": "biednego", "f_acc": "biedną", "adv": "biednie"},
    {"gy": "de", "m": "młody", "f": "młoda", "n": "młode", "m_acc_anim": "młodego", "f_acc": "młodą", "adv": "młodo"},
    {"gy": "due", "m": "stary", "f": "stara", "n": "stare", "m_acc_anim": "starego", "f_acc": "starą", "adv": "staro"},
    {"gy": "mie", "m": "wielki", "f": "wielka", "n": "wielkie", "m_acc_anim": "wielkiego", "f_acc": "wielką", "adv": "wielce"},
    {"gy": "mye", "m": "mały", "f": "mała", "n": "małe", "m_acc_anim": "małego", "f_acc": "małą", "adv": "mało"},
    {"gy": "bia", "m": "piękny", "f": "piękna", "n": "piękne", "m_acc_anim": "pięknego", "f_acc": "piękną", "adv": "pięknie"},
    {"gy": "bya", "m": "brzydki", "f": "brzydka", "n": "brzydkie", "m_acc_anim": "brzydkiego", "f_acc": "brzydką", "adv": "brzydko"},
    {"gy": "ho", "m": "zdrowy", "f": "zdrowa", "n": "zdrowe", "m_acc_anim": "zdrowego", "f_acc": "zdrową", "adv": "zdrowo"},
    {"gy": "huo", "m": "chory", "f": "chora", "n": "chore", "m_acc_anim": "chorego", "f_acc": "chorą", "adv": "choro"},
    {"gy": "dedo", "m": "nowy", "f": "nowa", "n": "nowe", "m_acc_anim": "nowego", "f_acc": "nową", "adv": "nowo"},
    {"gy": "fiot", "m": "biały", "f": "biała", "n": "białe", "m_acc_anim": "białego", "f_acc": "białą", "adv": "biało"},
    {"gy": "fyot", "m": "czarny", "f": "czarna", "n": "czarne", "m_acc_anim": "czarnego", "f_acc": "czarną", "adv": "czarno"},
]

TRANSITIVE_VERBS = [
    {"gy": "te", "pres": "widzi", "past_m": "widział", "past_f": "widziała", "fut": "zobaczy", "inf": "widzieć", "part_act_m": "widzącego", "part_pass_m": "widzianego", "perf_adv": "zobaczywszy"},
    {"gy": "to", "pres": "słyszy", "past_m": "słyszał", "past_f": "słyszała", "fut": "usłyszy", "inf": "słyszeć", "part_act_m": "słyszącego", "part_pass_m": "słyszanego", "perf_adv": "usłyszawszy"},
    {"gy": "la", "pres": "tworzy", "past_m": "stworzył", "past_f": "stworzyła", "fut": "stworzy", "inf": "tworzyć", "part_act_m": "tworzącego", "part_pass_m": "tworzonego", "perf_adv": "stworzywszy"},
    {"gy": "lua", "pres": "niszczy", "past_m": "zniszczył", "past_f": "zniszczyła", "fut": "zniszczy", "inf": "niszczyć", "part_act_m": "niszczącego", "part_pass_m": "niszczonego", "perf_adv": "zniszczywszy"},
    {"gy": "pu", "pres": "ma", "past_m": "miał", "past_f": "miała", "fut": "będzie miał", "inf": "mieć", "part_act_m": "mającego", "part_pass_m": "posiadanego", "perf_adv": "posiadłszy"},
    {"gy": "pua", "pres": "bierze", "past_m": "wziął", "past_f": "wzięła", "fut": "weźmie", "inf": "brać", "part_act_m": "biorącego", "part_pass_m": "branego", "perf_adv": "wziąwszy"},
    {"gy": "tia", "pres": "je", "past_m": "zjadł", "past_f": "zjadła", "fut": "zje", "inf": "jeść", "part_act_m": "jedzącego", "part_pass_m": "jedzonego", "perf_adv": "zjadłszy"},
    {"gy": "nula", "pres": "buduje", "past_m": "zbudował", "past_f": "zbudowała", "fut": "zbuduje", "inf": "budować", "part_act_m": "budującego", "part_pass_m": "budowanego", "perf_adv": "zbudowawszy"},
    {"gy": "gysue", "pres": "czyta", "past_m": "przeczytał", "past_f": "przeczytała", "fut": "przeczyta", "inf": "czytać", "part_act_m": "czytającego", "part_pass_m": "czytanego", "perf_adv": "przeczytawszy"},
    {"gy": "dy", "pres": "szuka", "past_m": "szukał", "past_f": "szukała", "fut": "będzie szukać", "inf": "szukać", "part_act_m": "szukającego", "part_pass_m": "szukanego", "perf_adv": "poszukawszy"},
    {"gy": "dyduo", "pres": "znajduje", "past_m": "znalazł", "past_f": "znalazła", "fut": "znajdzie", "inf": "znaleźć", "part_act_m": "znajdującego", "part_pass_m": "znalezionego", "perf_adv": "znalazłszy"},
    {"gy": "cio", "pres": "kocha", "past_m": "kochał", "past_f": "kochała", "fut": "pokocha", "inf": "kochać", "part_act_m": "kochającego", "part_pass_m": "kochanego", "perf_adv": "pokochawszy"},
    {"gy": "popa", "pres": "kupuje", "past_m": "kupił", "past_f": "kupiła", "fut": "kupi", "inf": "kupować", "part_act_m": "kupującego", "part_pass_m": "kupowanego", "perf_adv": "kupiwszy"},
    {"gy": "popua", "pres": "sprzedaje", "past_m": "sprzedał", "past_f": "sprzedała", "fut": "sprzeda", "inf": "sprzedawać", "part_act_m": "sprzedającego", "part_pass_m": "sprzedawanego", "perf_adv": "sprzedawszy"},
]

INTRANSITIVE_VERBS = [
    {"gy": "lo", "pres": "żyje", "past_m": "żył", "past_f": "żyła", "fut": "będzie żyć", "inf": "żyć"},
    {"gy": "luo", "pres": "umiera", "past_m": "umarł", "past_f": "umarła", "fut": "umrze", "inf": "umierać"},
    {"gy": "fyodupy", "pres": "śpi", "past_m": "spał", "past_f": "spała", "fut": "będzie spać", "inf": "spać"},
    {"gy": "xa", "pres": "idzie", "past_m": "szedł", "past_f": "szła", "fut": "pójdzie", "inf": "iść"},
    {"gy": "xoxa", "pres": "biegnie", "past_m": "biegł", "past_f": "biegła", "fut": "pobiegnie", "inf": "biec"},
    {"gy": "xua", "pres": "stoi", "past_m": "stał", "past_f": "stała", "fut": "będzie stać", "inf": "stać"},
    {"gy": "nuoxua", "pres": "siedzi", "past_m": "siedział", "past_f": "siedziała", "fut": "usiądzie", "inf": "siedzieć"},
    {"gy": "ro", "pres": "pracuje", "past_m": "pracował", "past_f": "pracowała", "fut": "będzie pracować", "inf": "pracować"},
    {"gy": "gioro", "pres": "myśli", "past_m": "myślał", "past_f": "myślała", "fut": "pomyśli", "inf": "myśleć"},
    {"gy": "cuasyo", "pres": "płacze", "past_m": "płakał", "past_f": "płakała", "fut": "zapłacze", "inf": "płakać"},
    {"gy": "gyaca", "pres": "śmieje się", "past_m": "śmiał się", "past_f": "śmiała się", "fut": "zaśmieje się", "inf": "śmiać się"},
    {"gy": "ca", "pres": "cieszy się", "past_m": "cieszył się", "past_f": "cieszyła się", "fut": "ucieszy się", "inf": "cieszyć się"},
    {"gy": "cue", "pres": "boi się", "past_m": "bał się", "past_f": "bała się", "fut": "będzie się bać", "inf": "bać się"},
]

PLACES = [
    {"gy": "lonu", "pl": "w domu"},
    {"gy": "giopanu", "pl": "w szkole"},
    {"gy": "gionu", "pl": "na uczelni"},
    {"gy": "locianu", "pl": "w mieście"},
    {"gy": "suomo", "pl": "w lesie"},
    {"gy": "luocianu", "pl": "na cmentarzu"},
    {"gy": "tianu", "pl": "w jadalni"},
    {"gy": "siotianu", "pl": "w kuchni"},
    {"gy": "lanu", "pl": "w fabryce"},
    {"gy": "syane", "pl": "na ziemi"},
    {"gy": "syone", "pl": "na wodzie"},
    {"gy": "nonu", "pl": "na niebie"},
    {"gy": "nial", "pl": "tutaj"},
    {"gy": "nyal", "pl": "tam"},
    {"gy": "numi", "pl": "wszędzie"},
]

TIMES = [
    {"gy": "dul", "pl": "teraz", "tense_hint": "pres"},
    {"gy": "dumi", "pl": "zawsze", "tense_hint": "pres"},
    {"gy": "fiodu", "pl": "w dzień", "tense_hint": "pres"},
    {"gy": "fyodu", "pl": "w nocy", "tense_hint": "pres"},
    {"gy": "siasyo", "pl": "podczas deszczu", "tense_hint": "pres"},
    {"gy": "dual", "pl": "wtedy", "tense_hint": "past"},
    {"gy": "duafiodu", "pl": "wczoraj", "tense_hint": "past"},
    {"gy": "do", "pl": "na początku", "tense_hint": "past"},
    {"gy": "dafiodu", "pl": "jutro", "tense_hint": "fut"},
]

TENSES = [
    {"gy": "", "name": "pres"},
    {"gy": "dua", "name": "past"},
    {"gy": "da", "name": "fut"},
]


# =====================================================================
# 2. FUNKCJE POMOCNICZE DO SKŁADNI I FLEKSJI
# =====================================================================

def format_noun_phrase(noun: Dict, adj: Dict = None, det: str = None, case: str = "nom") -> Tuple[str, str]:
    """Buduje frazę nominalną w języku polskim i gygy zgodnie z zasadą 'najważniejsze z tyłu'."""
    gy_parts = []
    pl_parts = []

    if adj:
        gy_parts.append(f"{adj['gy']}p")
        if case == "nom":
            pl_parts.append(adj["f"] if noun["gender"] == "f" else (adj["n"] if noun["gender"] == "n" else adj["m"]))
        elif case == "acc":
            if noun["gender"] == "m":
                pl_parts.append(adj["m_acc_anim"])
            elif noun["gender"] == "f":
                pl_parts.append(adj["f_acc"])
            elif noun["gender"] == "n":
                pl_parts.append(adj["n"])
            else:
                pl_parts.append(adj["m"])

    gy_noun = noun["gy"]
    if det == "c":  # pewien
        gy_noun += "c"
        if case == "nom":
            pl_parts.insert(0, "pewna" if noun["gender"] == "f" else "pewien")
        elif case == "acc":
            pl_parts.insert(0, "pewną" if noun["gender"] == "f" else "pewnego")
    elif det == "l":  # ten
        gy_noun += "l"
        if case == "nom":
            pl_parts.insert(0, "ta" if noun["gender"] == "f" else ("to" if noun["gender"] == "n" else "ten"))
        elif case == "acc":
            pl_parts.insert(0, "tę" if noun["gender"] == "f" else ("to" if noun["gender"] == "n" else "tego"))
    elif det == "mi":  # każdy
        gy_noun += "mi"
        if case == "nom":
            pl_parts.insert(0, "każda" if noun["gender"] == "f" else "każdy")
        elif case == "acc":
            pl_parts.insert(0, "każdą" if noun["gender"] == "f" else "każdego")

    gy_parts.append(gy_noun)
    pl_parts.append(noun[case])

    return " ".join(pl_parts), " ".join(gy_parts)


def conjugate_verb(verb: Dict, gender: str, tense_name: str) -> str:
    """Zwraca odpowiednią formę polskiego czasownika dla podanego czasu i rodzaju."""
    if tense_name == "pres":
        return verb["pres"]
    elif tense_name == "past":
        return verb["past_f"] if gender == "f" else verb["past_m"]
    else:
        return verb["fut"]


# =====================================================================
# 3. GENERATORY STRUKTUR GRAMATYCZNYCH (Rozdziały 3 i 4 podręcznika)
# =====================================================================

def gen_simple_sentences() -> Tuple[str, str]:
    """1. Zdania proste (SV oraz OSV) z przydawkami, kwantyfikatorami i czasami."""
    actor = random.choice(ACTORS)
    adj_s = random.choice(ADJECTIVES) if random.random() < 0.6 else None
    det_s = random.choice([None, "c", "l", "mi"]) if random.random() < 0.4 else None
    tense = random.choice(TENSES)

    pl_subj, gy_subj = format_noun_phrase(actor, adj_s, det_s, case="nom")

    if random.random() < 0.4:
        # Zdanie nieprzechodnie: Podmiot-k Orzeczenie-r
        verb = random.choice(INTRANSITIVE_VERBS)
        pl_v = conjugate_verb(verb, actor["gender"], tense["name"])
        pl = f"{pl_subj.capitalize()} {pl_v}."
        gy = f"{gy_subj}k {verb['gy']}{tense['gy']}r."
    else:
        # Zdanie przechodnie (OSV): Dopełnienie-s Podmiot-k Orzeczenie-r
        obj = random.choice(OBJECTS + ACTORS)
        adj_o = random.choice(ADJECTIVES) if random.random() < 0.5 else None
        pl_obj, gy_obj = format_noun_phrase(obj, adj_o, None, case="acc")
        verb = random.choice(TRANSITIVE_VERBS)
        pl_v = conjugate_verb(verb, actor["gender"], tense["name"])
        pl = f"{pl_subj.capitalize()} {pl_v} {pl_obj}."
        gy = f"{gy_obj}s {gy_subj}k {verb['gy']}{tense['gy']}r."

    return pl, gy


def gen_adverbial_and_dative() -> Tuple[str, str]:
    """2. Okoliczniki miejsca/czasu (-n) oraz dopełnienie dalsze (-nion)."""
    actor = random.choice(ACTORS)
    obj = random.choice(OBJECTS)
    tense = random.choice(TENSES)

    if random.random() < 0.5:
        # Dopełnienie dalsze (komu? czemu? -> -nion w okoliczniku)
        recipient = random.choice([a for a in ACTORS if a["gy"] != actor["gy"]])
        pl_verb = "daje" if tense["name"] == "pres" else ("dał" if actor["gender"] == "m" and tense["name"] == "past" else ("dała" if tense["name"] == "past" else "da"))
        if random.random() < 0.5:
            # Z dodatkowym okolicznikiem miejsca połączonym spójnikiem 'ci'
            place = random.choice(PLACES)
            pl = f"{actor['nom'].capitalize()} {pl_verb} {obj['acc']} {recipient['dat']} {place['pl']}."
            gy = f"{recipient['gy']}nio ci {place['gy']}n {obj['gy']}s {actor['gy']}k pa{tense['gy']}r."
        else:
            pl = f"{actor['nom'].capitalize()} {pl_verb} {obj['acc']} {recipient['dat']}."
            gy = f"{recipient['gy']}nion {obj['gy']}s {actor['gy']}k pa{tense['gy']}r."
    else:
        # Okolicznik miejsca lub czasu na początku zdania (szyk AOSPV)
        if random.random() < 0.5:
            place = random.choice(PLACES)
            verb = random.choice(TRANSITIVE_VERBS)
            pl_v = conjugate_verb(verb, actor["gender"], tense["name"])
            pl = f"{place['pl'].capitalize()} {actor['nom']} {pl_v} {obj['acc']}."
            gy = f"{place['gy']}n {obj['gy']}s {actor['gy']}k {verb['gy']}{tense['gy']}r."
        else:
            time_adv = random.choice(TIMES)
            t_gy = "" if time_adv["tense_hint"] == "pres" else ("dua" if time_adv["tense_hint"] == "past" else "da")
            verb = random.choice(INTRANSITIVE_VERBS)
            pl_v = conjugate_verb(verb, actor["gender"], time_adv["tense_hint"])
            pl = f"{time_adv['pl'].capitalize()} {actor['nom']} {pl_v}."
            gy = f"{time_adv['gy']}n {actor['gy']}k {verb['gy']}{t_gy}r."

    return pl, gy


def gen_relative_clauses() -> Tuple[str, str]:
    """3. Zdania podrzędnie złożone przydawkowe z zaimkiem względnym 'hi' (ki ... rp)."""
    actor = random.choice(ACTORS)
    obj = random.choice(OBJECTS)
    sub_verb = random.choice(TRANSITIVE_VERBS)
    main_verb = random.choice(INTRANSITIVE_VERBS)
    sub_tense = random.choice(TENSES)
    main_tense = random.choice(TENSES)

    if random.random() < 0.6:
        # Zdanie przydawkowe określające podmiot (hik):
        # np. "Kot, który zjadł mięso, śpi." -> "ki sotias hik tiaduarp tiesok fyodupyr."
        pron = "która" if actor["gender"] == "f" else "który"
        pl_sub_v = conjugate_verb(sub_verb, actor["gender"], sub_tense["name"])
        pl_main_v = conjugate_verb(main_verb, actor["gender"], main_tense["name"])

        pl = f"{actor['nom'].capitalize()}, {pron} {pl_sub_v} {obj['acc']}, {pl_main_v}."
        gy = f"ki {obj['gy']}s hik {sub_verb['gy']}{sub_tense['gy']}rp {actor['gy']}k {main_verb['gy']}{main_tense['gy']}r."
    else:
        # Zdanie przydawkowe określające dopełnienie (his):
        # np. "Mędrzec widzi dom, który zbudował uczeń." -> "ki his giopanukuk nuladuarp lonus giokuk ter."
        actor2 = random.choice([a for a in ACTORS if a["gy"] != actor["gy"]])
        main_tr_verb = random.choice(TRANSITIVE_VERBS)
        pron_acc = "którą" if obj["gender"] == "f" else ("które" if obj["gender"] == "n" else "który")
        pl_sub_v = conjugate_verb(sub_verb, actor2["gender"], "past")
        pl_main_v = conjugate_verb(main_tr_verb, actor["gender"], "pres")

        pl = f"{actor['nom'].capitalize()} {pl_main_v} {obj['acc']}, {pron_acc} {pl_sub_v} {actor2['nom']}."
        gy = f"ki his {actor2['gy']}k {sub_verb['gy']}duarp {obj['gy']}s {actor['gy']}k {main_tr_verb['gy']}r."

    return pl, gy


def gen_temporal_and_purpose_clauses() -> Tuple[str, str]:
    """4. Zdania podrzędne okolicznikowe czasu (nuadun / nadun) oraz celu (xen)."""
    actor = random.choice(ACTORS)
    obj = random.choice(OBJECTS)
    tr_verb = random.choice(TRANSITIVE_VERBS)
    intr_verb = random.choice(INTRANSITIVE_VERBS)

    choice = random.choice(["after", "before", "purpose"])
    if choice == "after":
        # Po tym, gdy... (ki ... rp nuadun ...)
        pl_v1 = conjugate_verb(tr_verb, actor["gender"], "past")
        pl_v2 = conjugate_verb(intr_verb, actor["gender"], "pres")
        pl = f"{actor['nom'].capitalize()} {pl_v2}, po tym, gdy {pl_v1} {obj['acc']}."
        gy = f"ki {obj['gy']}s {tr_verb['gy']}duarp nuadun {actor['gy']}k {intr_verb['gy']}r."
    elif choice == "before":
        # Zanim... (ki ... rp nadun ...)
        pl_v1 = conjugate_verb(tr_verb, actor["gender"], "fut")
        pl_v2 = conjugate_verb(intr_verb, actor["gender"], "pres")
        pl = f"Zanim {actor['nom']} {pl_v1} {obj['acc']}, {pl_v2}."
        gy = f"ki {obj['gy']}s {tr_verb['gy']}darp nadun {actor['gy']}k {intr_verb['gy']}r."
    else:
        # Zdanie celowe: żeby... (ki ... rp xen ...)
        move_verb = random.choice([v for v in INTRANSITIVE_VERBS if v["gy"] in ("xa", "xoxa")])
        pl_move = conjugate_verb(move_verb, actor["gender"], "pres")
        pl = f"{actor['nom'].capitalize()} {pl_move}, żeby {tr_verb['inf']} {obj['acc']}."
        gy = f"ki {obj['gy']}s {tr_verb['gy']}rp xen {actor['gy']}k {move_verb['gy']}r."

    return pl, gy


def gen_coordinate_sentences() -> Tuple[str, str]:
    """5. Zdania złożone współrzędnie ze spójnikami (ci, si, xi, pi, le, ni, bi)."""
    conjunctions = [
        {"gy": "ci", "pl": "i"},
        {"gy": "si", "pl": "lub"},
        {"gy": "xi", "pl": "więc"},
        {"gy": "pi", "pl": ", ale"},
        {"gy": "le", "pl": ", bo"},
        {"gy": "bi", "pl": "wtedy i tylko wtedy, gdy"},
    ]
    conj = random.choice(conjunctions)
    a1 = random.choice(ACTORS)
    a2 = random.choice(ACTORS)
    v1 = random.choice(INTRANSITIVE_VERBS)
    v2 = random.choice(INTRANSITIVE_VERBS)
    tense = random.choice(TENSES)

    pl_v1 = conjugate_verb(v1, a1["gender"], tense["name"])
    pl_v2 = conjugate_verb(v2, a2["gender"], tense["name"])

    sep = " " if not conj["pl"].startswith(",") else ""
    pl = f"{a1['nom'].capitalize()} {pl_v1}{sep}{conj['pl']} {a2['nom']} {pl_v2}."
    gy = f"{a1['gy']}k {v1['gy']}{tense['gy']}r {conj['gy']} {a2['gy']}k {v2['gy']}{tense['gy']}r."
    return pl, gy


def gen_conditionals_and_irrealis() -> Tuple[str, str]:
    """6. Okresy warunkowe rzeczywiste i nierzeczywiste (tryb przypuszczający 'fi')."""
    a1 = random.choice(ACTORS)
    a2 = random.choice(ACTORS)
    v1 = random.choice(INTRANSITIVE_VERBS)
    v2 = random.choice(INTRANSITIVE_VERBS)

    if random.random() < 0.5:
        # Tryb przypuszczający (Gdyby ... to ... - morfem fi)
        pl_v1 = conjugate_verb(v1, a1["gender"], "past")
        pl_v2 = conjugate_verb(v2, a2["gender"], "past")
        neg = random.random() < 0.4
        if neg:
            pl = f"Gdyby {a1['nom']} nie {pl_v1}, to {a2['nom']} {pl_v2}by."
            gy = f"ki {a1['gy']}k {v1['gy']}guafirp xue ci {a2['gy']}k {v2['gy']}fir."
        else:
            pl = f"Gdyby {a1['nom']} {pl_v1}, to {a2['nom']} {pl_v2}by."
            gy = f"ki {a1['gy']}k {v1['gy']}firp xue ci {a2['gy']}k {v2['gy']}fir."
    else:
        # Warunek rzeczywisty w okoliczniku (ki ... r xuen ...)
        obj = random.choice(OBJECTS)
        tr_v = random.choice(TRANSITIVE_VERBS)
        pl_v1 = conjugate_verb(tr_v, a1["gender"], "fut")
        pl_v2 = conjugate_verb(v2, a1["gender"], "fut")
        pl = f"Jeśli {a1['nom']} {pl_v1} {obj['acc']}, to {pl_v2}."
        gy = f"ki {obj['gy']}s {a1['gy']}k {tr_v['gy']}dar xuen {a1['gy']}k {v2['gy']}dar."

    return pl, gy


def gen_modals_and_imperatives() -> Tuple[str, str]:
    """7. Czasowniki modalne (lio, ly, lyo, lya), przeczenia (gua) oraz rozkazy (li, lidi, ligi)."""
    actor = random.choice(ACTORS)
    obj = random.choice(OBJECTS)
    verb = random.choice(TRANSITIVE_VERBS)

    modals = [
        {"gy": "lio", "pl": "chce"},
        {"gy": "ly", "pl": "może"},
        {"gy": "lyo", "pl": "musi"},
        {"gy": "lya", "pl": "powinien" if actor["gender"] == "m" else "powinna"},
    ]

    if random.random() < 0.65:
        mod = random.choice(modals)
        neg = random.random() < 0.3
        if neg:
            pl = f"{actor['nom'].capitalize()} nie {mod['pl']} {verb['inf']} {obj['acc']}."
            gy = f"{obj['gy']}s {actor['gy']}k {verb['gy']}{mod['gy']}guar."
        else:
            pl = f"{actor['nom'].capitalize()} {mod['pl']} {verb['inf']} {obj['acc']}."
            gy = f"{obj['gy']}s {actor['gy']}k {verb['gy']}{mod['gy']}r."
    else:
        # Tryb rozkazujący / prośba (li, lidi, ligi)
        imp_type = random.choice(["li", "lidi", "ligi"])
        if imp_type == "li":
            pl = f"Niech {actor['nom']} {verb['pres']} {obj['acc']}."
            gy = f"{obj['gy']}s {actor['gy']}k {verb['gy']}lir."
        elif imp_type == "lidi":
            pl = f"Proszę, niech {actor['nom']} {verb['pres']} {obj['acc']}."
            gy = f"{obj['gy']}s {actor['gy']}k {verb['gy']}lidir."
        else:
            pl = f"Niech {actor['nom']} natychmiast {verb['pres']} {obj['acc']}!"
            gy = f"{obj['gy']}s {actor['gy']}k {verb['gy']}ligir."

    return pl, gy


def gen_participles() -> Tuple[str, str]:
    """8. Imiesłowowy równoważnik zdania (-f, -duaf) oraz imiesłowy (-rup, -pyp)."""
    actor = random.choice(ACTORS)
    obj = random.choice(OBJECTS)
    tr_verb = random.choice(TRANSITIVE_VERBS)

    if random.random() < 0.5:
        # Równoważnik uprzedni (-duaf): np. "Zobaczywszy konia, podszedł..."
        intr_verb = random.choice(INTRANSITIVE_VERBS)
        pl_v = conjugate_verb(intr_verb, actor["gender"], "past")
        pl = f"{tr_verb['perf_adv'].capitalize()} {obj['acc']}, {actor['nom']} {pl_v}."
        gy = f"{obj['gy']}{tr_verb['gy']}duaf {actor['gy']}k {intr_verb['gy']}duar."
    else:
        # Imiesłowy przymiotnikowe czynne (-rup) i bierne (-pyp)
        target = random.choice([a for a in ACTORS if a["gy"] == "cyeku" or a["gender"] == "m"])
        is_active = random.random() < 0.5
        if is_active:
            pl = f"{actor['nom'].capitalize()} widział {tr_verb['part_act_m']} {target['acc']}."
            gy = f"{tr_verb['gy']}rup {target['gy']}s {actor['gy']}k teduar."
        else:
            pl = f"{actor['nom'].capitalize()} widział {tr_verb['part_pass_m']} {target['acc']}."
            gy = f"{tr_verb['gy']}pyp {target['gy']}s {actor['gy']}k teduar."

    return pl, gy


def gen_questions_and_comparisons() -> Tuple[str, str]:
    """9. Pytania (di) oraz konstrukcje porównawcze (miemiar, mylur)."""
    if random.random() < 0.5:
        a1 = random.choice(ACTORS)
        a2 = random.choice([a for a in ACTORS if a["gy"] != a1["gy"]])
        if random.random() < 0.5:
            adj = "większa" if a1["gender"] == "f" else "większy"
            pl = f"{a1['nom'].capitalize()} jest {adj} od {a2['gen']}."
            gy = f"{a1['gy']}k {a2['gy']}p miemiar."
        else:
            adj = "tak samo duża" if a1["gender"] == "f" else "tak samo duży"
            pl = f"{a1['nom'].capitalize()} jest {adj} jak {a2['nom']}."
            gy = f"{a1['gy']}k {a2['gy']}p mylur."
    else:
        actor = random.choice(ACTORS)
        obj = random.choice(OBJECTS)
        verb = random.choice(TRANSITIVE_VERBS)
        q_type = random.choice(["who", "what", "where", "when"])
        if q_type == "who":
            pl = f"Kto {verb['past_m']} {obj['acc']}?"
            gy = f"{obj['gy']}s dikuk {verb['gy']}duar?"
        elif q_type == "what":
            pl = f"Co {conjugate_verb(verb, actor['gender'], 'past')} {actor['nom']}?"
            gy = f"diruas {actor['gy']}k {verb['gy']}duar?"
        elif q_type == "where":
            pl = f"Gdzie {actor['nom']} {conjugate_verb(verb, actor['gender'], 'past')} {obj['acc']}?"
            gy = f"dinun {obj['gy']}s {actor['gy']}k {verb['gy']}duar?"
        else:
            pl = f"Kiedy {actor['nom']} {conjugate_verb(verb, actor['gender'], 'past')} {obj['acc']}?"
            gy = f"didun {obj['gy']}s {actor['gy']}k {verb['gy']}duar?"

    return pl, gy


def gen_passive_reflexive_and_speaking() -> Tuple[str, str]:
    """10. Strona bierna (-s + -r), zwrotność (ti) oraz konstrukcja 'mówić o czymś'."""
    actor = random.choice(ACTORS)
    obj = random.choice(OBJECTS)
    mode = random.choice(["passive", "reflexive", "speaking"])

    if mode == "passive":
        pl = f"Ktoś niszczy {obj['acc']}."
        gy = f"{obj['gy']}s luar."
    elif mode == "reflexive":
        pl = f"{actor['nom'].capitalize()} myje się."
        gy = f"{actor['gy']}k titier."
    else:
        target = random.choice(ACTORS)
        topic = random.choice(OBJECTS)
        pl = f"{actor['nom'].capitalize()} mówi o {topic['nom']} {target['gen']}."
        gy = f"{target['gy']}p {topic['gy']}s {actor['gy']}k gyr."

    return pl, gy


# =====================================================================
# 4. EKSTRAKCJA SŁOWNIKA MORFEMÓW I LICZEBNIKÓW Z PLIKÓW JSON
# =====================================================================

def load_dictionary_drills(morphemes_path: Path, numbers_path: Path) -> List[Dict[str, str]]:
    """Tworzy pary treningowe bezpośrednio z plików morphemes.json oraz numbers.json."""
    drills = []

    if morphemes_path.exists():
        with open(morphemes_path, "r", encoding="utf-8") as f:
            morphemes = json.load(f)
        for item in morphemes:
            m = item.get("morfem", "")
            klasa = item.get("klasa", "")
            znaczenia = item.get("znaczenia_pl", [])
            if not m or not znaczenia:
                continue
            for zn in znaczenia:
                drills.append({"pl": zn, "gygy": m, "type": f"lexicon_{klasa}"})
                if klasa == "nomen" and not zn.startswith("być ") and not zn.startswith("czynić "):
                    drills.append({"pl": f"To jest {zn}.", "gygy": f"lk {m}lur.", "type": "lexicon_sentence"})

    if numbers_path.exists():
        with open(numbers_path, "r", encoding="utf-8") as f:
            numbers = json.load(f)
        for num in numbers:
            val = str(num["liczba"])
            nazwa = num["nazwa"]
            drills.append({"pl": val, "gygy": nazwa, "type": "number_raw"})
            # Zastosowanie z klasyfikatorem liczbowym 'mu' (Rozdział 3.11)
            actor = random.choice(ACTORS)
            drills.append({
                "pl": f"{val} ({actor['nom']})",
                "gygy": f"{nazwa}mu {actor['gy']}",
                "type": "number_classifier"
            })

    return drills


# =====================================================================
# 5. ZŁOTY ZBIÓR TESTOWY (Oryginalne zdania z podręcznika gygy.pdf)
# =====================================================================

GOLDEN_MANUAL_SENTENCES = [
    {"pl": "Człowiek jest.", "gygy": "kuk lur."},
    {"pl": "Zabójca tworzy kobietę.", "gygy": "kas luokuak lar."},
    {"pl": "Matka rodzi córkę.", "gygy": "kokas kuokak lolar."},
    {"pl": "Pradziadek umiera.", "gygy": "kuokuokuokuak luor."},
    {"pl": "Matka zabiła córkę.", "gygy": "kokas kuokak luoduar."},
    {"pl": "Dziadek skończył umierać.", "gygy": "kuokuokuak luoduoduar."},
    {"pl": "Żyjący człowiek jest biedny.", "gygy": "lop kuk puor."},
    {"pl": "Ojciec bogato obdarował syna.", "gygy": "kokuas lolakuak pop paduar."},
    {"pl": "Bogaty i śmiertelny dawca będzie miał bogatą córkę i bogatego syna.", "gygy": "pop kokaci pop kokuas poci luop pakuak pudar."},
    {"pl": "Pewien człowiek się pali.", "gygy": "kuck sior."},
    {"pl": "Topię się.", "gygy": "kiak syoluor."},
    {"pl": "Pada deszcz.", "gygy": "syosiar."},
    {"pl": "Mędrzec mówił o bogactwie dziadka i biedzie babci.", "gygy": "kuokuokuap poci kuokuokap puos giokuk gyduar."},
    {"pl": "Na początku było Słowo.", "gygy": "don gyk duar."},
    {"pl": "Szkoła została zbudowana na wodzie.", "gygy": "syonen giopanus nular."},
    {"pl": "W budynku lata dym.", "gygy": "nulan sioduasiak siar."},
    {"pl": "Uczę cię.", "gygy": "kyanion kiak giogypar."},
    {"pl": "Daję ci moje bogactwo.", "gygy": "kyanion kiap pos kiak par."},
    {"pl": "Każdy uczeń ma nauczyciela w szkole.", "gygy": "giopanun giopakus giopanukumik pur."},
    {"pl": "Uczeń dał mamie swoje błoto.", "gygy": "lolakanion kyp syosyas giopanukuk paduar."},
    {"pl": "On zawsze ma dużo bogactw.", "gygy": "dumin pomos kiok pur."},
    {"pl": "Córka bogacza płacze.", "gygy": "pokuap kokak cuasyor."},
    {"pl": "Nie ma klaunów wśród mędrców.", "gygy": "giokucian cokuk muer."},
    {"pl": "Kto umarł?", "gygy": "dikuk luoduar?"},
    {"pl": "Ono wolno szło.", "gygy": "kiok xuop xaduar."},
    {"pl": "On biegnie, żeby dojść do celu.", "gygy": "ki xenion xarp xen kiok xoxar."},
    {"pl": "Musisz zniszczyć swoje bogactwo.", "gygy": "tip pos kyak lualyor."},
    {"pl": "Niech Pani pije piwo.", "gygy": "fiotyas kyokak tyalir."},
    {"pl": "Kot śpi, po tym, gdy zjadł mięso.", "gygy": "ki sotias tiaduarp nuadun tiesok fyodupyr."},
    {"pl": "Kot, który zjadł mięso, śpi.", "gygy": "ki sotias hik tiaduarp tiesok fyodupyr."},
    {"pl": "Tygrys jest większy od lwa.", "gygy": "mietiesok piotiesop miemiar."},
    {"pl": "Ja jem i ty jesz.", "gygy": "kiak tiar ci kyak tiar."},
    {"pl": "Kocham cię, ale muszę odejść.", "gygy": "kyas kiak cior pi kiak nyoxalyor."},
    {"pl": "Jestem szczęśliwy, bo ty jesteś tutaj.", "gygy": "kiak cor le kyak nialur."},
    {"pl": "Nie mówisz prawdy, czyli kłamiesz.", "gygy": "kyak gogyguar ni kyak guogyr."},
    {"pl": "Wybaczę ci wtedy i tylko wtedy, gdy przeprosisz.", "gygy": "kyas kiak nioduor bi kyak guer."},
    {"pl": "Zobaczywszy konia, podszedłem do niego.", "gygy": "xosoteduaf kiak kionioxaduar."},
    {"pl": "Gdyby słońce nie świeciło, poleciałbym tam w nocy.", "gygy": "ki fiofiok fioguafirp xue ci fyodun kiak siaxafir."},
    {"pl": "Widzieliśmy zabijającego żołnierza.", "gygy": "luarup cyekus kiamok teduar."},
    {"pl": "Widzieliśmy zabijanego żołnierza.", "gygy": "luapyp cyekus kiamok teduar."},
    {"pl": "Matematyk czyta książkę.", "gygy": "gysues mukuk gysuer."},
    {"pl": "Książka jest czytana.", "gygy": "gysues gysuer."},
    {"pl": "Ja sam zbudowałem dom.", "gygy": "lonus kiatik nuladuar."},
]


# =====================================================================
# 6. GŁÓWNA PĘTLA GENERUJĄCA ZBIÓR TRENINGOWY I WALIDACYJNY
# =====================================================================

def build_datasets(num_synthetic: int = 5000):
    output_dir = Path("data")
    output_dir.mkdir(exist_ok=True)

    # 1. Zapis złotego zbioru testowego (z podręcznika)
    golden_path = Path("data/test_golden.jsonl")
    seen_gygy = set()
    if golden_path.exists():
        with open(golden_path, "r", encoding="utf-8") as f:
            for line in f:
                seen_gygy.add(json.loads(line)["gygy"].strip().lower())
    print(f"[✓] Zapisano {len(GOLDEN_MANUAL_SENTENCES)} zdań testowych z podręcznika do: {golden_path}")

    # 2. Generowanie wprawek słownikowych z morphemes.json i numbers.json
    dataset = load_dictionary_drills(Path("morphemes.json"), Path("numbers.json"))
    print(f"[✓] Wygenerowano {len(dataset)} wprawek leksykalno-liczbowych z plików JSON.")

    # 3. Generowanie zróżnicowanych zdań gramatycznych
    generators = [
        (gen_simple_sentences, "simple_aospv"),
        (gen_adverbial_and_dative, "adverbial_dative"),
        (gen_relative_clauses, "subordinate_relative_hi"),
        (gen_temporal_and_purpose_clauses, "subordinate_temporal_purpose"),
        (gen_coordinate_sentences, "coordinate_clauses"),
        (gen_conditionals_and_irrealis, "conditional_irrealis_fi"),
        (gen_modals_and_imperatives, "modals_imperatives"),
        (gen_participles, "participles_f_ru_py"),
        (gen_questions_and_comparisons, "questions_comparisons"),
        (gen_passive_reflexive_and_speaking, "passive_reflexive_speaking"),
    ]

    seen_gygy = {item["gygy"] for item in GOLDEN_MANUAL_SENTENCES}
    attempts = 0
    max_attempts = num_synthetic * 5

    while len(dataset) < num_synthetic and attempts < max_attempts:
        attempts += 1
        gen_func, struct_type = random.choice(generators)
        pl, gy = gen_func()

        # Wykluczamy duplikaty oraz zdania ze złotego zbioru testowego (Data Leakage Prevention)
        if gy not in seen_gygy:
            seen_gygy.add(gy)
            dataset.append({
                "pl": pl,
                "gygy": gy,
                "type": struct_type,
                # Format instrukcyjny gotowy pod Unsloth / HuggingFace SFTTrainer
                "instruction": "Przetłumacz poniższe zdanie z języka polskiego na język gygy, stosując szyk AOSPV oraz zasady gramatyczne gygy.",
                "input": pl,
                "output": gy
            })

    random.shuffle(dataset)
    train_path = output_dir / "train_synthetic.jsonl"
    with open(train_path, "w", encoding="utf-8") as f:
        for item in dataset:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"[✓] Zapisano łącznie {len(dataset)} unikalnych przykładów treningowych do: {train_path}")


if __name__ == "__main__":
    build_datasets(num_synthetic=5000)