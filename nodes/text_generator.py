import os
import sys
import importlib.util

from folder_paths import input_directory


class TextGenerator:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        generators_path = os.path.join(input_directory, 'text_generators')
        os.makedirs(generators_path, exist_ok=True)

        python_files = [f for f in os.listdir(generators_path) if f.split('.')[-1] == 'py' and os.path.isfile(os.path.join(generators_path, f))]

        return {
            'required': {
                'file': (python_files,),
                'seed': ('INT', {
                    'default': 0,
                    'min': 0,
                    'max': 2**64 - 1,
                    'step': 1
                })
            }
        }
    
    RETURN_TYPES = ('STRING', 'STRING')
    RETURN_NAMES = ('text1', 'text2')

    FUNCTION = 'generate_text'

    CATEGORY = "_topfun's Nodes"

    def generate_text(self, file, seed):
        scripts_directory = os.path.join(input_directory, 'text_generators')
        module_name = f'text_generators.{file.split(".")[:-1]}'

        spec = importlib.util.spec_from_file_location(module_name, os.path.join(scripts_directory, file))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        return module.generate(seed)