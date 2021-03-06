"""
index와 slice는 __getitem__ 이라는 매직 메서드 덕에 동작한다.
이는 sample[key] 같은 형태에서 key에 해당하는 값을 파라미터롤 전달한다.
시퀀스 같은 경우에는 __getitem__, __len__을 모두 구현하는 객체이므로 반복이ㄱ 가능하다.
리스트, 튜플, 문자열은 표준 라이브러리에 있는 시퀀스 객체의 예라고 한다.

시퀀스나 이터러블 객체를 만들지 않고 키로 객체의 특정 요소를 가져오는 방법에 대해 다루고자 한다.

사용자정의 클래스에 __getitem__을 구현하려는 경우 고려해야할 점
- 클래스가 표준 라이브러리 객체를 감사는 래퍼인 경우 기본 객체에 많은 동작 위임 가능
- 즉 클래스가 리스트의 래퍼인 경우 리스트의 동일한 메서드를 호출하여 호환성 유지 가능
"""
class Items:
    def __init__(self, *values):
        self._values = list(values)
    
    def __len__(self):
        return len(self._values)
    
    def __getitem__(self, item):
        return self._values.__getitem__(item)

items = Items(1, 2, 3)
print(items.__len__()) # 3
print(items.__getitem__(1)) # 2

"""
위 예제는 캡슐화 방식을 사용함
다른 방법으로 collections.UserList 부모 클래스를 상속하여 사용할 수도 있다.

그러나 만약 래퍼도 아니고 내장 객체를 사용하지도 않은 경우는 자신만의 시퀀스를 구현할 수 있다.
이때 주의할 점은 아래와 같다.
- 범위로 인덱싱하는 결과는 해당 클래스와 같은 타입의 인스턴스여야 한다.(원본 객체와 동일한 타입)
- slice에 의해 제공된 범위는 파이썬이 하는 것처럼 마지막 요소는 제외해야 한다.(일관성에 관한 것)
"""
