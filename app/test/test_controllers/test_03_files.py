import pytest

from ...controllers.files import *
from ...controllers.files.slides import *


async def test_upload_file():
    ref = FileUpload(
        filename="some.py",
        read=(await aiofiles.open("/dev/null", "rb")).read
    )

    r = await upload(ref)

    assert isinstance(r.id, int)
    assert r.filename == ref.filename


async def test_list_files():
    refs: List[FileUpload] = [
        FileUpload(
            filename=f"some-file-{i}",
            read=(await aiofiles.open("/dev/null", "rb")).read
        )
        for i in range(10)
    ]

    files: List[File] = [await upload(ref) for ref in refs]

    ls = dict(((file.id, file) for file in await list_files()))

    for file in files:
        assert ls[file.id].dict() == file.dict()


async def test_remove_file():
    ref = FileUpload(
        filename="some.py",
        read=(await aiofiles.open("/dev/null", "rb")).read
    )

    r = await upload(ref)
    await remove_file(r.id)

    assert not list(filter(lambda x: x.id == r.id, await list_files()))


async def test_remove_non_exist_file():
    with pytest.raises(FileNotFound):
        await remove_file(-1)


async def test_presentation_info():
    file = "./assets/test_files/file.pptx"

    f = await upload(FileUpload(
        filename="presentation.pptx",
        read=(await aiofiles.open(file, "rb")).read
    ))

    r = await get_slides_info(f.id)

    assert list(map(lambda x: x.dict(), r)) == [{
        "image_path": f"{STORAGE_PRESENTATION_IMAGES}/{f.id}-00.jpg",
        "comment": "First slide comments"
    }, {
        "image_path": f"{STORAGE_PRESENTATION_IMAGES}/{f.id}-01.jpg",
        "comment": "Second slide comments"
    }]
