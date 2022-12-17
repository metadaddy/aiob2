import os
import pytest
from pathlib import Path

from aiob2 import Client

path = Path(__file__).resolve().parent / 'payloads/test_image.jpg'
bucket_id = os.environ['BUCKET_ID']


class TestB2Actions:
    @pytest.mark.asyncio
    async def test_actions(self):
        client = Client(os.environ['KEY_ID'], os.environ['KEY'])

        # Upload

        file = await client.upload_file(
            content_bytes=path.read_bytes(),
            content_type='image/jpeg',
            file_name='test.jpg',
            bucket_id=bucket_id,
        )

        assert file.name == 'test.jpg'
        assert file.bucket_id == bucket_id
        assert file.content_type == 'image/jpeg'

        # Download (by name)

        downloaded_file = await client.download_file_by_name(file_name=file.name, bucket_name=os.environ['BUCKET_NAME'])

        assert downloaded_file.name == file.name
        assert downloaded_file.id == file.id
        # assert downloaded_file.upload_timestamp == file.upload_timestamp
        assert downloaded_file.content == path.read_bytes()

        # Download (by id)

        downloaded_file = await client.download_file_by_id(file_id=file.id)

        assert downloaded_file.name == file.name
        assert downloaded_file.id == file.id
        # assert downloaded_file.upload_timestamp == file.upload_timestamp
        assert downloaded_file.content == path.read_bytes()

        # Delete

        deleted_file = await client.delete_file(file_name=file.name, file_id=file.id)

        assert deleted_file.name == file.name
        assert deleted_file.id == file.id

        await client.close()
