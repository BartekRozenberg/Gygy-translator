import json
import os
import re
import time
from collections import defaultdict
from pathlib import Path
from openai import OpenAI
import sacrebleu
from tqdm import tqdm

# =====================================================================
# 1. KONFIGURACJA POŁĄCZENIA (GROQ API LUB LOKALNA OLLAMA)
# =====================================================================

# Ustaw zmienną środowiskową GROQ_API_KEY
API_KEY = os.environ.get("GROQ_API_KEY")

# Konfiguracja dla darmowego API Groq:
BASE_URL = "https://api.groq.com/openai/v1"
MODEL_NAME = "qwen/qwen3.8-27b"

# (Opcjonalnie) Jeśli używasz lokalnej Ollamy, odkomentuj poniższe 3 linie:
# API_KEY = "ollama"
# BASE_URL = "http://localhost:11434/v1"
# MODEL_NAME = "llama3.1:8b"


# =====================================================================
# 2. BUDOWANIE PROMPTU SYSTEMOWEGO ZE SŁOWNIKIEM I GRAMATYKĄ GYGY
# =====================================================================

def build_system_prompt(morphemes_path: Path, numbers_path: Path) -> str:
    """Tworzy kompletny prompt systemowy ze słownikiem JSON i regułami gramatyki gygy."""
    with open(morphemes_path, "r", encoding="utf-8") as f:
        morphemes = json.load(f)

    # Kompresja słownika, aby oszczędzać tokeny i zwiększyć czytelność dla modelu
    functio_lines = []
    nomen_lines = []
    for m in morphemes:
        morf = m.get("morfem", "")
        znaczenia = ", ".join(m.get("znaczenia_pl", []))
        if not morf or not znaczenia:
            continue
        if m.get("klasa") == "functio":
            functio_lines.append(f"- -{morf} / {morf}: {znaczenia}")
        else:
            nomen_lines.append(f"- {morf}: {znaczenia}")

    numbers_info = ""
    if numbers_path.exists():
        with open(numbers_path, "r", encoding="utf-8") as f:
            nums = json.load(f)[:20]  # Pierwsze 20 liczb jako wzorzec
        numbers_info = ", ".join([f"{n['liczba']}={n['nazwa']}" for n in nums])

    prompt = f"""Jesteś ekspertem i natywnym tłumaczem sztucznego języka 'gygy'.
Twoim zadaniem jest przetłumaczenie podanego zdania z języka polskiego na język gygy.

### ZASADY GRAMATYKI JĘZYKA GYGY:
1. BRAK ODMIANY I CZĘŚCI MOWY: W gygy dzielimy morfemy tylko na 'nomina' (rzeczy/pojęcia/czynności) oraz 'functiones' (morfemy strukturalne). Nie ma różnicy między rzeczownikiem, czasownikiem a przymiotnikiem – o roli słowa decyduje morfem strukturalny na końcu wyrazu.
2. ZASADA "NAJWAŻNIEJSZE Z TYŁU" (SZYK ZDANIA AOSPV):
   Kolejność części zdania jest ściśle określona:
   [Okolicznik (-n)] + [Dopełnienie bliższe (-s)] + [Podmiot (-k)] + [Orzeczenie (-r)].
   Przykład: "Zabójca tworzy kobietę" -> kobieta-s zabójca-k tworzyć-r -> "kas luokuak lar."
3. SŁOWOTWÓRSTWO (ZŁOŻENIA):
   W wyrazach złożonych człon określający stoi PRZED członem określanym (rdzeń główny zawsze na końcu).
   Przykład: "luo" (śmierć/zabijać) + "kua" (mężczyzna) = "luokua" (zabójca).
   Przykład: "sio" (ogień) + "tia" (jedzenie) + "nu" (miejsce) = "siotianu" (kuchnia).
4. NAJWAŻNIEJSZE MORFEMY STRUKTURALNE (FUNCTIONES):
   - '-k': oznacza koniec podmiotu (wykonawcy czynności, agensa), np. "kuk" (człowiek jako podmiot).
   - '-s': oznacza koniec dopełnienia bliższego (pacjensa), np. "kas" (kobietę jako dopełnienie). Brak '-k' przy obecnym '-s' tworzy stronę bierną (np. "kuas luar." = Mężczyzna jest niszczony).
   - '-r': oznacza koniec orzeczenia (czasownika) i koniec zdania, np. "lur." (jest), "lar." (tworzy).
   - '-n': oznacza koniec okolicznika (miejsca, czasu) oraz dopełnienia dalszego.
   - '-nio' + '-n' ('-nion'): dopełnienie dalsze (komu? czemu? do kogo?), np. "kyanion" (tobie / do ciebie).
   - '-p': tworzy przymiotnik, przydawkę dzierżawczą lub przysłówek (to, co stoi przed '-p', określa słowo za nim), np. "riop ku" (dobry człowiek), "kiap lonu" (mój dom).
   - 'ci': spójnik "i / oraz" (łączy wyrazy, przydawki i zdania).
   - 'ki ... rp': nawias otwierający ('ki') i zamykający ('rp' po orzeczeniu) zdanie podrzędne.
   - 'hi' ('hik', 'his'): zaimek względny "który" wewnątrz zdania podrzędnego, odnoszący się do słowa stojącego bezpośrednio po 'rp'. Przykład: "ki sotias hik tiaduarp tiesok fyodupyr." (Kot, który zjadł mięso, śpi).
   - 'dua' (przed -r): czas przeszły (np. "luoduar" = umarł).
   - 'da' (przed -r): czas przyszły (np. "luodar" = umrze).
   - 'gua' (przed -r): negacja "nie" (np. "luguaduar" = nie był).
   - 'li' / 'lidi' / 'ligi' (przed -r): tryb rozkazujący / prośba ("niech").
   - 'fi' (przed -r): tryb przypuszczający (modus irrealis, "gdyby / -by").
   - 'ti': zaimek zwrotny "się / sam" (np. "kiak titier." = Ja myję się).
   - 'di': zaimek pytajny wstawiany w miejsce części zdania, o którą pytamy (np. "dikuk" = kto?, "diruas" = co?, "dinun" = gdzie?, "didun" = kiedy?).
   - '-m' oraz klasyfikator 'mu': liczebniki kończą się na '-m', a przed rzeczownikiem przyjmują klasyfikator 'mu' (np. "cummu ku" = jeden człowiek). Podstawowe liczby: {numbers_info}.

### LISTA MORFEMÓW STRUKTURALNYCH (FUNCTIONES):
{chr(10).join(functio_lines)}

### SŁOWNIK MORFEMÓW RDZENIOWYCH (NOMINA):
{chr(10).join(nomen_lines)}

### PRZYKŁADY TŁUMACZEŃ (FEW-SHOT):
PL: Kobieta widzi duży dom.
GYGY: miep lonus kak ter.

PL: Wczoraj uczeń dał nauczycielowi książkę w szkole.
GYGY: duafiodu ci giopakunion ci giopanun gysues giopanukuk paduar.

PL: Człowiek, który zbudował dom, śpi.
GYGY: ki lonus hik nuladuarp kuk fyodupyr.

PL: Gdyby on przyszedł, byłbym szczęśliwy.
GYGY: ki kiok nioxafirp xue ci kiak cofir.

INSTRUKCJA KOŃCOWA:
Zwróć WYŁĄCZNIE przetłumaczone zdanie w języku gygy. Nie dodawaj żadnych wyjaśnień, komentarzy, cudzysłowów ani analizy krok po kroku."""

    return prompt


