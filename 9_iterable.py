"""
파이썬에는 반복 가능한 객체가 있다.
리스트, 퓨틀, 셋, 딕셔너리 등은 원하는 구조의 데이터를 보유할 수 있을 뿐 아니라 
for 루프를 통해 값을 반복적으로 가져올 수 있다.

하지만 이와같은 내장 반복형 객체만 for 루프에서 사용 가능한 것이 아니다.
반복을 위해 정의한 로직을 사용해 자체 커스터마이징 이터러블을 만들 수도 있는데,
엄밀히 말하면 이터러블은 __iter__ 매직 메서드를 구현한 객체,
이터레이터는 __next__ 매직 메서드를 구현한 객체를 말한다.

파이썬의 반복은 이터러블 프로토콜이라는 자체 프로토콜을 사용해 동작한다.
for e in myobjecc: 형태로 개체를 반복할 수 있는지 확인하기 위해
파이썬은 고수준에서 다음 두 가지를 차례로 검사한다.
1. 객체가 __next__나 __iter__ 이터레이터 메서드 중 하나를 포함하는지 여부
2. 객체가 시퀀스이고 __len__, __getitem__을 모두 가졌는지 여부

즉 fullback mechanism(만일을 대비해 준비한 절차)으로 시퀀스도 반복을 할 수 있으므로
for 루프에서 반복 가능한 객체를 만드는 방법은 두가지가 있다.

객체를 반복하려고 하면 파이썬은 iter() 함수를 호출한다.
이 함수가 하는 것은 
1. 해당 객체에 __iter__ 메서드가 있는지를 확인
2. __iter__ 메서드를 실행
이다.
"""

from datetime import timedelta, date

class DateRangeIterable:
    """ 자체 이터레이터 메서드를 가지고 있는 이터러블 """

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self._present_day = start_date

    def __iter__(self):
        return self

    def __next__(self):
        if self._present_day >= self.end_date:
            raise StopIteration
        today = self._present_day
        self._present_day += timedelta(days=1)
        return today

for day in DateRangeIterable(date(2019, 1, 1), date(2019, 1, 5)):
    print(day)
"""
2019-01-01
2019-01-02
2019-01-03
2019-01-04
"""

"""
위 객체는 해당 기간의 날짜를 반복하면서 하루 간격으로 날짜를 표시한다.
for 루프는 앞서 만든 객체를 사용해 새로운 반복을 시작한다.
파이썬은 iter() 함수를 호출 -> __iter__ 매직 메서드 호출

__iter__ 메서드는 self를 반환하고 있으므로 객체 자신이 이터러블임을 나타낸다.

따라서 루프의 각 단계에서마다 
자신의 next() 함수를 호출 -> __next__ 매직 메서드에게 위임

__next__ 메서드는 요소를 어떻게 생산하고 하나씩 반한할 것인지 결정하고
더이상 생산할 것이 없을 경우 StopIteration 예외를 발생시켜 알려줘야 한다

for 루프가 작동하는 원리는 StopIteration 예외가 발생할 때까지 next()를 호출하는 것과 같다.

위 예제의 문제점이 하나 있다.
한번 실행하면 끝의 날짜에 도달한 상태이므로 이후에 호출하면 계속 StopIteration 예외가 발생하는 것이다.

만약 두 개의 for루프에서 이 값을 사용하면 첫 번째 루프만 작동하고 두번째 루프는 작동안한다.
아래의 예시는 오류가 날 것이다.
"""

r1 = DateRangeIterable(date(2019, 1, 1), date(2019, 1, 5))
print(", ".join(map(str, r1))) # 2019-01-01, 2019-01-02, 2019-01-03, 2019-01-04

# print(max(r1)) 
# max() arg is an empty sequence
print("---" * 30)
"""
위 문제가 발생하는 이유는 반복 프로토콜이 작동하는 방식 때문이다.
이터러블 객체는 이터레이터를 생성하고 이것을 사용해 반복을 한다.
위 예제에서 __iter__는 self를 반환했지만 호추로딜때마다 새로운 이터레이터를 만들 수 있다.

이 문제를 해결하는 한가지 방법은 매번 새로운 DateRangeIterable 인스턴스를 만드는 것이다.
이것도 그리 나쁜 방법은 아니지만
__iter__에서 제너레이터(이터레이터 객체)를 사용할 수도 있다.

달라진 점은 각각의 for 루프는 __iter__를 호출하고 __iter__는 다시 제너레이터를 생성한다는 것이다.
이러한 형태의 객체를
"컨테이너 이터러블(container iterable)"
이라고 한다.
"""

class DateRangeIterable2:
    """ 자체 이터레이터 메서드를 가지고 있는 이터러블 """

    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def __iter__(self):
        current_day = self.start_date
        while current_day < self.end_date:
            yield current_day
            current_day += timedelta(days=1)

r2 = DateRangeIterable2(date(2019, 1, 1), date(2019, 1, 5))
print(", ".join(map(str, r2))) # 2019-01-01, 2019-01-02, 2019-01-03, 2019-01-04
print(max(r2)) # 2019-01-04