from .nodes.conditioning_perturbation import ConditioningPerturbation
from .nodes.text_generator import TextGenerator

NODE_CLASS_MAPPINGS = {
    'ConditioningPerturbation': ConditioningPerturbation,
    'TextGenerator': TextGenerator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    'ConditioningPerturbation': 'Conditioning Perturbation',
    'TextGenerator': 'Text Generator'
}
