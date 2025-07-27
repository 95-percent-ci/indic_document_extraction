import albumentations as A
import cv2
import os

def augment_image(image, output_directory):
    """
    Augments the image to simulate real world scenarios
    """
    image_path = image
    image = cv2.imread(image)
    transform = A.ReplayCompose([
        A.RandomBrightnessContrast(brightness_limit = 0.2,
                                    contrast_limit = 0.2,
                                    p = 1), # adjust brightness and contrast
        A.Posterize(num_bits = 3,
                     p=1), # number of colors bits are reduced to similate printing / scanning
        A.Affine(
            rotate = (-4, 4), # rotate by -2 to 2 degrees
            scale = (0.8, 1.2), # zoom in or out by 5%
            shear = (-3, 3), # shear by -1 to 1 degrees
            p = 1,
            fit_output=True
        ),
        A.Perspective(scale = (0.02, 0.05),
                    keep_size = True,
                    fit_output=True,
                    p = 1), # simulate perspective distortion
        A.GridDistortion(num_steps = 5,
                        distort_limit =  0.25, 
                        p = 1), # grid like distortion to simulate uneven surfaces
        A.GaussNoise(std_range = (1/255, 2/255),
                     p = 1), # add gaussian noise to simulate low quality images
        A.ImageCompression(quality_range= (90,99)
                           , p=1), # compress the image to simulate low quality images
        A.Blur(blur_limit = 3,
               p = 0) # blurring to simulate low quality images
    ])

    # Apply the augmentations
    augmented = transform(image = image)
    augmented_image = augmented['image']

    # BGR to RGB and save
    augmented_image = cv2.cvtColor(augmented_image, cv2.COLOR_BGR2RGB)
    cv2.imwrite(os.path.join(output_directory, os.path.basename(image_path)), augmented_image)