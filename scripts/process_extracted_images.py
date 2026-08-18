"""
Process Extracted iPhone Backup Images for Social Media Setup
Automates image renaming, resizing, and organization for the 28 souls
"""

import json
import os
import shutil
from pathlib import Path
from PIL import Image
from typing import Dict, List

class ImageProcessor:
    """Process extracted images for social media setup"""
    
    def __init__(self):
        self.base_path = Path("scripts/iphone_backup_data")
        self.profile_images_dir = self.base_path / "profile_images"
        self.header_images_dir = self.base_path / "header_images"
        self.mapping_file = self.profile_images_dir / "image_mapping.json"
        self.souls_mapping = self.load_mapping()
        
    def load_mapping(self) -> Dict:
        """Load soul-to-image mapping"""
        if self.mapping_file.exists():
            with open(self.mapping_file, 'r') as f:
                return json.load(f)
        return {}
    
    def organize_extracted_images(self):
        """Organize extracted images by soul ID"""
        print("\n" + "=" * 60)
        print("Organizing Extracted Profile Images")
        print("=" * 60)
        
        # Find all image files in the profile_images directory
        image_extensions = ['.png', '.jpg', '.jpeg', '.heic', '.heif']
        extracted_images = []
        
        for ext in image_extensions:
            extracted_images.extend(self.profile_images_dir.glob(f"*{ext}"))
            extracted_images.extend(self.profile_images_dir.glob(f"*{ext.upper()}"))
        
        print(f"\nFound {len(extracted_images)} extracted images")
        
        if not extracted_images:
            print("No images found. Please extract images from iPhone Backup Extractor first.")
            return
        
        # Create a mapping of current filenames to expected soul IDs
        for image_path in extracted_images:
            filename = image_path.name.lower()
            
            # Try to match filename to soul mapping
            for soul_id, soul_data in self.souls_mapping.items():
                expected_name = soul_data['expected_filename'].lower()
                
                # Check if filename contains the expected name
                if expected_name.replace('.png', '') in filename or \
                   soul_data['name'].lower().replace(' ', '_') in filename:
                    
                    new_filename = soul_data['expected_filename']
                    new_path = self.profile_images_dir / new_filename
                    
                    if image_path != new_path:
                        print(f"Renaming: {image_path.name} → {new_filename}")
                        shutil.move(str(image_path), str(new_path))
                    break
        
        print("\n✓ Image organization complete")
    
    def resize_for_platforms(self):
        """Resize images for different social media platforms"""
        print("\n" + "=" * 60)
        print("Resizing Images for Social Media Platforms")
        print("=" * 60)
        
        platform_sizes = {
            'discord': 512,
            'twitter_profile': 400,
            'twitter_header': (1500, 500),
            'reddit': 256,
            'instagram': 1080
        }
        
        # Create platform-specific directories
        for platform in platform_sizes.keys():
            platform_dir = self.profile_images_dir / platform
            platform_dir.mkdir(exist_ok=True)
        
        # Process each soul's image
        for soul_id, soul_data in self.souls_mapping.items():
            source_image = self.profile_images_dir / soul_data['expected_filename']
            
            if not source_image.exists():
                print(f"⚠ Image not found: {soul_data['expected_filename']}")
                continue
            
            try:
                with Image.open(source_image) as img:
                    # Convert to RGB if necessary (for JPEG compatibility)
                    if img.mode in ('RGBA', 'P'):
                        img = img.convert('RGB')
                    
                    # Discord
                    discord_path = self.profile_images_dir / 'discord' / soul_data['expected_filename']
                    img.resize((platform_sizes['discord'], platform_sizes['discord']), 
                              Image.Resampling.LANCZOS).save(discord_path)
                    
                    # Twitter Profile
                    twitter_profile_path = self.profile_images_dir / 'twitter_profile' / soul_data['expected_filename']
                    img.resize((platform_sizes['twitter_profile'], platform_sizes['twitter_profile']), 
                              Image.Resampling.LANCZOS).save(twitter_profile_path)
                    
                    # Reddit
                    reddit_path = self.profile_images_dir / 'reddit' / soul_data['expected_filename']
                    img.resize((platform_sizes['reddit'], platform_sizes['reddit']), 
                              Image.Resampling.LANCZOS).save(reddit_path)
                    
                    # Instagram
                    instagram_path = self.profile_images_dir / 'instagram' / soul_data['expected_filename']
                    img.resize((platform_sizes['instagram'], platform_sizes['instagram']), 
                              Image.Resampling.LANCZOS).save(instagram_path)
                    
                    print(f"✓ Processed: {soul_data['name']} ({soul_id})")
                    
            except Exception as e:
                print(f"✗ Error processing {soul_data['name']}: {e}")
        
        print("\n✓ Image resizing complete")
        print(f"Platform directories created:")
        for platform in platform_sizes.keys():
            print(f"  - {platform}/")
    
    def generate_header_images(self):
        """Generate header images for Twitter from profile images"""
        print("\n" + "=" * 60)
        print("Generating Twitter Header Images")
        print("=" * 60)
        
        header_size = (1500, 500)
        header_dir = self.header_images_dir / 'twitter'
        header_dir.mkdir(parents=True, exist_ok=True)
        
        for soul_id, soul_data in self.souls_mapping.items():
            source_image = self.profile_images_dir / soul_data['expected_filename']
            
            if not source_image.exists():
                continue
            
            try:
                with Image.open(source_image) as img:
                    if img.mode in ('RGBA', 'P'):
                        img = img.convert('RGB')
                    
                    # Create header with centered profile image
                    header = Image.new('RGB', header_size, color='#1a1a2e')
                    
                    # Resize profile image for header
                    profile_size = 400
                    img_resized = img.resize((profile_size, profile_size), Image.Resampling.LANCZOS)
                    
                    # Center the profile image
                    x = (header_size[0] - profile_size) // 2
                    y = (header_size[1] - profile_size) // 2
                    header.paste(img_resized, (x, y))
                    
                    # Save header
                    header_filename = soul_data['expected_filename'].replace('.png', '_header.png')
                    header_path = header_dir / header_filename
                    header.save(header_path)
                    
                    print(f"✓ Generated header: {soul_data['name']}")
                    
            except Exception as e:
                print(f"✗ Error generating header for {soul_data['name']}: {e}")
        
        print("\n✓ Header image generation complete")
    
    def create_processing_report(self):
        """Create a report of processed images"""
        print("\n" + "=" * 60)
        print("Creating Processing Report")
        print("=" * 60)
        
        report = {
            'processing_summary': {
                'total_souls': len(self.souls_mapping),
                'images_processed': 0,
                'images_missing': 0,
                'platforms': ['discord', 'twitter_profile', 'twitter_header', 'reddit', 'instagram']
            },
            'soul_status': {}
        }
        
        for soul_id, soul_data in self.souls_mapping.items():
            source_image = self.profile_images_dir / soul_data['expected_filename']
            
            if source_image.exists():
                report['processing_summary']['images_processed'] += 1
                report['soul_status'][soul_id] = {
                    'name': soul_data['name'],
                    'status': 'processed',
                    'archetype': soul_data['archetype']
                }
            else:
                report['processing_summary']['images_missing'] += 1
                report['soul_status'][soul_id] = {
                    'name': soul_data['name'],
                    'status': 'missing',
                    'archetype': soul_data['archetype']
                }
        
        report_file = self.profile_images_dir / 'processing_report.json'
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n✓ Processing report saved: {report_file}")
        print(f"\nSummary:")
        print(f"  Total souls: {report['processing_summary']['total_souls']}")
        print(f"  Images processed: {report['processing_summary']['images_processed']}")
        print(f"  Images missing: {report['processing_summary']['images_missing']}")
    
    def run_full_processing(self):
        """Run complete image processing workflow"""
        print("=" * 60)
        print("iPhone Backup Image Processing Workflow")
        print("=" * 60)
        
        self.organize_extracted_images()
        self.resize_for_platforms()
        self.generate_header_images()
        self.create_processing_report()
        
        print("\n" + "=" * 60)
        print("Image Processing Complete")
        print("=" * 60)
        print(f"\nOutput directories:")
        print(f"  Profile images: {self.profile_images_dir}")
        print(f"  Header images: {self.header_images_dir}")
        print(f"\nPlatform-specific folders created:")
        print(f"  - discord/")
        print(f"  - twitter_profile/")
        print(f"  - twitter_header/")
        print(f"  - reddit/")
        print(f"  - instagram/")

def main():
    """Main function"""
    print("iPhone Backup Image Processor")
    print("This script will process extracted images for social media setup\n")
    
    processor = ImageProcessor()
    processor.run_full_processing()

if __name__ == "__main__":
    main()
