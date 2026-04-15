import json
import pandas as pd
import os
import datetime

# --- CONFIGURATION ---
SOURCE_FILE = 'raw_data.json'
OUTPUT_FILE = 'processed_data.csv'


def extract(file_path):
    """
    Task 1: Doc du lieu JSON tu file.
    """
    print(f"Extracting data from {file_path}...")
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
        print(f"Extracted: {len(data)}")
        return data
    except FileNotFoundError:
        print("Error: File not found.")
        return []
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
        return []


def validate(data):
    """
    Task 2: Kiem tra chat luong du lieu.
    """
    valid_records = []
    error_count = 0

    for record in data:
        price = record.get('price', 0)
        category = record.get('category')

        # Validation rules
        if price > 0 and category and str(category).strip() != "":
            valid_records.append(record)
        else:
            error_count += 1

    print(f"Processed: {len(valid_records)}")
    print(f"Dropped: {error_count}")
    return valid_records


def transform(data):
    """
    Task 3: Ap dung business logic.
    """
    if not data:
        print("No data to transform.")
        return None

    df = pd.DataFrame(data)

    # Ensure price column exists
    if 'price' not in df.columns:
        print("Error: 'price' column missing.")
        return None

    # Transformations
    df['discounted_price'] = df['price'] * 0.9
    df['category'] = df['category'].astype(str).str.title()
    df['processed_at'] = datetime.datetime.now().isoformat()

    print(f"Transformation complete. {len(df)} records processed.")
    return df


def load(df, output_path):
    """
    Task 4: Luu DataFrame ra file CSV.
    """
    try:
        df.to_csv(output_path, index=False)
        print(f"Data saved to {output_path}")
    except Exception as e:
        print(f"Error saving file: {e}")


# ============================================================
# MAIN PIPELINE
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("ETL Pipeline Started...")
    print("=" * 50)

    # 1. Extract
    raw_data = extract(SOURCE_FILE)

    if raw_data:
        # 2. Validate
        clean_data = validate(raw_data)

        # 3. Transform
        final_df = transform(clean_data)

        # 4. Load
        if final_df is not None:
            load(final_df, OUTPUT_FILE)
            print(f"\nPipeline completed! {len(final_df)} records saved.")
        else:
            print("\nTransform returned None. Check your transform() function.")
    else:
        print("\nPipeline aborted: No data extracted.")