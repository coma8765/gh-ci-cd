import pytest

from ...controllers.files import *
from ...controllers.files.slides import *

SLIDES_FILE = "./assets/test_files/file.pptx"


async def test_upload_file():
    ref = FileUpload(
        filename="some.py", read=(await aiofiles.open("/dev/null", "rb")).read
    )

    r = await upload(ref)

    assert isinstance(r.id, int)
    assert r.filename == ref.filename


async def test_list_files():
    refs: List[FileUpload] = [
        *[
            FileUpload(
                filename=f"some-file-{i}",
                read=(await aiofiles.open("/dev/null", "rb")).read,
            )
            for i in range(10)
        ],
        *[
            FileUpload(
                filename=f"some-file-{i}.pptx",
                read=(await aiofiles.open(SLIDES_FILE, "rb")).read,
            )
            for i in range(10)
        ],
    ]

    files: List[File] = [await upload(ref) for ref in refs]

    ls = dict(((file.id, file) for file in await list_files()))

    for file in files:
        assert ls[file.id].dict() == file.dict()

        if file.filename.endswith(".pptx"):
            assert ls[file.id].type_addons.count_slides == 2


async def test_remove_file():
    ref = FileUpload(
        filename="some.py", read=(await aiofiles.open("/dev/null", "rb")).read
    )

    r = await upload(ref)
    await remove_file(r.id)

    assert not list(filter(lambda x: x.id == r.id, await list_files()))


async def test_remove_non_exist_file():
    with pytest.raises(FileNotFound):
        await remove_file(-1)


async def test_presentation_info():
    file = "./assets/test_files/file.pptx"

    f = await upload(
        FileUpload(
            filename="presentation.pptx", read=(await aiofiles.open(file, "rb")).read
        )
    )

    r = await get_slides_info(f.id)

    assert list(map(lambda x: x.dict(), r)) == [
        {
            "image_path": os.path.relpath(STORAGE_PRESENTATION_IMAGES, STORAGE)
            + f"/{f.id}-01.png",
            "comment": "First slide comments",
        },
        {
            "image_path": os.path.relpath(STORAGE_PRESENTATION_IMAGES, STORAGE)
            + f"/{f.id}-02.png",
            "comment": "Second slide comments",
        },
    ]


async def test_presentation_info_not_pptx():
    f = await upload(
        FileUpload(
            filename="some.txt", read=(await aiofiles.open("/dev/null", "rb")).read
        )
    )

    with pytest.raises(FileNotFound):
        await get_slides_info(f.id)


async def test_presentation_info_bad_file():
    f = await upload(
        FileUpload(
            filename="some.pptx", read=(await aiofiles.open("/dev/null", "rb")).read
        )
    )

    with pytest.raises(BadFile):
        await get_slides_info(f.id)