# =====================================================================
# 3. FUNKCJE CZYSZCZĄCE I LICZĄCE METRYKI (BLEU, chrF, Exact Match)
# =====================================================================

def normalize_text(text: str) -> str:
    """Ujednolica tekst do porównania (małe litery, pojedyncze spacje)."""
    text = text.strip().lower()
    # Jeśli model mimo zakazu dodał np. "GYGY: ...", usuwamy prefiks
    text = re.sub(r"^(gygy\s*:\s*)", "", text)
    text = text.splitlines()[0].strip()
    text = re.sub(r"\s+", " ", text)
    return text


def compute_metrics(predictions: list[str], references: list[str]) -> dict:
    """Oblicza metryki BLEU, chrF2 oraz Exact Match dla listy zdań."""
    norm_preds = [normalize_text(p) for p in predictions]
    norm_refs = [normalize_text(r) for r in references]

    # Obliczanie BLEU i chrF2 za pomocą biblioteki sacrebleu
    bleu = sacrebleu.corpus_bleu(norm_preds, [norm_refs]).score
    chrf = sacrebleu.corpus_chrf(norm_preds, [norm_refs]).score

    # Exact Match (bez kropek i znaków interpunkcyjnych na końcu)
    strip_punct = lambda s: re.sub(r"[.!?,:;]+$", "", s).strip()
    exact_matches = sum(
        1 for p, r in zip(norm_preds, norm_refs) if strip_punct(p) == strip_punct(r)
    )
    em_score = (exact_matches / len(norm_refs)) * 100.0 if norm_refs else 0.0

    return {
        "count": len(norm_refs),
        "chrF2": round(chrf, 2),
        "BLEU": round(bleu, 2),
        "Exact_Match_%": round(em_score, 2),
    }


# =====================================================================
# 4. GŁÓWNA PĘTLA EWALUACJI Z OBSŁUGĄ LIMITÓW API I WZNAWIANIEM
# =====================================================================

