import json
from pathlib import Path
from typing import List

class PairsConfig:
    def __init__(self, config_path: str = 'data/pairs.json'):
        self.config_path = Path(config_path)
        if not self.config_path.exists():
            self._save_pairs([])  # создаем пустой файл при отсутствии

    def _load_pairs(self) -> List[str]:
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                pairs = json.load(f)
                if isinstance(pairs, list):
                    return pairs
                return []
        except Exception:
            return []

    def _save_pairs(self, pairs: List[str]) -> None:
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(pairs, f, ensure_ascii=False, indent=2)

    def get_pairs(self) -> List[str]:
        return self._load_pairs()

    def add_pair(self, pair: str) -> bool:
        pairs = self._load_pairs()
        if pair not in pairs:
            pairs.append(pair)
            self._save_pairs(pairs)
            return True
        return False

    def remove_pair(self, pair: str) -> bool:
        pairs = self._load_pairs()
        if pair in pairs:
            pairs.remove(pair)
            self._save_pairs(pairs)
            return True
        return False