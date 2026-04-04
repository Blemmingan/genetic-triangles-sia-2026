import argparse
import logging
from pathlib import Path
from PIL import Image

from utils.config_loader import load_config

def main():
    """
    Entry point for the Genetic Algorithm Image Approximation.
    Parses arguments, loads hyperparameters, and runs the engine.
    """
    parser = argparse.ArgumentParser(description="Genetic Algorithm for Image Approximation")
    
    # Core parameters
    parser.add_argument("--image", type=str, help="Path to target image")
    parser.add_argument("--triangles", type=int, help="Number of triangles to use")
    parser.add_argument("--config", type=str, default="config/default.json", help="Path to config file")
    
    # Hyperparameter overrides
    parser.add_argument("--population-size", type=int, help="Override population size")
    parser.add_argument("--generations", type=int, help="Override generations count")
    parser.add_argument("--selection", type=str, help="Override selection method")
    parser.add_argument("--crossover", type=str, help="Override crossover method")
    parser.add_argument("--mutation", type=str, help="Override mutation method")
    parser.add_argument("--replacement", type=str, help="Override replacement method")
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config, args)
    
    # Identify images to process
    images_to_process = []
    
    if args.image:
        images_to_process.append(Path(args.image))
    else:
        # Default: read all .png files in the inputs directory
        inputs_dir = Path("inputs")
        if inputs_dir.exists():
            images_to_process.extend(inputs_dir.rglob("*.png"))
    
    if not images_to_process:
        print("No images found to process. Please provide --image or add .png files to inputs directory.")
        return
        
    for image_path in images_to_process:
        print(f"Processing image: {image_path}")
        try:
            with Image.open(image_path) as img:
                # Force loading the image data
                img.load()
                print(f"Successfully loaded image {image_path.name} with size {img.size}")
                
            # TODO: Instantiate operators based on config
            # TODO: Instantiate the GA engine
            # TODO: engine.run()
            # TODO: Save metrics and best generated image to outputs/
            
        except Exception as e:
            print(f"Error reading {image_path}: {e}")
            
    print("GA engine logic is currently stubbed out.")

if __name__ == "__main__":
    main()
