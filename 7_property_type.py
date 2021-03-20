"""
파이썬 객체의 모든 프로퍼티와 함수는 public이다.(타 언어처럼 private, protected 프로퍼티 X)
즉 호출자가 객체의 속성을 호출하지 못하도록 할 방법이 없다.

하지만 _ 즉 밑줄로 시작하는 속성은 해당 객체에 대해 private을 의미하며,
강제하지는 못하지만 외부에서 호출하지 않기를 기대하는 것이다.
"""

"""
파이썬에서의 밑줄

아래 예제 Connector 객체는 source로 생성되며 source, timeout이라는 두개의 속성을 가진다.
실제 후자는 private이지만 두개 속성에 모두 접근 가능하다.

_timeout은 connector 자체에서만 사용되고 바깥에서는 호출되지 않아서 동일한 인터페이스를 유지하므로
언제든 필요한 경우에 안전하게 리팩토링 될수 있어야 한다.
이러한 규칙을 준수하면 객체의 인터페이스를 유지하였으므로
- 유지보수가 쉽다
- 보다 견고한 코드를 작성할 수 있다
라는 점이 있다.
"""
class Connector:
    def __init__(self, source):
        self.source = source
        self._timeout = 60

conn = Connector("postgresql://localhost")
print(conn.source) # postgresql://localhost
print(conn._timeout) # 60
print(conn.__dict__) # {'source': 'postgresql://localhost', '_timeout': 60}
print("---" * 30)


"""
동일한 원칙이 메서드에도 적용된다.

그러나 일부 속성과 메서드를 실제로 private으로 만들 수 있다는 오해는 정말 오해이다.
일부 개발자는 아래 예제와 같이 __ 밑줄 2개를 사용하여 다른 객체가 수정할 수 없다고 생각하는 경우가 있지만
Attribute 에러는 말 그대로 속성이 존재하지 않는다는 뜻이지 'private'이나 '접근 불가'를 말하는 것이 아니다.
이것은 실제로 부작용에 의한 결과로 생긴 것이라는 의미를 암시한다.

밑줄 두개를 사용하면 
"이름 맹글링(name mangling). 이것이 하는 일은 _<class_name>__<attribute_name> 속성 생성"
이다.
이러한 속성은 아래 예제를 기준으로
conn._Connector__timeout 으로 접근할 수 있다.

때문에 AttributeError가 발생한 것이다.
파이썬에서 __ 밑줄 2개를 사용하는 경우는 완전히 다른 경우인데,
여러 번 확장되는 클래스의 메서드를 이름 충돌 없이 "오버라이드" 하기 위해 만들어진 것이다.

속성을 private으로 정의하려는 경우(강제성은 없지만)
하나의 밑줄을 사용하는 것이 파이썬스러운 것이다.
"""
class Connector:
    def __init__(self, source):
        self.source = source
        self.__timeout = 60

    def connect(self):
        print("connecting with {0}s".format(self.__timeout))

conn = Connector("postgresql://localhost")
conn.connect() # connecting with 60s
print(conn.__timeout) 
# Traceback (most recent call last):
#   File "/Users/wooogy-dev/dev/python-clean-code/7_property_type.py", line 47, in <module>
#     print(conn.__timeout)
# AttributeError: 'Connector' object has no attribute '__timeout'

print(conn._Connector__timeout) # 60