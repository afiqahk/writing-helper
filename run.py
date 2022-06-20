import yaml
import pathlib

from __generator__ import generate

def main():
    # read yaml config
    with open("config.yaml", 'r') as f:
        args = yaml.load(f, Loader=yaml.SafeLoader)
    generate.run(**args)

if __name__=="__main__":
    main()