import logging
from functools import lru_cache
from typing import Optional
import threading
import torch
from transformers import (
    AutoModelForSequenceClassification,
    AutoTokenizer,
    PreTrainedModel,
    PreTrainedTokenizerBase,
)
from peft import PeftModel, PeftConfig

from backend import BASE_MODEL_PATH
import warnings
warnings.filterwarnings("ignore")

logger = logging.getLogger(__name__)

id2label = {0: "positive", 1: "neutral", 2: "negative"}
CATEGORIES = {
    "positive": "resolved",
    "neutral": "basic",
    "negative": "complaint",
}
PRIORITIES = {
    "resolved": "low",
    "basic": "medium",
    "complaint": "high",
}


class ModelService:

    def __init__(
        self,
        adapter_path: str = BASE_MODEL_PATH,
        num_labels: int = 3,
        device: Optional[str] = None,
        local_files_only: bool = True,
    ) -> None:
        self.adapter_path = adapter_path
        self.num_labels = num_labels
        self.local_files_only = local_files_only
        self.device = torch.device(device or self._select_device())

        self.tokenizer: PreTrainedTokenizerBase = self._load_tokenizer()
        self.model: PreTrainedModel = self._load_model()
        self._thread_lock = threading.Lock()

    @staticmethod
    def _select_device() -> str:
        if torch.backends.mps.is_available():
            return "mps"  # mac
        if torch.cuda.is_available():
            return "cuda"  # nvidia gpu
        return "cpu"

    def _load_tokenizer(self) -> PreTrainedTokenizerBase:
        return AutoTokenizer.from_pretrained(
            self.adapter_path,
            local_files_only=self.local_files_only,
        )

    def _load_model(self) -> PreTrainedModel:
        peft_config = PeftConfig.from_pretrained(self.adapter_path)
        base_model_name = peft_config.base_model_name_or_path

        base_model = AutoModelForSequenceClassification.from_pretrained(
            base_model_name,
            num_labels=self.num_labels,
        )
        model = PeftModel.from_pretrained(base_model, self.adapter_path)
        model.to(self.device)
        model.eval()
        return model

    @torch.no_grad()
    def warmup(self, num_iterations: int = 2, max_length: int = 64) -> None:
        dummy_inputs = self.tokenizer(
            "warmup",
            return_tensors="pt",
            padding="max_length",
            truncation=True,
            max_length=max_length,
        ).to(self.device)

        for _ in range(num_iterations):
            self.model(**dummy_inputs)

    @torch.no_grad()
    def request(self, text: str):
        with self._thread_lock:
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True).to(self.device)
            logits = self.model(**inputs).logits

            probs = torch.softmax(logits, dim=-1).squeeze().tolist()
            probabilities = {id2label[i]: v for i, v in enumerate(probs)}
            pred_class = max(probabilities, key=probabilities.get)
            confidence = probabilities[pred_class]

            category = CATEGORIES[pred_class]
            priority = PRIORITIES[category]
            return {
                "category": category,
                "priority": priority,
                "probabilities": probabilities,
                "confidence": confidence,
            }


@lru_cache(maxsize=1)
def load_model() -> ModelService:
    """
    Загрузка и прогрев модели.
    """
    model = ModelService()
    model.warmup()
    return model