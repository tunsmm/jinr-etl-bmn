import os
import random
import string

from config.logger import logger


def create_files_workflow(
    directory: str,
    num_files: int,
    file_size_range: tuple,
    change_file_content_index: int = 10,
):
    """
    Generate files in a specified directory.

    Args:
        - directory: The directory where the files will be generated.
        - num_files: The number of files to generate.
        - file_size_range: A tuple representing the range of file sizes to generate.
        - change_file_content_index: The index file number at which content needs to be changed.
    """
    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f"The directory {directory} has been created.")

    # Generate the files
    for index in range(num_files):
        # Generate a random file name
        file_name = (
            "".join(random.choices(string.ascii_letters + string.digits, k=10)) + ".txt"
        )

        if index % change_file_content_index == 0:
            # Generate a random file size within the specified range
            file_size = random.randint(file_size_range[0], file_size_range[1])

            # Generate the file content
            file_content = "".join(
                random.choices(string.ascii_letters + string.digits, k=file_size)
            )

        # Write the file content to the file
        with open(os.path.join(directory, file_name), "w") as file:
            file.write(file_content)

        logger.info(f"File '{file_name}' has been created with size {file_size}")
