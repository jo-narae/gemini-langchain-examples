# -*- coding: utf-8 -*-
"""
Step 2: 도구(Tool) 정의

@tool 데코레이터를 사용하여 커스텀 도구를 정의하는 방법을 학습합니다.
"""

import os
import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.tools import tool
from datetime import datetime
import pytz

# 환경설정
project_root = Path(__file__).parent.parent
load_dotenv(project_root / ".env")

print("=" * 70)
print("Step 2: 도구(Tool) 정의")
print("=" * 70)
print()

# 커스텀 도구 정의
@tool
def get_current_time(timezone: str, location: str) -> str:
    """현재 시각을 반환하는 함수
    
    Args:
        timezone (str): 타임존 (예: 'Asia/Seoul') 실제 존재하는 타임존이어야 함
        location (str): 지역명. 타임존이 모든 지명에 대응되지 않기 때문에 이후 llm 답변 생성에 사용됨
    """
    try:
        tz = pytz.timezone(timezone)
        now = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
        location_and_local_time = f'{timezone} ({location}) 현재시각 {now}'
        print(f"🕐 시간 조회: {location_and_local_time}")
        return location_and_local_time
    except Exception as e:
        error_msg = f"시간 조회 실패: {str(e)}"
        print(f"❌ {error_msg}")
        return error_msg

# 도구 정보 확인
print("📋 도구 정보:")
print(f"   이름: {get_current_time.name}")
print(f"   설명: {get_current_time.description}")
print()

# 도구 직접 호출 테스트
print("🧪 도구 직접 호출 테스트:")
result = get_current_time.invoke({"timezone": "Asia/Seoul", "location": "서울"})
print(f"   결과: {result}")
print()

