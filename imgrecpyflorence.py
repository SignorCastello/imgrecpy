import requests
import time
import torch
import json
from PIL import Image
from transformers import AutoProcessor, PaliGemmaForConditionalGeneration

# Set configurations
torch.set_num_threads(4)
start_time = time.time()
device = "cuda"  # Assuming the device name is 'cuda' for GPU
torch_dtype = torch.float32
model_name = "google/paligemma-3b-pt-224"
model_id = "google/paligemma-3b-mix-224"
device = "cuda:0"
dtype = torch.bfloat16

image = Image.open("C:\\Users\\Nicolò\\Desktop\\imgrecpy-master\\uploads\\photo.jpg")

model = PaliGemmaForConditionalGeneration.from_pretrained(
    model_id,
    torch_dtype=dtype,
    device_map=device,
    revision="bfloat16",
).eval()
processor = AutoProcessor.from_pretrained(model_id, token=access_token)

prompt = "caption it"
model_inputs = processor(text=prompt, images=image, return_tensors="pt").to(model.device)
input_len = model_inputs["input_ids"].shape[-1]

with torch.inference_mode():
    generation = model.generate(**model_inputs, max_new_tokens=100, do_sample=False)
    generation = generation[0][input_len:]
    decoded = processor.decode(generation, skip_special_tokens=True)
    print(decoded)

# Save the result to a file
with open('caption.txt', 'w') as fp:
    fp.write(json.dumps(decoded))

# Upload the result to the server
with open('caption.txt', "rb") as file:
    files = {"file": file}
    response = requests.post("http://192.168.137.174:5000/upload", files=files)

# Output the time taken to process
print("--- %s seconds ---" % (time.time() - start_time))
