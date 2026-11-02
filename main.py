# import torch

# # 1. Check if CUDA is available
# cuda_available = torch.cuda.is_available()
# print(f"Is CUDA available? {cuda_available}")

# # 2. Get additional GPU information if available
# if cuda_available:
#     print(f"CUDA Version: {torch.version.cuda}")
#     print(f"Number of GPUs: {torch.cuda.device_count()}")
#     print(f"Current GPU Device ID: {torch.cuda.current_device()}")
#     print(f"GPU Name: {torch.cuda.get_device_name(torch.cuda.current_device())}")
# else:
#     print("CUDA is not available. PyTorch will use the CPU.")
import os
from config.settings import settings
from src.server import create_app

app, stream = create_app()

if __name__ == "__main__":
    # Launch with built-in WebRTC test UI on port 7860
    # To run as pure FastAPI backend instead, use:
    # uvicorn.run("main:app", host=settings.APP_HOST, port=settings.APP_PORT, reload=True)
    stream.ui.launch(server_port=7860)