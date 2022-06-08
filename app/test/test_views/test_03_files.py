import os

from starlette import status

from app.settings import STORAGE, STORAGE_PRESENTATION_IMAGES

SLIDES_FILE = "./assets/test_files/file.pptx"


async def test_upload_file(client):
    r = await client.post(
        "/files",
        files={"file": ("some-file.txt", open("/dev/null", "rb"))},
    )

    assert r.status_code == status.HTTP_200_OK
    data = r.json()
    assert isinstance(data["id"], int)
    assert data["filename"] == "some-file.txt"


async def test_list_files(client):
    refs = [*[
        (await client.post(
            "/files",
            files={"file": (f"some-file-{i}.txt", open("/dev/null", "rb"))}
        )).json()
        for i in range(10)], *[
        (await client.post(
            "/files",
            files={"file": (f"some-file-{i}.pptx", open(SLIDES_FILE, "rb"))}
        )).json()
        for i in range(10)
    ]]

    r = await client.get("/files")
    assert r.status_code == status.HTTP_200_OK

    data = r.json()

    list_files = dict(((i["id"], i) for i in data))

    for ref in refs:
        assert list_files[ref["id"]] == ref

        if ref["filename"].endswith(".pptx"):
            assert list_files[ref["id"]]["type_addons"]["count_slides"] == 2


async def test_remove_file(client):
    file_id = (await client.post(
        "/files",
        files={"file": ("some-file.txt", open("/dev/null", "rb"))},
    )).json()['id']

    r = await client.delete(f"/files/{file_id}")
    assert r.status_code == status.HTTP_204_NO_CONTENT

    assert list(filter(
        lambda x: x["id"] == file_id,
        (await client.get("/files")).json()
    )) == []


async def test_remove_non_exist_file(client):
    r = await client.delete("/files/-1")
    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert r.json() == {"detail": "Not found"}


async def test_presentation_info(client):
    file_id = (await client.post(
        "/files",
        files={"file": ("some-file.pptx", open(SLIDES_FILE, "rb"))},
    )).json()['id']

    r = await client.get(f"/files/slides?file_id={file_id}")

    assert r.status_code == status.HTTP_200_OK

    assert r.json() == [{
        "image_path":
            os.path.relpath(STORAGE_PRESENTATION_IMAGES, STORAGE) +
            f"/{file_id}-01.png",
        "comment": "First slide comments"
    }, {
        "image_path":
            os.path.relpath(STORAGE_PRESENTATION_IMAGES, STORAGE) +
            f"/{file_id}-02.png",
        "comment": "Second slide comments"
    }]


async def test_presentation_info_not_pptx(client):
    file_id = (await client.post(
        "/files",
        files={"file": ("some-file.txt", open("/dev/null", "rb"))},
    )).json()['id']

    r = await client.get(f"/files/slides?file_id={file_id}")
    assert r.status_code == status.HTTP_404_NOT_FOUND
    assert r.json() == {"detail": "Not found"}


async def test_presentation_info_bad_file(client):
    file_id = (await client.post(
        "/files",
        files={"file": ("some-file.pptx", open("/dev/null", "rb"))},
    )).json()['id']

    r = await client.get(f"/files/slides?file_id={file_id}")
    assert r.status_code == status.HTTP_400_BAD_REQUEST
    assert r.json() == {"detail": "File is damaged"}
