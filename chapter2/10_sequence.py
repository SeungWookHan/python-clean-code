"""
객체에 __iter__() 메서드를 정의하지 않았지만 반복하기를 원하는 경우도 있다.
iter() 함수의 동작은 이렇다
1. __iter__ 정의를 찾음
2. 없다면 __getitem__ 을 찾음
3. 없으면 TypeError을 발생 시킴

시퀀스는 __len__과 __getitem__을 구현하고 첫 번째 인덱스 0부터 시작하여 포함된 요소를 한번에 하나씩 차례로 가져올 수 있어야 한다.
즉, __getitem__을 올바르게 구현하는 것에 주의를 기울여야 한다고 한다.
그렇지 않으면 반복이 작동 안한다.

이전 섹션에서 다뤘던 이터러블의 장점은 메모리를 적게 사용한다는 점이다.
한 번에 하나의 날짜만 보관 -> 한번에 하나의 날짜만 생성 한다는 의미이다.
그러나 n번째 요소를 얻고 싶다면 도달할때까지 다시 n번 반복한다는 단점이 있다.(링크드 리스트?!와 개념이 비슷한듯한)
전형적인 "메모리와 CPU 사이의 트레이드오프"이다.

이터러블 사용시 메모리를 적게 사용하지만 n번째 요소를 얻기 위한 시간복잡도는 O(n)

시퀀스로 구현하면 더 많은 메모리가 사용되지만(모든 것을 한번에 보관 하기에) 인덱싱의 시간복잡도는 O(1)
"""

from datetime import timedelta, date

class DateRangeSequence:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self._range = self._create_range()

    def _create_range(self):
        days = []
        current_day = self.start_date
        while current_day < self.end_date:
            days.append(current_day)
            current_day += timedelta(days=1)
        return days

    def __getitem__(self, day_no):
        return self._range[day_no]

    def __len__(self):
        return len(self._range)

s1 = DateRangeSequence(date(2019, 1, 1), date(2019, 1, 5))
for day in s1:
    print(day)
"""
2019-01-01
2019-01-02
2019-01-03
2019-01-04
""" 
print(s1[0]) # 2019-01-01
print(s1[3]) # 2019-01-04
print(s1[-1]) # 2019-01-04

"""
이터러블과 시퀀스 중 어느 것을 사용할지 결정할때 메모리와 CPU 사이의 트레이드오프 계산을 하면 좋다.
일반적으로 이터레이션 그 중 제너레이터 방식이 바람직하지만 모든 경우의 요건을 염두해 둬야 한다.
"""