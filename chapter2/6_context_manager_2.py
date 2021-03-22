"""
앞의 예제를 컨텍스트 관리자를 구현하고자 한다.
__enter__ 와 __exit__ 매직 메서드를 구현하면 컨텍스트 관리자 프로토콜을 지원할 수 있다.
이렇게 구현하는 것이 일반적인 방법이지만 유일하지는 않다고 한다.

여러 방법을 살펴보고자 한다.
"""
import contextlib

def stop_database():
    run("systemctl stop postgresql.service")

def start_database():
    run("systemctl start postgresql.service")

def db_backup():
    run("pg_dump database")

@contextlib.contextmanager
def db_handler():
    stop_database()
    yield
    start_database()

with db_handler():
    db_backup()
"""
함수에 contextlib.contextmanager 데코레이터를 적용하면 해당 함수의 코드를 컨텍스트 관리자로 변환한다.
함수는 "제너레이터"라는 특수한 함수의 형태여야 하는데 이 함수는 코드의 문장을 __enter__와 __exit__ 메서드로 분리힌다.
위 db_handler() 함수는 yield 문을 사용했으므로 제너레이터 함수가 된다.
@의 데코레이터를 적용하면 yield 문 앞의 모든 것은 __enter__ 메서드의 일부처럼 취급된다.
__enter__ 메서드의 반환 값과 같은 역할을 하는 것으로 as x: 와 같은 형태로 변수에 할당할 수 있다.
(위 경우에는 아무것도 반환하지 않음, 암묵적으로 None을 반환하는 것과 같다)

이 지점에서 제너레이터 함수가 중단되고 컨텍스트 관리자로 진입하여 데이터베이스의 백업 코드가 실행된다.
이 작업이 완료되면 다음 작업이 이어서 실행되므로 yield 문 다음에 오는 모든 것들을 __exit__ 로직으로 볼 수 있다.

컨텍스트 매니저를 작성하면 기존 함수를 리팩토링하기 쉬운 장점이 있다.
'어느 특정 객체에도 속하지 않은 컨텍스트 관리자가 필요한 경우 좋은 방법'이라고 하는데 무슨 소리인지는 잘 모르겠다....
매직 메서드를 추가하면
- 업무 도메인에 보다 얽히게 됨
- 책임이 커짐
- 하지 않아도 될 것들을 지원해야만 함

이런 문제가 있기에 많은 상태를 관리할 필요가 없고, 
다른 클래스와 독립되어 있는 컨텍스트 관리자 함수를 만드는 경우에는
이렇게 하는 것이 좋다고 한다.
"""

class dbhandler_decorator(contextlib.ContextDecorator):
    def __enter__(self):
        stop_database()
    
    def __exit__(self, ext_type, ex_value, ex_traceback):
        start_database()

@dbhandler_decorator
def offline_backup():
    run("pg_dump database")

"""
또 다른 도우미 클래스로 contextlib.ContextDecorator가 있다.
이 클래스는 컨텍스트 관리자 안에서 실행될 함수에 데코레이터를 적용하기 위한 로직을 제공하는 믹스인 클래스이다.
(믹스인: 다른 클래스에서 필요한 기능만 섞어서 사용할 수 있도록 메서드만을 제공하는 유틸리티 클래스)

반면에 컨텍스트 관리자 자체의 로직은 __enter__, __exit__의 매직 메서드를 구현하여 제공해야 한다.

이전 예제와 다른 점으로는 with문이 없다는 것이다. 그저 함수를 호출하기만 하면 offline_backup() 함수가
컨텍스트 관리자 안에서 자동으로 실행된다.

이 접근법의 단점은
- 완전이 독립적이다.
라는 것이다.

이것은 오히려 좋은 특성인데 데코레이터는 함수에 대해 아무것도 모르고 그 반대도 마찬가지라고 한다.
하지만 컨텍스트 관리자 내부에서 사용하고자 하는 객체를 얻을 수 없다는 점도 있다.

예를들어 with offline_backup() as bp: 처럼 __enter__ 메서드가 반환한 객체를 사용해야 하는 경우
이전의 예제 접근방식을 선택해야 한다.

데코레이터로서의 이점 역시 그대로
- 로직을 한번만 정의하면 동일한 로직을 필요로 하는 함수에 적용 가능
- 재사용 가능
이다.
"""

import contextlib

with contextlib.suppress(DataConversionException):
    parse_data(input_json_or_dict)

"""
contextlib.suppress는 컨텍스트 관리자에서 사용하는 util 패키지로,
제공한 예외 중 하나가 발생한 경우에는 실패하지 않도록 한다.
try, except 블록에서 코드를 실행하고 예외를 전달하거나 로그를 남기는 것은 비슷하지만,
차이점은 suppress 메서드를 호출하면 로직에서 자체적으로 처리하고 있는 예외임을 명시한다는 점이다.

DataConversionException은 입력 데이터가 기대한 것과 같은 포맷이어서 무시해도 안전하다는 것을 뜻한다.
"""