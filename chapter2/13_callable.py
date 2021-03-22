"""
호출형 객체

함수처럼 동작하는 객체를 정의하면 매우 편리하다고 한다.
데코레이터가 그 예 중 하나인데 이것만 있는 것이 아니다.

매직 메서드 __call__을 사용하면 객체를 일반 함수처럼 호출할 수 있다고 한다.
전달된 모든 파라미터로 해당 메서드에 그대로 전달된다.

주된 이점은 객체에는 상태가 있기 때문에 함수 호출 사이에 정보를 저장할 수 있다는 ㅈ머이다.
파이썬은 object(*args, **kwargs)같은 구문을
object.__call__(*args, **kwargs)로 변환한다고 한다.

1. 객체를 파라미터가 있는 함수처럼 활용
2. 정보를 기억하는 함수처럼 사용
하는 경우 유용하다.
"""

from collections import defaultdict

class CallCount:
    def __init__(self) -> None:
        self._counts = defaultdict(int)
    
    def __call__(self, argument):
        self._counts[argument] += 1
        return self._counts[argument]

cc = CallCount()
print(cc(1)) # 1
print(cc(2)) # 1
print(cc(1)) # 2
print(cc(1)) # 4
print(cc("something")) # 1

"""
입력된 파라미터와 동일한 값으로 몇 번이나 호출되었는지 반환하는 예제
추후 데코레이터 생성시 이 메서드를 사용하면 편리하다고 한다.
"""