from os.path import exists


def get_unique_filename(original_filename: str, extension: str):
    if (exists(original_filename + "." + extension)):
        count = 1
        while (exists(original_filename+"_" + str(count) + "." + extension)):
            count += 1

        return original_filename + "_" + str(count) + "." + extension
    else:
        return original_filename + "." + extension
