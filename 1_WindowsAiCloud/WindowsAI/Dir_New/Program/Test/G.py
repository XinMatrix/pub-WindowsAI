from multiprocessing import freeze_support

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from torch.utils.data import Dataset, DataLoader

freeze_support()


# 数据生成
def generate_star_data_optimized(num_stars):
    names = [f"Star_{i}" for i in range(num_stars)]
    masses = np.random.uniform(1e10, 1e30, size=num_stars)
    distances = np.random.uniform(1e10, 1e20, size=num_stars)
    star_data = list(zip(names, masses, distances))
    return star_data


# 计算引力
def calculate_forces_optimized(masses, distances):
    num_stars = len(masses)
    forces = []
    for i in range(num_stars):
        for j in range(i + 1, num_stars):
            mass1 = masses[i]
            mass2 = masses[j]
            distance = abs(distances[i] - distances[j])
            force = 6.67430e-11 * mass1 * mass2 / distance ** 2
            forces.append((mass1, mass2, distance, force))
    return forces


# 准备数据
def prepare_data(star_data, forces):
    features = []
    labels = []
    for mass1, mass2, distance, force in forces:
        features.append([mass1, mass2, distance])
        labels.append(force)
    return np.array(features), np.array(labels)


# 生成和处理数据
stars = generate_star_data_optimized(1000)
masses = np.array([mass for _, mass, _ in stars])
distances = np.array([distance for _, _, distance in stars])
forces = calculate_forces_optimized(masses, distances)
features, labels = prepare_data(stars, forces)

# 数据标准化
scaler = StandardScaler()
features = scaler.fit_transform(features)

# 转换为 PyTorch 张量
X = torch.tensor(features, dtype=torch.float32)
y = torch.tensor(labels, dtype=torch.float32)

# 划分数据集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# 自定义数据集
class GravityDataset(Dataset):
    def __init__(self, features, labels):
        self.features = features
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        return self.features[idx], self.labels[idx]


# 数据加载器
train_dataset = GravityDataset(X_train, y_train)
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True, num_workers=4)


# 神经网络模型
class GravityNet(nn.Module):
    def __init__(self):
        super(GravityNet, self).__init__()
        self.fc1 = nn.Linear(3, 128)
        self.bn1 = nn.BatchNorm1d(128)
        self.dropout1 = nn.Dropout(0.2)
        self.fc2 = nn.Linear(128, 64)
        self.bn2 = nn.BatchNorm1d(64)
        self.dropout2 = nn.Dropout(0.2)
        self.fc3 = nn.Linear(64, 32)
        self.bn3 = nn.BatchNorm1d(32)
        self.dropout3 = nn.Dropout(0.2)
        self.fc4 = nn.Linear(32, 1)

    def forward(self, x):
        x = torch.relu(self.bn1(self.fc1(x)))
        x = self.dropout1(x)
        x = torch.relu(self.bn2(self.fc2(x)))
        x = self.dropout2(x)
        x = torch.relu(self.bn3(self.fc3(x)))
        x = self.dropout3(x)
        x = self.fc4(x)
        return x


model = GravityNet().cuda()
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr=1e-3)
scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.1)

# 训练模型
num_epochs = 20
for epoch in range(num_epochs):
    model.train()
    for batch_features, batch_labels in train_loader:
        batch_features, batch_labels = batch_features.cuda(), batch_labels.cuda()
        optimizer.zero_grad()
        outputs = model(batch_features)
        loss = criterion(outputs.squeeze(), batch_labels)
        loss.backward()
        optimizer.step()

    scheduler.step()

    if (epoch + 1) % 5 == 0:
        model.eval()
        with torch.no_grad():
            test_outputs = model(X_test.cuda())
            test_loss = criterion(test_outputs.squeeze(), y_test.cuda())
            print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}, Test Loss: {test_loss.item():.4f}')

# 模型评估
model.eval()
with torch.no_grad():
    y_pred = model(X_test.cuda()).cpu().numpy()
    y_true = y_test.numpy()
    mse = np.mean((y_pred - y_true) ** 2)
    print(f'Mean Squared Error on Test Set: {mse:.4e}')
