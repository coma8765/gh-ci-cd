from starlette import status

from app.settings import STORAGE_PRESENTATION_IMAGES


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
    refs = [
        (await client.post(
            "/files",
            files={"file": (f"some-file-{i}.txt", open("/dev/null", "rb"))}
        )).json()
        for i in range(10)
    ]

    r = await client.get("/files")
    assert r.status_code == status.HTTP_200_OK

    data = r.json()

    list_files = dict(((i["id"], i) for i in data))

    for ref in refs:
        assert list_files[ref["id"]] == ref


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


async def test_presentation_info(client):
    file = "./assets/test_files/file.pptx"
    file_id = (await client.post(
        "/files",
        files={"file": ("some-file.pptx", open(file, "rb"))},
    )).json()['id']

    r = await client.get(f"/files/slides?file_id={file_id}")

    assert r.status_code == status.HTTP_200_OK

    assert r.json() == [{
        "image_path": f"{STORAGE_PRESENTATION_IMAGES}/{file_id}-00.jpg",
        "comment": "First slide comments"
    }, {
        "image_path": f"{STORAGE_PRESENTATION_IMAGES}/{file_id}-01.jpg",
        "comment": "Second slide comments"
    }]