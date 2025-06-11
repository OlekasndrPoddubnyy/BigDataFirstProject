# main.py

import os
from config.settings import TEST_APP
from nlp.registry import parse_question
from core.query_builder import build_static_job, build_dynamic_job
from core.executor import execute_code
from client.interface import prompt_test_questions, print_intro

def main():
    print_intro(TEST_APP)

    if TEST_APP:
        for question in prompt_test_questions():
            print(f"\nDomanda: {question}")
            intent = parse_question(question)
            print(f"[Intent riconosciuto] ➜ {intent}")

            code = build_static_job(intent)
            print("[Codice generato]")
            print(code)

            result = execute_code(code)
            if result is not None:
                result.show()
            else:
                print("⚠️ Nessun risultato disponibile.")
    else:
        # Modalità shell interattiva
        while True:
            question = input("> ").strip()
            if question.lower() in {"exit", "quit"}:
                break

            intent = parse_question(question)
            print(f"[Intent riconosciuto] ➜ {intent}")

            code = build_dynamic_job(intent)
            print("[Codice generato]")
            clean_code = strip_markdown(code)
            print(clean_code)

            result = execute_code(clean_code)
            if result is None:
                print("⚠️ Nessun risultato disponibile.")
                continue

            # ⬇️ LOOP sulla risposta per la stessa domanda
            while True:
                print("\nVuoi una risposta:")
                print("1 ➜ semplice (tabella)")
                print("2 ➜ elaborata (testuale con AI)")
                choice = input("Scelta (1/2): ").strip()

                if choice == "1":
                    result.show()
                elif choice == "2":
                    try:
                        import pandas as pd
                        from openai import OpenAI
                        from config.settings import OPENAI_API_KEY

                        client = OpenAI(api_key=OPENAI_API_KEY)

                        df = result.limit(5).toPandas()
                        records = df.to_dict(orient="records")

                        prompt = f"""
                    Domanda dell'utente:
                    \"{question}\"

                    Risultato Spark (prime 5 righe):
                    {records}

                    Fornisci una spiegazione chiara, in linguaggio naturale, di questo risultato. 
                    Sii sintetico ma comprensibile anche per chi non è esperto tecnico.
                    """

                        response = client.chat.completions.create(
                            model="gpt-4o",
                            messages=[
                                {
                                    "role": "system",
                                    "content": (
                                        "Sei un assistente esperto che aiuta a comprendere i risultati di analisi dati "
                                        "basati su Spark. Spiega i risultati in modo semplice, evitando termini tecnici complessi."
                                    )
                                },
                                {
                                    "role": "user",
                                    "content": prompt
                                }
                            ],
                            temperature=0.5
                        )

                        print("\n📢 Risposta AI:\n" + response.choices[0].message.content)

                    except Exception as e:
                        print(f"[AI] Errore durante la risposta elaborata: {e}")
                else:
                    print("Scelta non valida. Inserisci 1 o 2.")
                    continue

                retry = input("\nVuoi rivedere la risposta (rivedi) o fare una nuova domanda (nuova)? ").strip().lower()
                if retry == "rivedi":
                    continue
                elif retry == "nuova":
                    break
                else:
                    print("Scelta non valida, torno alla shell.")
                    break


def strip_markdown(code: str) -> str:
    return code.replace("```python", "").replace("```", "").strip()


if __name__ == "__main__":
    main()

