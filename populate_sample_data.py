from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from datetime import datetime

from db import get_session
from db.models import Channels, Posts, Replies

import uuid

async def create_sample_data(db: AsyncSession):
    channel_1 = Channels(external_id="channel_001", name="Automotive News")
    db.add(channel_1)
    await db.commit()
    await db.refresh(channel_1)

    post_1 = Posts(
        external_id="post_001", 
        name="New Car Launch Update",
        content="The launch of the Speedster 3000 model is progressing. Final design is complete.",
        channel_id=channel_1.id
    )
    db.add(post_1)
    await db.commit()
    await db.refresh(post_1)

    reply_1 = Replies(external_id="reply_001", content="When will the Speedster 3000 be available for purchase?", post_id=post_1.id)
    reply_2 = Replies(external_id="reply_002", content="Can we schedule a test drive soon?", post_id=post_1.id)
    reply_3 = Replies(external_id="reply_003", content="Excited to see this car! Any launch events planned?", post_id=post_1.id)
    reply_4 = Replies(external_id="reply_004", content="How much will the Speedster 3000 cost?", post_id=post_1.id)
    reply_5 = Replies(external_id="reply_005", content="Can we expect any advanced tech features like autonomous driving?", post_id=post_1.id)
    reply_6 = Replies(external_id="reply_006", content="What colors will the Speedster 3000 come in?", post_id=post_1.id)
    reply_7 = Replies(external_id="reply_007", content="Will there be a special edition version available?", post_id=post_1.id)
    reply_8 = Replies(external_id="reply_008", content="Will there be an option for a hybrid engine?", post_id=post_1.id)
    reply_9 = Replies(external_id="reply_009", content="Can we get more information on the interior features?", post_id=post_1.id)

    db.add_all([reply_1, reply_2, reply_3, reply_4, reply_5, reply_6, reply_7, reply_8, reply_9])
    await db.commit()

    print("Sample data has been added successfully.")

async def add_new_replies(db: AsyncSession, post_id : int, reply_list):
    reply_objects = [Replies(external_id=str(uuid.uuid4()), content=reply, post_id=post_id) for reply in reply_list]
    db.add_all(reply_objects)
    await db.commit()


async def run_script():
    async for db in get_session():
        await create_sample_data(db)

async def update(post_id, reply_list):
    async for db in get_session():
        await add_new_replies(db, post_id, reply_list)

if __name__ == "__main__":
    import asyncio

    new_replies = [
            "Will the Speedster 3000 be available globally at launch?",
            "Are there any special features for the interior of the new model?",
            "Will there be a loyalty discount for existing customers?",
            "Can we get more details about the car's fuel efficiency?",
            "How soon can we pre-order the Speedster 3000?"
        ]
    post_id = 3
    
    state = 1
    if state == 0:
        asyncio.run(run_script())
    if state == 1:
        asyncio.run(update(post_id, new_replies))
