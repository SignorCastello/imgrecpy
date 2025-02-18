import requests
import time
import torch
import json
from PIL import Image
from transformers import AutoProcessor, AutoModelForCausalLM
torch.set_num_threads(4)
start_time = time.time()
device = "cpu"
torch_dtype = torch.float32
model_name = "microsoft/Florence-2-base"
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch_dtype, trust_remote_code=True).to(device)
processor = AutoProcessor.from_pretrained(model_name, trust_remote_code=True)
image = Image.open("D:\\apk1\\imgrecpy\\uploads\\photo.jpg").convert("RGB")
image = image.resize((512, 512))
def run_example(task_prompt, text_input=None):
    prompt = task_prompt if text_input is None else task_prompt + text_input
    inputs = processor(text=prompt, images=image, return_tensors="pt").to(device, torch_dtype)

    generated_ids = model.generate(
        input_ids=inputs["input_ids"],
        pixel_values=inputs["pixel_values"],
        max_new_tokens=512,
        num_beams=1,
        do_sample=True,
        temperature=0.7,
        top_k=50,
        top_p=0.95,
        early_stopping=False
    )

    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    parsed_answer = processor.post_process_generation(generated_text, task=task_prompt, image_size=(image.width, image.height))
    with open('caption.txt', 'w') as fp:
        fp.write(json.dumps(parsed_answer))

    with open('caption.txt', "rb") as file:
        files = {"file": file}
        response = requests.post("http://192.168.169.248:5000/upload", files=files)

prompt = "<CAPTION>"
run_example(prompt)
print("--- %s seconds ---" % (time.time() - start_time))
