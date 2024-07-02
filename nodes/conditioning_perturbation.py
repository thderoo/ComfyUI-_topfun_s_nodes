import torch

class ConditioningPerturbation:
    def _init_():
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            'required': {
                'conditioning': ('CONDITIONING',),
                'strength': ('FLOAT', {
                    'default': 0.1,
                    'min': 0.0,
                    'step': 0.001,
                    'display': 'number'
                }),
                'seed': ('INT', {
                    'default': 0,
                    'min': 0,
                    'max': 2**64 - 1,
                    'step': 1
                })
            }
        }
    
    RETURN_TYPES = ('CONDITIONING',)

    FUNCTION = 'conditioning_perturbation'

    CATEGORY = '_topfun'

    def conditioning_perturbation(self, conditioning, strength, seed):
        device = conditioning[0][0].device

        generator = torch.Generator(device=device)
        generator.manual_seed(seed)

        output = []

        for c in conditioning:
            if c[0].shape[2] == 2048:
                noise1 = torch.randn([c[0].shape[0], c[0].shape[1], 1280], generator=generator, device=device)
                noise1 /= torch.norm(noise1, dim=2, keepdim=True)

                noise2 = torch.randn([c[0].shape[0], c[0].shape[1], 768], generator=generator, device=device)
                noise2 /= torch.norm(noise1, dim=2, keepdim=True)

                norms1 = torch.norm(c[0][:, :, :1280], dim=2, keepdim=True)
                norms2 = torch.norm(c[0][:, :, 1280:], dim=2, keepdim=True)

                cond = torch.clone(c[0])
                cond[:, :, :1280] = strength * norms1 * noise1 + (1 - strength) * c[0][:, :, :1280]
                cond[:, :, 1280:] = strength * norms2 * noise2 + (1 - strength) * c[0][:, :, 1280:]
            else:
                noise = torch.randn(c[0].shape, generator=generator, device=device)
                noise /= torch.norm(noise, dim=2, keepdim=True)
            
                norms = torch.norm(c[0], dim=2, keepdim=True)

                cond = strength * norms * noise + (1 - strength) * c[0]

            output.append([cond, c[1].copy()])

        return (output,)