import os
import json
from app.utils.text_utils import normalize
from app.core.config import DATASET_DIR


def build_documents_per_ayat(record):

    docs = []

    sumber = record.get("sumber", "")
    bab = record.get("bab", "")
    pasal = record.get("pasal", "")

    if "isi" in record:

        isi_text = []

        for item in record["isi"]:
            isi_text.append(item.get("isi", ""))

        doc = f"""
Sumber: {sumber}
Bab: {bab}
Pasal: {pasal}

Isi:
{" ".join(isi_text)}
"""
        docs.append(doc)

    if "ayat" in record:

        for ayat in record["ayat"]:

            nomor = ayat.get("nomor", "")
            isi_ayat = ayat.get("isi", "")

            isi_text = [isi_ayat]

            if "huruf" in ayat:

                for huruf in ayat["huruf"]:

                    isi_text.append(
                        f"Huruf ({huruf.get('kode','')}) {huruf.get('isi','')}"
                    )

            doc = f"""
Sumber: {sumber}
Bab: {bab}
Pasal: {pasal}
Ayat: ({nomor})

Isi:
{" ".join(isi_text)}
"""
            docs.append(doc)

    return docs


def load_documents():

    raw_docs = []
    documents = []

    for filename in os.listdir(DATASET_DIR):

        if filename.endswith(".json"):

            path = os.path.join(DATASET_DIR, filename)

            with open(path, "r", encoding="utf-8") as f:

                data = json.load(f)

                for record in data:

                    docs = build_documents_per_ayat(record)

                    for doc in docs:

                        raw_docs.append(doc)
                        documents.append(normalize(doc))

    return raw_docs, documents
