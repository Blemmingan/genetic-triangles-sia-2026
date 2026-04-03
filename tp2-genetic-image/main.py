import argparse
import logging
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
    
    # TODO: Initialize target image
    # TODO: Instantiate operators based on config
    # TODO: Instantiate the GA engine
    # TODO: engine.run()
    # TODO: Save metrics and best generated image to outputs/
    
    raise NotImplementedError("main logic is stubbed out and ready to be filled.")

if __name__ == "__main__":
    main()
