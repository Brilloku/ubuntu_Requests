import requests
import os
from urllib.parse import urlparse
import hashlib

def get_filename_from_url(url):
    """Extract a safe filename from the URL, or generate one."""
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    if not filename:
        filename = "downloaded_image.jpg"
    return filename

def is_duplicate(content, save_dir):
    """Check if this image already exists (compare by file hash)."""
    file_hash = hashlib.md5(content).hexdigest()
    for fname in os.listdir(save_dir):
        fpath = os.path.join(save_dir, fname)
        with open(fpath, "rb") as f:
            existing_hash = hashlib.md5(f.read()).hexdigest()
            if file_hash == existing_hash:
                return True
    return False

def fetch_image(url, save_dir="Fetched_Images"):
    try:
        # Make request
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Check content type (precaution)
        content_type = response.headers.get("Content-Type", "")
        if not content_type.startswith("image/"):
            print(f"✗ Skipped (not an image): {url}")
            return
        
        # Create directory if it doesn't exist
        os.makedirs(save_dir, exist_ok=True)
        
        # Duplicate prevention
        if is_duplicate(response.content, save_dir):
            print(f"✗ Duplicate detected, skipping: {url}")
            return
        
        # Get filename
        filename = get_filename_from_url(url)
        filepath = os.path.join(save_dir, filename)
        
        # If file exists with same name, avoid overwrite
        counter = 1
        base, ext = os.path.splitext(filename)
        while os.path.exists(filepath):
            filename = f"{base}_{counter}{ext}"
            filepath = os.path.join(save_dir, filename)
            counter += 1
        
        # Save image
        with open(filepath, "wb") as f:
            f.write(response.content)
        
        print(f"✓ Successfully fetched: {filename}")
        print(f"✓ Image saved to {filepath}")
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
    except Exception as e:
        print(f"✗ An error occurred: {e}")

def main():
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")
    
    urls = input("Please enter one or more image URLs (separated by spaces): ").split()
    
    for url in urls:
        fetch_image(url)
    
    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()
