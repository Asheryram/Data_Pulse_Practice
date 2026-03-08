"""Celery tasks for background processing."""

from celery import shared_task


@shared_task
def process_uploaded_file(dataset_id, filename):
    """
    Process uploaded CSV/JSON file in background.
    Updates dataset status when complete.
    """
    import json

    from datasets.models import Dataset, DatasetFile
    from datasets.services.file_parser import parse_csv, parse_json

    print(f"\n{'=' * 60}")
    print(f"[CELERY WORKER] 🚀 Starting to parse dataset {dataset_id}: {filename}")
    print(f"{'=' * 60}\n")

    try:
        dataset = Dataset.objects.get(id=dataset_id)
        dataset_file = DatasetFile.objects.get(dataset=dataset)

        # Parse the file (this is the slow part for large files)
        if filename.endswith(".csv"):
            metadata = parse_csv(dataset_file.file_path)
        else:
            metadata = parse_json(dataset_file.file_path)

        # Update dataset with parsed metadata
        dataset.row_count = metadata["row_count"]
        dataset.column_count = metadata["column_count"]
        dataset.column_names = json.dumps(metadata["column_names"])
        dataset.status = "COMPLETED"
        dataset.save()

        print(f"\n{'=' * 60}")
        print("[CELERY WORKER] ✅ Finished parsing dataset {}".format(dataset_id))
        print(f"[CELERY WORKER] 📈 Parsed {metadata['row_count']} rows, {metadata['column_count']} columns")
        print("[CELERY WORKER] 💾 Updated dataset status to COMPLETED")
        print(f"{'=' * 60}\n")

        return {
            "dataset_id": dataset_id,
            "filename": filename,
            "rows_parsed": metadata["row_count"],
            "status": "completed",
        }
    except Exception as e:
        print(f"[CELERY WORKER] ❌ Error processing dataset {dataset_id}: {e}")
        dataset = Dataset.objects.get(id=dataset_id)
        dataset.status = "FAILED"
        dataset.save()
        raise
