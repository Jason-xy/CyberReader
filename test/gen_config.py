import sys
import yaml

def generate_yaml_file(model, token, tmp_dir, result_dir, contents):
    data = {
        'MODEL': model,
        'TOKEN': token,
        'TMP_DIR': tmp_dir,
        'RESULT_DIR': result_dir,
        'CONTENTS': contents
    }

    with open('config.yaml', 'w') as file:
        yaml.dump(data, file)

if __name__ == '__main__':
    if len(sys.argv) != 6:
        print('Usage: python script.py <model> <token> <tmp_dir> <result_dir> <contents>')
        sys.exit(1)

    model = sys.argv[1]
    token = sys.argv[2]
    tmp_dir = sys.argv[3]
    result_dir = sys.argv[4]
    contents = sys.argv[5]

    generate_yaml_file(model, token, tmp_dir, result_dir, contents)
    print('YAML file generated successfully.')