import torch
import torchvision
import torchvision.transforms as transforms
from PIL import Image
import torch.nn.functional as F

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

class ModelHead(torch.nn.Module):
    def __init__(self, input_dim, hidden_dim, n_classes):
        super(ModelHead, self).__init__()
        self.fc1 = torch.nn.Linear(input_dim, hidden_dim)
        self.relu1 = torch.nn.ReLU()
        self.fc2 = torch.nn.Linear(hidden_dim, hidden_dim // 2)
        self.relu2 = torch.nn.ReLU()
        self.fc3 = torch.nn.Linear(hidden_dim // 2, n_classes)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu1(x)
        x = self.fc2(x)
        x = self.relu2(x)
        x = self.fc3(x)
        return x

model = torchvision.models.resnet50(pretrained=True).to(device)
model.fc = ModelHead(2048, 1024, 12)
model.fc.to(device)

MODEL_SAVE_PATH = '../data/best_checkpoint.pth'
model.load_state_dict(torch.load(MODEL_SAVE_PATH, map_location=device))
model.eval()

transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
])

def preprocess_image(image):
    image = Image.open(image).convert('RGB')
    image = transform(image)
    image = image.unsqueeze(0)
    return image.to(device)

def predict(model, image):
    model.eval()
    image = preprocess_image(image)
    with torch.no_grad():
        output = model(image)
        probabilities = F.softmax(output, dim=1)
        confidence, predicted = torch.max(probabilities, 1)
    return predicted.item(), confidence.item()