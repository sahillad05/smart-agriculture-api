from huggingface_hub import hf_hub_download
import os

MODEL_DIR = "ml_models"

os.makedirs(MODEL_DIR, exist_ok=True)


def download_models():

    crop_model = os.path.join(MODEL_DIR, "crop_model.pkl")
    yield_model = os.path.join(MODEL_DIR, "yield_model.pkl")
    disease_model = os.path.join(MODEL_DIR, "disease_model.pth")

    if not os.path.exists(crop_model):

        hf_hub_download(
            repo_id="sahillad55/smart-agriculture-models",
            filename="crop_model.pkl",
            local_dir=MODEL_DIR
        )

    if not os.path.exists(yield_model):

        hf_hub_download(
            repo_id="sahillad55/smart-agriculture-models",
            filename="yield_model.pkl",
            local_dir=MODEL_DIR
        )

    if not os.path.exists(disease_model):

        hf_hub_download(
            repo_id="sahillad55/smart-agriculture-models",
            filename="disease_model.pth",
            local_dir=MODEL_DIR
        )