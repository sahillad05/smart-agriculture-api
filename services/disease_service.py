import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image
import numpy as np

MODEL_PATH = "ml_models/disease_model.pth"

IMAGE_SIZE = 128

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


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
            nn.Linear(512, 14)
        )

    def forward(self, x):
        x = self.conv(x)
        x = self.fc(x)
        return x


class_names = [
'Apple___Apple_scab',
'Apple___Black_rot',
'Apple___healthy',
'Corn_(maize)___Northern_Leaf_Blight',
'Corn_(maize)___healthy',
'Potato___Early_blight',
'Potato___Late_blight',
'Potato___healthy',
'Tomato___Early_blight',
'Tomato___Late_blight',
'Tomato___Septoria_leaf_spot',
'Tomato___Target_Spot',
'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
'Tomato___healthy'
]


model = PlantDiseaseCNN(len(class_names))
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model.to(device)
model.eval()


transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor()
])


def predict_disease(image):

    # Heuristic Check: Ensure image actually contains a leaf
    # Convert PIL Image to HSV to check for plant colors
    img_hsv = image.convert("HSV")
    img_np = np.array(img_hsv)
    
    h = img_np[:, :, 0]
    s = img_np[:, :, 1]
    v = img_np[:, :, 2]
    
    # In PIL's HSV, H is 0-255. Green is ~85, Yellow is ~42.
    # We look for H between 35 and 105 (greenish), with higher saturation to avoid pale walls.
    mask = (h >= 35) & (h <= 105) & (s >= 50) & (v >= 40)
    plant_ratio = np.mean(mask)

    if plant_ratio < 0.05:  # Require at least 5% of the image to be distinctly plant-colored
        return "No leaf detected", 0.0

    image_tensor = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():

        outputs = model(image_tensor)

        probabilities = torch.softmax(outputs, dim=1)

        confidence, predicted = torch.max(probabilities, 1)

    disease = class_names[predicted.item()]
    confidence = confidence.item()

    return disease, confidence