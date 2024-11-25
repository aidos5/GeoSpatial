from transformers import pipeline

# Load Hugging Face NER pipeline
ner_pipeline = pipeline("ner", model="dslim/bert-base-NER")

# Input text


def ner_hugging_face(text):
    entities = ner_pipeline(text)
    print("NER Results:", entities)

    # Reconstruct subword tokens
    place_candidates = []
    current_entity = ""
    for ent in entities:
        if ent['entity'].startswith("B-"):  # Start of a new entity
            if current_entity:
                place_candidates.append(current_entity)
            current_entity = ent['word'].replace("##", "")
        elif ent['entity'].startswith("I-"):  # Continuation of the same entity
            current_entity += ent['word'].replace("##", "")
    if current_entity:  # Add the last entity
        place_candidates.append(current_entity)

    return(place_candidates)
