import os
import torch
import torch.nn as nn
import torch.optim as optim

from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from tqdm import tqdm


# -----------------------------
# Configuration
# -----------------------------

TRAIN_DIR = "data/plant_disease/dataset/train"
VALID_DIR = "data/plant_disease/dataset/valid"

BATCH_SIZE = 16
EPOCHS = 15
IMAGE_SIZE = 128
LR = 0.001

CHECKPOINT_PATH = "ml_models/disease_checkpoint.pth"
FINAL_MODEL_PATH = "ml_models/disease_model.pth"


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print("Using device:", device)


# -----------------------------
# Image Transformations
# -----------------------------

transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor()
])


# -----------------------------
# Dataset Loading
# -----------------------------

train_dataset = datasets.ImageFolder(TRAIN_DIR, transform=transform)
valid_dataset = datasets.ImageFolder(VALID_DIR, transform=transform)

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=0)
valid_loader = DataLoader(valid_dataset, batch_size=BATCH_SIZE, num_workers=0)

num_classes = len(train_dataset.classes)

print("Number of classes:", num_classes)
print("Classes:", train_dataset.classes)


# -----------------------------
# CNN Model
# -----------------------------

class PlantDiseaseCNN(nn.Module):

    def __init__(self, num_classes):
        super().__init__()

        self.conv = nn.Sequential(

            nn.Conv2d(3, 32, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(32, 64, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),

            nn.Conv2d(64, 128, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2)

        )

        self.fc = nn.Sequential(

            nn.Flatten(),
            nn.Linear(128 * 16 * 16, 512),
            nn.ReLU(),
            nn.Dropout(0.5),

            nn.Linear(512, num_classes)

        )

    def forward(self, x):

        x = self.conv(x)
        x = self.fc(x)

        return x


model = PlantDiseaseCNN(num_classes).to(device)


# -----------------------------
# Loss and Optimizer
# -----------------------------

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=LR)


# -----------------------------
# Resume Training
# -----------------------------

start_epoch = 0

if os.path.exists(CHECKPOINT_PATH):

    checkpoint = torch.load(CHECKPOINT_PATH)

    model.load_state_dict(checkpoint["model"])
    optimizer.load_state_dict(checkpoint["optimizer"])
    start_epoch = checkpoint["epoch"] + 1

    print("Resuming training from epoch", start_epoch)


# -----------------------------
# Training Loop
# -----------------------------

for epoch in range(start_epoch, EPOCHS):

    model.train()
    running_loss = 0

    loop = tqdm(train_loader)

    for images, labels in loop:

        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(outputs, labels)

        loss.backward()

        optimizer.step()

        running_loss += loss.item()

        loop.set_description(f"Epoch [{epoch+1}/{EPOCHS}]")
        loop.set_postfix(loss=loss.item())


    # -------------------------
    # Validation
    # -------------------------

    model.eval()

    correct = 0
    total = 0

    with torch.no_grad():

        for images, labels in valid_loader:

            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)

            _, predicted = torch.max(outputs, 1)

            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    accuracy = 100 * correct / total

    print(f"Validation Accuracy: {accuracy:.2f}%")



    # -------------------------
    # Save Checkpoint
    # -------------------------

    torch.save({
        "epoch": epoch,
        "model": model.state_dict(),
        "optimizer": optimizer.state_dict()
    }, CHECKPOINT_PATH)


# -----------------------------
# Save Final Model
# -----------------------------

torch.save(model.state_dict(), FINAL_MODEL_PATH)

print("Training Complete")
print("Model saved at:", FINAL_MODEL_PATH)