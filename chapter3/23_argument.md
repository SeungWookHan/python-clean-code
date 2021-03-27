## 함수와 메서드의 인자

파이썬은 여러 가지 방법으로 인자를 받도록 함수를 정의할 수 있음  
또한 소프트웨어 엔지니어링에서 함수의 인자를 정의하는 것과 관련한 관행이 있음

### 파이썬의 함수 인자 동작방식

#### 인자는 어떻게 함수에 복사되는가?

파이썬의 첫 번째 규칙은 모든 인자가 값에 의해 전달(passed by a value)된다는 것이다.  
함수에 값을 전달하면 함수의 서명에 있는 변수에 할당하고 나중에 사용한다.  
인자를 변경하는 함수는 인자의 타입에 따라 다른 결과를 낼 수 있다.  
만약 mutable(변형 가능한) 객체를 전달하고 함수에서 해당 값을 변경하면 실제 값이 변경되는 부작용이 생길 수 있다.

```
def function(arg):
    arg += " in function"
    print(arg)

immutable = "hello"
function(immutable)
# hello in function
immutable
# hello

mutable = list("hello")
function(mutable)
# ['h', 'e', ..., 'f', 'u', ..., 'n']
mutable
# ['h', 'e', ..., 'f', 'u', ..., 'n']
```

첫 번째 예시인 문자열을 전달하면 함수의 인자에 할당한다.  
string 객체는 immutable(불변형) 타입이므로 "arg += in function" 문장은 새로운 객체를 만들어서 arg에 다시 할당한다.  
이 시점에서 arg는 단지 함수 스코프 내에 있는 로컬 변수이며 원래 변수와는 아무 관련이 없다.

반면 mutable 객체는 list를 전달하면 해당 문장은 list의 extend()를 호출하는 것과 같다.  
원래 리스트 객체에 대한 참조를 보유하고 있기에 함수 외부에 있는 실제 값이 변경된다.  
그렇기에 이러한 방식으로 변경하는 것은 가급적 피하고 다른 대안을 찾아야 한다고 한다.  
(절대적으로 옳은 상황이 아니라면....)  
`함수 인자를 변경하지 않아야 함. 최대한 함수에서 발생할 수 있는 부작용을 회피해야 함`

파이썬의 인자는 다른 프로그래밍 언어와 마찬가지로

- 위치에 기반을 두어 호출
- 키워드에 기반을 두어 호출
  두가지가 가능하다.  
  키워드 인자에 의한 호출은 오로지 명시적으로 파라미터를 지정해야 한다는 것을 의미한다.  
  또한 유일한 주의 사항은 이후의 파라미터도 반드시 키워드 인자 방식으로 호출돼야 한다는 점이다.  
  (그렇지 않으면 SyntaxError 발생)

---

#### 가변인자

파이썬은 다른 언어와 마찬가지로 가변 인자를 사용 가능하다.  
가변 인자 함수를 위한 몇 가지 권장사항과 기본 원칙을 배우고자 한다.  
가변 인자를 사용하려면 해당 인자를 패킹할 변수 앞에 별표(\*)를 사용한다.  
각 인자 요소에 list[0], list[1] ... 으로 전달하는 것은 전혀 파이썬스러운 코드가 아니라고 한다.

```
def f(first, second, third):
    print(first)
    print(second)
    print(third)

l = [1, 2, 3]
f(*l)
# 1
# 2
# 3
```

패킹 기업의 장점은 다른 방향으로도? 동작한다는 것이다.  
리스트 값을 각 위치별로 변수에 언패킹하려면 다음과 같이 할 수 있다.

```
a, b, c = [1, 2, 3]
```

부분적인 언패킹도 가능하다.  
시퀀스(or 리스트 or 튜플)의 첫 번째 값과 나머지에만 관심이 있다고 가정해보자.  
이런 경우 첫번째를 필요한 변수를 할당하고 나머지는 리스트로 패킹할 수 있다고 한다.  
언패킹하는 순서는 제한이 없고,  
언패킹할 부분이 없다면 결과는 비어있게 된다고 한다.

```
# 제너레이터와 언패킹 예제
def show(e, rest):
    print("요소: {0} - 나머지: {1}".format(e, rest))

first, *rest = [1, 2, 3, 4, 5]
show(first, rest)
# 요소: 1 - 나머지 [2, 3, 4, 5]

*rest, last = range(6)
show(last, rest)
# 요소 5 - 나머지: [0, 1, 2, 3, 4]

first, *middle, last = range(6)
first
# 0
middle
# [1, 2, 3, 4]
last
# 5

first, last, *empty = (1, 2)
first
# 1
last
# 2
empty
# []
```

변수 언패킹의 가장 좋은 사용 예는 반복이다.

1. 일련의 요소를 반복해야 하고
2. 각 요소가 차례로 있다면  
   각 요소를 반복할 때 언패킹하는 것이 좋다고 한다.

다음은 데이터를 받아서 사용자를 생성하는 예제이다.

```
USERS = [(i, f"first_name_{i}", "last_name_{i} ") for i in range(1_000)]

class User:
    def __init__(self, user_id, first_name, last_name):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name

    def bad_users_from_rows(dbrows) -> list:
        """ DB 레코드에서 사용자를 생성하는 파이썬스럽지 않은 잘못된 예 """
        return [User(row[0], row[1], row[2]) for row in dbrows]

    def users_from_rows(dbrows) -> list:
        """ DB 레코드에서 사용자 생성 파이썬스러운 예 """
        return [
            User(user_id, first_name, last_name)
            for (user_id, first_name, last_name) in dbrows
        ]

```

두 번째 버전이 훨씬 가독성이 좋다.
첫 번째 버전인 bad_users_from_rows 함수에서는 row[0], row[1], row[2]가 무엇을 뜻하는지 전혀 알 수가 없다.  
반면 user_id, first_name, last_name는 직관적이다.  
자체 함수를 디자인할때 이러한 종류의 기능을 활용할 수 있다.

표준 라이브러리에서의 예는 max 함수에서 발견할 수 있다.

```
max(...)
    max(iterable, *[, default=obj, key=func]) -> value
    max(arg1, arg2, *args, *[, key=func]) -> value
    단일 반복형 인자를 넘기면 그 중에 가장 큰 값을 반환.
    키워드 인자로만 사용할 수 있는 default는 제공된 반복형이 비엇을 때 반환할 값이다.
    2개 이상의 인자가 사용되면 가장 큰 인자를 반환한다.
```

비슷한 표기법으로 이중 별표(\*\*)를 키워드 인자에 사용할 수 있다.  
딕셔너리에 이중 별표를 사용하여 함수에 전달하면 파라미터의 이름으로 키를 사용하고, 파라미터의 값으로 딕셔너리 값을 사용한다.

```
function(**{"key": "value})
이것은 아래와 동일하다.
function(key="value")

반대로 이중 별표로 시작하는 파라미터를 함수에 사용하면 반대 현상이 벌어진다.
키워드 제공 인자들이 딕셔너리로 패킹된다.

def function(**kwargs):
    print(kwargs)

function(key="value")
# {'key': 'value}
```
