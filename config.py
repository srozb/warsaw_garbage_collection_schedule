
def parse_config(filename: str = "config.yaml"):
    import yaml
    with open(filename, 'r') as cnf_file:
        return yaml.safe_load(cnf_file.read())

config = parse_config()
