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
print("서버 준비 확인 중...")
for _ in range(60):
    try:
        urllib.request.urlopen("http://127.0.0.1:8000/health", timeout=2)
        print("서버 준비 완료\n")
        break
    except Exception:
        time.sleep(2)
times, passed = [], 0
N = 5

for i in range(N):
    req = urllib.request.Request(
        "http://127.0.0.1:8000/api/ai/report",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=120) as res:
            r = json.loads(res.read())
    except Exception as e:
        print(f"[{i+1}회] 실패: {e}")
        continue
    t = time.time() - start
    times.append(t)

    all_text = r["summary"] + " ".join(r["disease_analysis"].values()) + " ".join(r["precautions"])
    checks = {
        "긴급도": r["visit_urgency"] in ("즉시", "1주 이내"),
        "수의사필요": r["vet_required"] is True,
        "주의사항3개": len(r["precautions"]) == 3,
        "질환3개이하": len(r["disease_analysis"]) <= 3,
    }
    ok = all(checks.values())
    passed += ok
    print(f"[{i+1}회] {t:.1f}초 | 긴급도={r['visit_urgency']} 주의사항={len(r['precautions'])}개 "
          f"'진단' {all_text.count('진단')}회 | {'통과' if ok else '실패: ' + ', '.join(k for k, v in checks.items() if not v)}")

if times:
    print(f"\n평균 {sum(times)/len(times):.1f}초 / 규칙 통과 {passed}/{len(times)}")