def run_baseline_evaluation():
    morphemes_path = Path("morphemes.json")
    numbers_path = Path("numbers.json")
    golden_path = Path("data/test_golden.jsonl")
    preds_path = Path("data/baseline_predictions.jsonl")
    report_path = Path("data/baseline_report.json")

    if not golden_path.exists():
        raise FileNotFoundError(
            f"Nie znaleziono pliku {golden_path}! Uruchom najpierw build_golden_dataset.py."
        )

    system_prompt = build_system_prompt(morphemes_path, numbers_path)
    print(f"[i] Zbudowano System Prompt (długość: {len(system_prompt)} znaków).")

    # Wczytanie złotego zbioru testowego
    golden_data = []
    with open(golden_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                golden_data.append(json.loads(line))

    # Sprawdzenie wcześniej przetłumaczonych zdań (Checkpointing)
    completed = {}
    if preds_path.exists():
        with open(preds_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    rec = json.loads(line)
                    completed[rec["pl"]] = rec["pred_gygy"]
        print(f"[i] Znaleziono {len(completed)} wcześniej przetłumaczonych zdań. Wznawiam...")

    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

    results = []
    with open(preds_path, "a", encoding="utf-8") as out_f:
        for item in tqdm(golden_data, desc="Tłumaczenie zbioru testowego"):
            pl_text = item["pl"]
            ref_gygy = item["gygy"]
            category = item.get("category", "ogolne")

            if pl_text in completed:
                pred_gygy = completed[pl_text]
            else:
                # Pętla ponawiania na wypadek przekroczenia darmowego limitu zapytań na minutę (Rate Limit 429)
                for attempt in range(5):
                    try:
                        response = client.chat.completions.create(
                            model=MODEL_NAME,
                            messages=[
                                {"role": "system", "content": system_prompt},
                                {"role": "user", "content": pl_text},
                            ],
                            temperature=0.0,  # Temperatura 0 zapewnia powtarzalność (deterministyczność)
                            max_tokens=150,
                        )
                        pred_gygy = response.choices[0].message.content.strip()
                        break
                    except Exception as e:
                        wait_time = 5 * (attempt + 1)
                        print(f"\n[!] Limit API lub błąd połączenia: {e}. Czekam {wait_time}s...")
                        time.sleep(wait_time)
                else:
                    pred_gygy = "BŁĄD_API"

                # Zapis na bieżąco do pliku
                record = {
                    "category": category,
                    "pl": pl_text,
                    "ref_gygy": ref_gygy,
                    "pred_gygy": pred_gygy,
                }
                out_f.write(json.dumps(record, ensure_ascii=False) + "\n")
                out_f.flush()

                # Krótka pauza dla darmowego planu Groq (30 zapytań / minutę)
                if "groq.com" in BASE_URL:
                    time.sleep(2.1)

            results.append({
                "category": category,
                "pl": pl_text,
                "ref_gygy": ref_gygy,
                "pred_gygy": pred_gygy,
            })

    # Obliczanie wyników całościowych i dla poszczególnych kategorii
    all_preds = [r["pred_gygy"] for r in results]
    all_refs = [r["ref_gygy"] for r in results]
    overall_metrics = compute_metrics(all_preds, all_refs)

    by_category = defaultdict(lambda: {"preds": [], "refs": []})
    for r in results:
        by_category[r["category"]]["preds"].append(r["pred_gygy"])
        by_category[r["category"]]["refs"].append(r["ref_gygy"])

    category_metrics = {
        cat: compute_metrics(data["preds"], data["refs"])
        for cat, data in by_category.items()
    }

    full_report = {
        "model": MODEL_NAME,
        "method": "Baseline (In-Context Prompt + Dictionary)",
        "overall": overall_metrics,
        "categories": category_metrics,
    }

    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(full_report, f, indent=4, ensure_ascii=False)

    # Wyświetlenie tabeli podsumowującej w terminalu
    print("\n" + "=" * 68)
    print(f" WYNIKI BASELINE DLA MODELU: {MODEL_NAME}")
    print("=" * 68)
    print(f"{'Kategoria':<24} | {'Zdań':>5} | {'chrF2':>8} | {'BLEU':>8} | {'Exact Match':>12}")
    print("-" * 68)
    for cat, m in category_metrics.items():
        print(f"{cat:<24} | {m['count']:>5} | {m['chrF2']:>8.2f} | {m['BLEU']:>8.2f} | {m['Exact_Match_%']:>11.2f}%")
    print("-" * 68)
    print(f"{'OGÓŁEM (OVERALL)':<24} | {overall_metrics['count']:>5} | {overall_metrics['chrF2']:>8.2f} | {overall_metrics['BLEU']:>8.2f} | {overall_metrics['Exact_Match_%']:>11.2f}%")
    print("=" * 68)
    print(f"[✓] Pełny raport zapisano w: {report_path}")
    print(f"[✓] Wszystkie tłumaczenia modelu zapisano w: {preds_path}")


if __name__ == "__main__":
    run_baseline_evaluation()