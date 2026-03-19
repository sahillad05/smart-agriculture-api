import torch
import torch.nn as nn
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

VALID_DIR = "data/plant_disease/dataset/valid"
MODEL_PATH = "ml_models/disease_model.pth"

IMAGE_SIZE = 128
BATCH_SIZE = 16

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Model Architecture definition
class PlantDiseaseCNN(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(3, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(64, 128, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2)
        )
        self.fc = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 16 * 16, 512), nn.ReLU(), nn.Dropout(0.5),
            nn.Linear(512, num_classes)
        )
    def forward(self, x):
        x = self.conv(x)
        return self.fc(x)

def evaluate_disease_model():
    print("Evaluating Plant Disease CNN Model...")
    
    transform = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor()
    ])
    
    try:
        valid_dataset = datasets.ImageFolder(VALID_DIR, transform=transform)
    except FileNotFoundError:
        print(f"Error: Validation dataset not found at {VALID_DIR}")
        return
        
    valid_loader = DataLoader(valid_dataset, batch_size=BATCH_SIZE, num_workers=0)
    
    num_classes = len(valid_dataset.classes)
    model = PlantDiseaseCNN(num_classes).to(device)
    
    try:
        model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
    except FileNotFoundError:
        print(f"Error: Model not found at {MODEL_PATH}")
        return
        
    model.eval()
    correct = 0
    total = 0

    print("Running evaluation on validation set...")
    with torch.no_grad():
        for images, labels in valid_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    accuracy = 100 * correct / total
    print(f"\nValidation Accuracy: {accuracy:.2f}%")

if __name__ == "__main__":
    evaluate_disease_model()
