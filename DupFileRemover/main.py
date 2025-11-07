import os
import hashlib

def file_hash(path, chunk_size=8192):
    """Compute SHA256 hash of a file."""
    sha = hashlib.sha256()
    try:
        with open(path, "rb") as f:
            while chunk := f.read(chunk_size):
                sha.update(chunk)
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return None
    return sha.hexdigest()

def remove_duplicates(folder, recursive=True, dry_run=True):
    """Remove duplicate files in a folder based on file content."""
    seen_hashes = {}
    duplicates = []

    for root, _, files in os.walk(folder):
        for filename in files:
            filepath = os.path.join(root, filename)
            filehash = file_hash(filepath)
            if not filehash:
                continue

            if filehash in seen_hashes:
                duplicates.append(filepath)
            else:
                seen_hashes[filehash] = filepath

        if not recursive:
            break

    # Summary
    print(f"\nFound {len(duplicates)} duplicate files.")

    # Delete duplicates
    for dup in duplicates:
        if dry_run:
            print(f"[DRY RUN] Would remove: {dup}")
        else:
            try:
                os.remove(dup)
                print(f"Removed: {dup}")
            except Exception as e:
                print(f"Failed to remove {dup}: {e}")

    print("\nDone.")
    return duplicates


if __name__ == "__main__":
    folder_path = input("Enter folder path: ").strip()
    confirm = input("Dry run? (y/n): ").strip().lower() != "n"
    remove_duplicates(folder_path, dry_run=confirm)

