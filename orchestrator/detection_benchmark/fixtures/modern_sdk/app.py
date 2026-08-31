"""Minimal service using modern from-import SDK style (the DL-027 blind spot)."""
from anthropic import Anthropic
from deepface import DeepFace

client = Anthropic()


def verify_face(img_a: str, img_b: str) -> bool:
    return DeepFace.verify(img_a, img_b)["verified"]


def summarize(text: str) -> str:
    msg = client.messages.create(
        model="claude-sonnet-5", max_tokens=256,
        messages=[{"role": "user", "content": text}],
    )
    return msg.content[0].text
