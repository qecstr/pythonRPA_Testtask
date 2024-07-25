import os
import pytest
from tempfile import TemporaryDirectory
from categorize_files import categorize_files_by_type


@pytest.fixture
def create_test_environment():
    with TemporaryDirectory() as tmp_dir:
        base_path = tmp_dir
        os.makedirs(os.path.join(base_path, "subfolder1"), exist_ok=True)
        os.makedirs(os.path.join(base_path, "subfolder2", "nested"), exist_ok=True)

        with open(os.path.join(base_path, "file1.txt"), 'w') as f:
            f.write("content1")

        with open(os.path.join(base_path, "subfolder1", "file2.txt"), 'w') as f:
            f.write("content2" * 1000)

        with open(os.path.join(base_path, "subfolder2", "file3.txt"), 'w') as f:
            f.write("content3" * 1000)

        with open(os.path.join(base_path, "subfolder2", "nested", "file4.txt"), 'w') as f:
            f.write("content4" * 1000)

        with open(os.path.join(base_path, "image.jpg"), 'w') as f:
            f.write("image content" * 500)

        with open(os.path.join(base_path, "subfolder1", "image2.jpg"), 'w') as f:
            f.write("image content2" * 500)

        with open(os.path.join(base_path, "document.pdf"), 'w') as f:
            f.write("document content" * 2)

        with open(os.path.join(base_path, "subfolder2", "nested", "file_no_ext"), 'w') as f:
            f.write("file with no extension")

        yield base_path


def test_categorize_files_by_type(create_test_environment):
    folder_path = create_test_environment
    result = categorize_files_by_type(folder_path)

    assert '.txt' in result
    assert any(file['path'] == os.path.join(folder_path, 'file1.txt') for file in result['.txt'])
    assert any(file['path'] == os.path.join(folder_path, 'subfolder1', 'file2.txt') for file in result['.txt'])
    assert any(file['path'] == os.path.join(folder_path, 'subfolder2', 'file3.txt') for file in result['.txt'])
    assert any(
        file['path'] == os.path.join(folder_path, 'subfolder2', 'nested', 'file4.txt') for file in result['.txt'])

    assert '.jpg' in result
    assert any(file['path'] == os.path.join(folder_path, 'image.jpg') for file in result['.jpg'])
    assert any(file['path'] == os.path.join(folder_path, 'subfolder1', 'image2.jpg') for file in result['.jpg'])

    assert '.pdf' in result
    assert any(file['path'] == os.path.join(folder_path, 'document.pdf') for file in result['.pdf'])

    assert '' in result
    assert any(file['path'] == os.path.join(folder_path, 'subfolder2', 'nested', 'file_no_ext') for file in result[''])


def test_non_existent_directory():
    with pytest.raises(FileNotFoundError):
        categorize_files_by_type("non_existent_directory")


def test_not_a_directory():
    with TemporaryDirectory() as tmp_dir:
        file_path = os.path.join(tmp_dir, "file.txt")
        with open(file_path, 'w') as f:
            f.write("content")

        with pytest.raises(NotADirectoryError):
            categorize_files_by_type(file_path)