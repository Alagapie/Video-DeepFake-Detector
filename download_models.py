import os
import yaml
from huggingface_hub import hf_hub_download


def main():
    with open("config.yaml") as f:
        config = yaml.safe_load(f)

    weights_dir = config["weights_dir"]
    os.makedirs(weights_dir, exist_ok=True)

    model_specs = {
        "resnet18": config["models"]["resnet18"],
        "vit_b16": config["models"]["vit_b16"],
    }

    for name, spec in model_specs.items():
        dest = os.path.join(weights_dir, spec["filename"])
        if os.path.exists(dest):
            print(f"[SKIP] {name} already exists at {dest}")
            continue

        print(f"[DOWNLOAD] {name} from {spec['repo_id']}/{spec['filename']} ...")
        path = hf_hub_download(
            repo_id=spec["repo_id"],
            filename=spec["filename"],
            local_dir=weights_dir,
        )
        print(f"[DONE] {name} -> {path}")

    print("\nAll models downloaded to ./weights/")
    print("Files:", os.listdir(weights_dir))


if __name__ == "__main__":
    main()
