import base64
from openai import OpenAI
import os
from io import BytesIO
from PIL import Image

client = OpenAI(
    api_key='sk-svcacct-6Qr1cyZrWfWZe9bMFDBYT3BlbkFJHJPnxAKgqo6ErrWSTPfF'
)


def __parse_result_message(message):
    result_dict = {}
    section = None
    lines = message.split("\n")
    for line in lines:
        if not line:
            continue

        if line[-1] == ':':
            section = line[:-1].upper()
            result_dict[section] = []
            continue

        if section is None:
            continue

        result_dict[section].append(line)

    return result_dict


def parse_gauge_img(result_img, gauge_type):
    with Image.open(result_img) as pil_img:
        if pil_img.height > pil_img.width:
            rot_img = pil_img.transpose(Image.ROTATE_90)
            pil_img = rot_img
        buffered = BytesIO()
        pil_img.save(buffered, format="JPEG")
        encoded_img = base64.b64encode(buffered.getvalue()).decode('utf-8')

    if gauge_type == 'MyChron5':
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        """
                        This is a image of the screen of a gauge. The content in the image are organized in 2 tables.
                        The 2nd table has 5 columns: "LAP", "Best Laps", "RPM", "MPH", and "ET1 MAX". Please first give me
                        the 3 numbers under column "LAP". Then give me the 3 numbers under
                        column "Best Laps". Then give me the 6 numbers under column "RPM". Then give me the 6 numbers
                        under column "mph". Finally please give me the 6 numbers under column "EGT".
                        For each column, please print the column name first, then the values under the column. Add ':' 
                        to the end of column name, but don't add any prefix or suffix to the values of each column.
                        """,
                        *map(lambda f: {"image": f, "resize": 768}, [encoded_img]),
                    ],
                },
            ],
            n=1,
        )
        result_dict = __parse_result_message(completion.choices[0].message.content)

    else:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        """
                        In the presented image, there are numbers organized in a table. First, please give me the
                        three numbers under column "LAP". Then give me the three numbers under column "LAP TIME".
                        Then give me the six numbers under column "GPS SPEED". Then give me the six numbers under
                        column "TEMP 1". Lastly, please give me the six numbers under column "RPM".
                        For each column, please print the column name first, then the values under the column. Add ':'
                        to the end of column name, but don't add any prefix or suffix to the values of each column.
                        """,
                        *map(lambda f: {"image": f, "resize": 768}, [encoded_img]),
                    ],
                },
            ],
            n=1,
        )
        result_dict = __parse_result_message(completion.choices[0].message.content)
        print(result_dict)

    return result_dict


