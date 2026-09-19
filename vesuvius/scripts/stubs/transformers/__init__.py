"""Minimal local stub for transformers (offline env)."""
import torch.nn as nn

class PreTrainedModel(nn.Module):
    config_class = None
    base_model_prefix = ""
    def __init__(self, config=None):
        super().__init__()
        self.config = config
    @classmethod
    def register_for_auto_class(cls, *args, **kwargs):
        return cls

class PretrainedConfig:
    model_type = ""
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
    @classmethod
    def register_for_auto_class(cls, *args, **kwargs):
        return cls
