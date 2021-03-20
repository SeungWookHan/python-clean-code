"""
객체에 값을 저장해야 할 경우 일반적인 속성(attribute)을 사용할 수 있다.
객체의 상태나 다른 속성의 값을 기반으로 어떤 계산을 하려 할때 대부분 프로퍼티(property)를 사용하는 것이
좋은 선택이라고 한다.

프로퍼티는 객체의 어떤 속성에 대한 접근을 제어하려는 경우 사용한다
자바 같은 언어에서는 접근 메서드인 게터나 세터를 만들지만(getter, setter) 파이썬에서는 프로퍼티를 사용한다.

책에서 들어준 예는
"사용자가 등록한 이메일에 잘못된 정보가 입력되지 않게 보호하는 경우"
이고 예제는 아래와 같다.
"""

import re

EMAIL_FORMAT = re.compile(r"[^@]+@[^@]+[^@]+")

def is_valid_email(potentially_balid_email: str):
    return re.match(EMAIL_FORMAT, potentially_balid_email) is not None

class User:
    def __init__(self, username):
        self.username = username
        self._email = None

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, new_email):
        if not is_valid_email(new_email):
            raise ValueError(f"유효한 이메일이 아니므로 {new_email} 값을 사용할 수 없음")
        self._email = new_email

u1 = User("han")
u1.email = "han@"
# ...ValueError: 유효한 이메일이 아니므로 han@ 값을 사용할 수 없음

u1.email = "han@g.co"
print(u1.email)
# han@g.co
"""
이메일에 프로퍼티를 사용하여 얻을 수 이점
- 첫 번째 @property 메서드는 private 속성인 email 값을 반환한다.(_ 는 private으로 사용될 것을 말함)
- 두 번째 메서드는 앞에서 정의한 프로퍼티에 @email.setter를 추가한다.
    <user>, email= <new_email>이 실행될 때 호출되는 코드로 <new_email>이 파라미터가 됨
    설정하려는 값이 실제 이메일 주소가 아닌 경우 명확하게 유효성 검사를 한다.
이렇게 하면 get_, set_ 접두어를 사용하여 사용자 메서드를 만드는 것보다 훨씬 더 간단하다.

프로퍼티는 명령-쿼리 분리 원칙(command and query separation - CC08)을 따르기 위한 좋은 방법이다.
위 원칙은 객체의 메서드가 무언가의 상태를 변경하는 커맨드이거나, 무언가의 값을 반환하는 쿼리이거나,
둘 중 하나만 수행해야지 둘 다 동시에 수행하면 안된다는 것이다.

객체의 메서드가 동시에 무언가를 하면서, 질문에 대답하기 위한 상태를 반환한다면 이는 명령-쿼리 분리 원칙을 위배하는 것이다.

메서드 이름에 따라 실제 코드가 무슨 동장을 하는지 혼돈스럽고 이해하기가 어려운 경우가 있다며 저자는 예를 들어준다.
예) set_email이라는 메서드를 if self.set_email("a@j.com") 처럼 사용했다면 무엇을 의미하는 건지 헷갈린다.
    1. a@j.com으로 이메일을 설정하려는 것인지
    2. 이미 이메일이 해당 값으로 설정되어 있는지 확인하는 것인지
    3. 동시에 이메일 값을 설정하고 상태가 유효한지 체크하려는 것인지

@property 데코레이터는 무언가에 응답하기 위한 쿼리이고, @<property_name>.setter는 무언가를 하기 위한 커맨드이다.

+ 한 메서드에서 한 가지 이상의 일을 하지 말자!
무언가를 할당하고 유효성 검사를 하고 싶으면 두 개 이상의 문장으로 나누어야 한다.
"""