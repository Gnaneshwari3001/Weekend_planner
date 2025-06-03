import os

# Get the directory of the current script (F:\Weekend_Planner)
current_dir = os.path.dirname(os.path.abspath(__file__))
test_file_path = os.path.join(current_dir, "test.txt")

print(f"Attempting to read file from: {test_file_path}")

try:
    with open(test_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        print("Successfully read content:")
        print(content)
        if content.strip() == "":
            print("WARNING: File appears empty or only whitespace.")
        else:
            print("SUCCESS: File has content!")
except FileNotFoundError:
    print(f"ERROR: File not found at {test_file_path}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")