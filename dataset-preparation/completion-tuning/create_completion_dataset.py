from pathlib import Path
import pandas as pd


# Script I used to create a pandas dataset of ascii art which I can use to train my ASCII adapters.
# This time I formatted it in a parquet file directly.


# see: https://huggingface.co/datasets/Thufail/Ascii-Art-Animals
def create_dataset(path: Path, version_tag: str) -> None:
    paths = []
    for file in path.glob("**/*.txt"):
        txt_file = file
        paths.append({"ascii": txt_file})
    paths.sort(
        key=lambda x: (x["ascii"].parent.parents[0], int(x["ascii"].parent.name))
    )

    dataset_items = []
    for path in paths:
        with open(path["ascii"], "r") as f:
            ascii_art = f.read()

        dataset_items.append(
            {
                "ascii": ascii_art,
                "creature": str(path["ascii"].parent.parent.name),
            }
        )

    df = pd.DataFrame(dataset_items)

    output_path = Path(f"src/dataset/out/ascii_art_{version_tag}.parquet")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path)
    print(f"Dataset successfully saved to {output_path}")


if __name__ == "__main__":
    create_dataset(path=Path("src/dataset/ascii_art/animals/cat"), version_tag="cat_5")
