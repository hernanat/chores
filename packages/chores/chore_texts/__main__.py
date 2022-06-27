import datetime
import json
import os
from twilio.rest import Client

CHORES = {
    "living_room": """
    0.) "The floor" includes both the living room and the hallway!!!
    1.) Sweep the floor.
    2.) Run Mr. Robot.
    3.) Clean the floor with a wet wipe on the swiffer.
    4.) Wipe down the table with clorox wipes.
    5.) Clean the dust off of the TV stand.
    """,
    "bathroom": """
    1.) Sweep the floor.
    2.) Run Mr. Robot.
    3.) Clean the floor with a wet wipe on the swiffer.
    4.) Clean the counter and the sink with clorox wipes.
    5.) Clean the mirror with windex.
    6.) Clean the toilet
    7.) Clean (scrub) the shower & make sure the cleaning products go down the drain
        because our shower doesn't really drain well.
    """,
    "kitchen": """
    1.) Sweep the floor.
    2.) Run Mr. Robot.
    3.) Clean the floor with a wet wipe on the swiffer.
    4.) Clean all counter tops with clorox wipes.
    5.) Clean the stove top
    6.) Clean out any crumbs / food residue from inside the stove
    7.) Clean the microwave.
    8.) Load / Unload the dishwasher.
    """
}


def main(args):
    people = json.loads(os.getenv("PEOPLE", "{}"))

    if len(people) == 0:
        return {"body": {}}

    today = datetime.date.today()
    week = today.isocalendar().week

    chore_assignments = make_chore_assignments(people, week)

    send_chore_texts(chore_assignments)

    return {
        "body": {
            assignment[0]: assignment[2] for assignment in chore_assignments
        }
    }


def send_chore_texts(chore_assignments):
    twilio_client = Client(os.getenv("TWILIO_ACCOUNT_SID"),
                           os.getenv("TWILIO_AUTH_TOKEN"))

    for person, phone, chore in chore_assignments:
        twilio_client.messages.create(
            to=phone,
            from_=os.getenv("TWILIO_PHONE_NUMBER"),
            body=f'Hey {person.capitalize()}, you are in charge of the ' +
            f'{chore.replace("_", " ")} this week! Here is what you need to do:\n' +
            CHORES[chore]
        )


def make_chore_assignments(people, week):
    return [
        (person, phone, list(CHORES.keys())[(i + week) % len(CHORES)])
        for i, (person, phone) in enumerate(people.items())
    ]
