import torch
import torch.nn as nn
from torchvision import transforms
from PIL import Image

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

    image = transform(image).unsqueeze(0).to(device)

    with torch.no_grad():

        outputs = model(image)

        probabilities = torch.softmax(outputs, dim=1)

        confidence, predicted = torch.max(probabilities, 1)

    disease = class_names[predicted.item()]
    confidence = confidence.item()

    return disease, confidence