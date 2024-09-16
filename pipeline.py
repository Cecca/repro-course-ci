import joblib
import pyattimo
import pandas as pd
import time


MEM = joblib.Memory(".cache")


# We get data from https://figshare.com/articles/dataset/Datasets/20747617
DATASETS = {
    "freezer": ("https://figshare.com/ndownloader/files/36982390", ".data/freezer.txt.gz"),
    "ECG": ("https://figshare.com/ndownloader/files/36982384", ".data/ECG.csv.gz")
}


def download_dataset(dataset):
    import urllib.request
    import os

    if not os.path.isdir(".data"):
        os.mkdir(".data")

    url, local_path = DATASETS[dataset]
    if not os.path.isfile(local_path):
        urllib.request.urlretrieve(url, filename=local_path)

    return local_path


@MEM.cache
def top_motif(dataset, window):
    dataset_path = download_dataset(dataset)
    ts = pyattimo.loadts(dataset_path, prefix=1_000_000)
    t_start = time.time()
    motifs = pyattimo.MotifsIterator(
      ts,
      w=window,
      top_k=1
    )
    motif = next(motifs)
    elapsed = time.time() - t_start
    res = pd.DataFrame([{
      "dataset": dataset,
      "window": window,
      "time_s": elapsed,
      "motif_distance": motif.distance
    }])

    return res


if __name__ == "__main__":
    import sys
    print(sys.argv)
    if len(sys.argv) > 1 and sys.argv[-1] == "check":
        m = top_motif("ECG", 500)
        expected = 0.17663362609569203
        actual = m["motif_distance"][0]
        assert expected == actual, f"expected {expected} got {actual}"
        sys.exit(0)

    res = pd.concat([
        top_motif("ECG", 500),
        top_motif("ECG", 1000),
        top_motif("freezer", 500),
        top_motif("freezer", 1000),
    ])
    print(res)

