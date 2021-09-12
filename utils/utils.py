from datetime import datetime


def write_to_file(data, file_path):
    print(f'Starting to write into file: {file_path} ...')

    try:
        with open(file_path, 'a') as f:
            f.write(data)
            f.write(',\n')
    except:
        return False

    return True


def assemble_file_path(file_path_base, interval):
    dt_now = datetime.now()
    dt_string = dt_now.strftime(f'%Y_%m_%d_%H:%M:%S_{interval}')

    return file_path_base + dt_string + '.json'
