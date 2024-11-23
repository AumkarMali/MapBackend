# Import necessary libraries
from fastai.vision.all import *
import os


# Define function to prepare data, train, and export model
def train_and_export_model():
    # Define path to your image folder
    path = Path('earthquake_images')  # Replace with the path to your images folder

    # Assume your images are in folders with the class labels as folder names
    # Create a DataBlock for image classification
    dblock = DataBlock(
        blocks=(ImageBlock, CategoryBlock),  # Input is an image, output is a category
        get_items=get_image_files,  # Get image files
        splitter=RandomSplitter(valid_pct=0.2, seed=42),  # 80% train, 20% validation
        get_y=parent_label,  # Labels are the parent folder names
        item_tfms=Resize(224),  # Resize images to 224x224 for the model
        batch_tfms=aug_transforms(mult=2)  # Data augmentation for training
    )

    # Load data
    dls = dblock.dataloaders(path, bs=8)  # Adjust batch size as needed

    # Create a CNN learner using resnet34 as the architecture
    learn = cnn_learner(dls, resnet34, metrics=accuracy)

    # Train the model (fine-tune for 5 epochs)
    learn.fine_tune(5)

    # Export the model to a .pkl file
    learn.export('earthquake_model.pkl')
    print("Model exported successfully!")


# Train the model and export it
if __name__ == '__main__':
    train_and_export_model()
