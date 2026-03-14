from __future__ import annotations

import asyncio

from yandex_cloud_ml_sdk import AsyncYCloudML

import config as cg


async def YaGPT_text(req, model_name):
    message = [
        {
            "role": "user",
            "text": req,
        },
    ]

    sdk = AsyncYCloudML(
        folder_id=cg.YAGPT_CATALOG_ID,
        auth=cg.YAGPT_API_KEY,
    )

    model = sdk.models.completions(model_name)

    operation = await (
        model.configure(temperature=0.5).run_deferred(message)
    )

    status = await operation.get_status()
    while status.is_running:
        await asyncio.sleep(1)
        status = await operation.get_status()

    result = await operation.get_result()

    return {
        'text': result.alternatives[0].text,
        'total_tokens': result.usage.total_tokens
    }


async def get_orientation(req):
    if req == 'Книжная':
        width_ratio = 1
        height_ratio = 2
    if req == 'Альбомная':
        width_ratio = 2
        height_ratio = 1
    return {
        "width_ratio": width_ratio,
        "height_ratio": height_ratio
    }


async def YaGPT_image(req, model_name, orientation):

    sdk = AsyncYCloudML(
        folder_id=cg.YAGPT_CATALOG_ID,
        auth=cg.YAGPT_API_KEY,
        )

    model = sdk.models.image_generation(model_name)

    orient = await get_orientation(orientation)

    model = model.configure(
        width_ratio=orient['width_ratio'],
        height_ratio=orient['height_ratio'],
        seed=50
        )

    operation = await model.run_deferred(req)

    status = await operation.get_status()

    while status.is_running:
        await asyncio.sleep(1)
        status = await operation.get_status()

    result = await operation.get_result()

    return {
        'image': result,
        'total_tokens': 1
    }