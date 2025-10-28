from utils.load_bytes import load_bytes


def get_rubrica(workshop_id: str) -> str:
    blob_name = f"{workshop_id}.txt"
    rubrica_bytes = load_bytes("rubicas", blob_name)
    return rubrica_bytes.decode('utf-8')
