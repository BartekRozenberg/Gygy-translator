# Gygy-translator
Translator for a conlang gygy.


gygy-translator/
├── data/
│   ├── numbers.json             # Słownik liczb w języku gygy
│   ├── morphemes.json           # Twój ustrukturyzowany słownik 256 morfemów
│   ├── golden_dataset.jsonl     # Zbiór testowy do walidacji (50-100 par)
│   └── synthetic_train.jsonl    # Wygenerowane pary do fine-tuningu
├── gygy/
│   ├── __init__.py
│   ├── engine.py                # Wrapper na model LLM + prompt ze słownikiem
│   ├── postprocessor.py         # Sklejanie morfemów i czyszczenie tokenów
│   └── evaluator.py             # Automatyczny pomiar metryk BLEU / chrF
├── training/
│   └── finetune_lora.py         # Skrypt douczający model (np. Llama-3 / Mistral)
├── app.py                       # Interfejs Streamlit / Gradio (do Hugging Face)
├── cli.py                       # Interfejs terminalowy
├── requirements.txt
└── README.md                    # Dokumentacja języka, architektury i wykres metryk