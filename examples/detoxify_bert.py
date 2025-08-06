import torch as pt
from detoxify import Detoxify

# set device for apple devices
device = "mps" if pt.backends.mps.is_available() else "cpu"
print(f"Using device: {device}")

model = Detoxify("original", device=device)

# Test prediction
text = "You are worthless and should die"
results = model.predict(text)

print(results)
