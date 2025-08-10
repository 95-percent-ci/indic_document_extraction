import albumentations as A
import cv2
import os

class ImageNoiseAddition():
    """This Class adds Noise at Image at 3 levels. Each level Progressive degrades quality of Input Image"""

    def __init__(self, img_path, degradation_level):
        self.path = img_path
        self.degradation_level = degradation_level
        
    def set_transform_params(self):
        params = {
            'low': {
                'brightness_contrast': {'brightness_limit': 0.1, 'contrast_limit': 0.1},
                'posterize': {'num_bits': 4},
                'affine': {'rotate': (-1, 1), 'scale': (0.95, 1.05), 'shear': (-1, 1)},
                'perspective': {'p': 0},  # Not applied
                'grid_distortion': {'distort_limit': 0.05},
                'gaussian_noise': {'p': 0},  # Not applied
                'image_compression': {'quality_range': (61, 99)},
                'blur': {'p': 0}  # Not applied
            },
            'medium': {
                'brightness_contrast': {'brightness_limit': 0.2, 'contrast_limit': 0.1},
                'posterize': {'num_bits': 3},
                'affine': {'rotate': (-3, 3), 'scale': (0.9, 1.1), 'shear': (-2, 2)},
                'perspective': {'scale': (0.02, 0.05)},
                'grid_distortion': {'distort_limit': 0.15},
                'gaussian_noise': {'p': 0},  # Not applied
                'image_compression': {'quality_range': (31, 60)},
                'blur': {'p': 0}  # Not applied
            },
            'high': {
                'brightness_contrast': {'brightness_limit': 0.2, 'contrast_limit': 0.2},
                'posterize': {'num_bits': 3},
                'affine': {'rotate': (-4, 4), 'scale': (0.8, 1.2), 'shear': (-3, 3)},
                'perspective': {'scale': (0.02, 0.05)},
                'grid_distortion': {'distort_limit': 0.25},
                'gaussian_noise': {'std_range': (5/255, 10/255)},
                'image_compression': {'quality_range': (31, 60)},
                'blur': {'blur_limit': 3}
            }
        }
        return params[self.degradation_level]
    
    def get_transform(self):
        """Create Albumentations transform based on degradation level"""
        params = self.set_transform_params()
        
        transform = A.ReplayCompose([
            A.RandomBrightnessContrast(
                brightness_limit=params['brightness_contrast']['brightness_limit'],
                contrast_limit=params['brightness_contrast']['contrast_limit'],
                p=1
            ),
            A.Posterize(
                num_bits=params['posterize']['num_bits'],
                p=1
            ),
            A.Affine(
                rotate=params['affine']['rotate'],
                scale=params['affine']['scale'],
                shear=params['affine']['shear'],
                p=1,
                fit_output=True
            ),
            A.Perspective(
                scale=params['perspective'].get('scale', (0, 0)),
                keep_size=True,
                fit_output=True,
                p=params['perspective'].get('p', 1)
            ),
            A.GridDistortion(
                num_steps=5,
                distort_limit=params['grid_distortion']['distort_limit'],
                p=1
            ),
            A.GaussNoise(
                std_range=params['gaussian_noise'].get('std_range', (0, 0)),
                p=params['gaussian_noise'].get('p', 1)
            ),
            A.ImageCompression(
                quality_range=params['image_compression']['quality_range'],
                p=1
            ),
            A.Blur(
                blur_limit=params['blur'].get('blur_limit', 0),
                p=params['blur'].get('p', 1)
            )
        ])
        
        return transform
    
    def apply_transform(self):
        """Apply Transform"""
        image_load = cv2.imread(self.path)
        transforms = self.get_transform()

        image_augmented = transforms(image = image_load)['image']
        image_augmented = cv2.cvtColor(image_augmented, cv2.COLOR_BGR2RGB)
        return image_augmented

    def save_transformed_image(self, output_folder):
        """Write Transformed Image Back"""
        ## augmented_image
        augmented_image = self.apply_transform()
        cv2.imwrite(os.path.join(output_folder, os.path.basename(self.path)), augmented_image)