import json, time, urllib.request

payload = {
    "animal_type": "dog",
    "pet_name": "테스트",
    "pet_breed": "말티즈",
    "pet_age": 8,
    "predictions": {
        "백내장": {"label": "유", "confidence": 87.5},
        "결막염": {"label": "유", "confidence": 64.2},
        "유루증": {"label": "무", "confidence": 22.1},
        "안검염": {"label": "무", "confidence": 15.3},
        "궤양성각막질환": {"label": "무", "confidence": 8.7},
    },
}

for i in range(3):
    req = urllib.request.Request(
        "http://127.0.0.1:8000/api/ai/report",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=120) as res:
            body = json.loads(res.read())
        print(f"[{i+1}회] {time.time() - start:.1f}초 / 요약: {body['summary'][:40]}...")
    except Exception as e:
        print(f"[{i+1}회] 실패 ({time.time() - start:.1f}초): {e}")