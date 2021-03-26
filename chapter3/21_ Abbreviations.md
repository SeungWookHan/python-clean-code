## 개발지침 약어
- 좋은 소프트웨어 관행을 약어를 통해 쉽게 기억
- 이를 통해 좋은 모범사례와 연결 및 특정 코드에 적합한 아이디어 빠르게 떠올리기 가능  

### DRY/OAOO
- DRY: Do not Repeat Yourself
- OAOO: Once and Only Once
위 둘은 밀접한 관련이 있고 자명한 원리로서 중복을 반드시 피해야함...?  
(위 둘의 중복을 말하는 것이 아닌 코드의 중복을 말하는 것으로 보임)  

코드에 있는 지식은 단 한번, 단 한곳에 정의되어야 한다.  
이를 통해 코드 변경시 수정이 필요한 곳을 단 한군데로 만드는 것이 중요하다.  
그렇지 않다는 것은 잘못된 시스템의 징조이다.  
```
코드 중복 -> 유지보수에 악영향  
- 오류가 발생하기 쉽다: 어떤 로직이 코드 전체에 여러 번 반복되어 있는데 수정을 한다고 해보자. 이때 인스턴스의 하나라도 빠트리면 버그가 발생할 것.  
- 비용이 비싸다: 한번 정의했을 때보다 여러 곳에서 정의했을 경우 변경하는데 더 많은 시간이 소요됨.  
- 신뢰성이 덜어진다: 문맥상 여러 코드를 변경해야하는 경우 사람이 모든 인스턴스의 위치를 기억해야 함.  단일 데이터 소스(single source of truth)가 아니므로 데이터의 완결성이 떨어짐.  
```
중복은 기존 코드의 지식을 무시하거나 잊어버림으로써 발생함  
코드의 특정 부분에 의미를 부여함으로써 해당 지식을 식별하고 표시할 수 있다  

```
# 시험 통과 11점, 시험 통과실패 -5점, 1년 지날때마다 -2점
# 아래는 나쁜 코드의 예  

def process_students_list(students):
    # 중간 생략

    students_ranking = sorted(
        students, key = lambda s: s.passed * 11 - s.failed * 5 - s.years * 2
    )
    # 학생별 순위 출력
    for student in students_ranking:
        print(
            "이름: {0}, 점수: {1}".format(
                student.name,
                (student.passed * 11 - student.failed * 5 - student.years * 2),
            )
        )
```
위 예제의 경우 sorted 함수의 key로 사용된 lambda가 특별한 도메인 지식을 나타내지만 아무런 정의가 없음.  
특별히 할당된 이름의 코드 블록도 없고 어떤 의미도 부여하지 않았기에 순위를 출력하는데 중복 발생  
이와같이 도메인 문제에 대한 지식이 사용된 경우 의미를 부여해야 함으로써 중복을 제거해야함  
```
def score_for_student(student):
    return student.passed * 11 - student.failed * 5 - student.years * 2

def process_students_list(students):
    # 중간 생략

    students_ranking = sorted(students, key=score_for_student)
    # 학생별 순위 출력
    for student in students_ranking:
        print(
            "이름: {0}, 점수: {1}".format(
                student.name, score_for_student(student)
            )
        )
```  
의미를 부여한다는 것은 아무래도 함수로 정의를 함으로써 재사용가능하게 만드는 것 같다.  
위의 예시는 코드 중복의 특징 중 하나를 분석한 것이라고 한다.  
코드 중복에는 더 많은 유형과 분류가 있지만 여기서는 약자에 숨어 있는 특별한 측면에 초점을 맞췄다고 한다.  
중복 제거를 하는 가장 간단한 방법인 ***함수 생성 기법***을 사용했으며 경우에 따라서 최선의 해결책은 달라진다.  
전체적으로 추상화하지 않은 경우 완전히 새로운 객체를 만드는 것이 좋다고 한다.  
(어떤 경우에는 컨텍스트 관리자 사용 가능)  
또한 이터레이터나 제너레이터가 코드의 반복을 피하는데 도움이 될 수 있으며 데코레이터 역시 도움이 될 수도 있다고 한다.  
파이썬에는 명확한 규칙이나 패턴이 없기에 직관이 중요!!!  
---
### YAGNI
- YAGNI: You Ain't Gonna Need it  
이는 과잉 엔지니어링을 하지 않기 위해 솔루션 작성시 계속 염두에 두어야 하는 원칙이다.  
우리는 프로그램을 쉽게 수정하기를 원하므로 ***미래 보장성***이 높기를 바란ㄷ.  
미래의 모든 요구사항을 고려하게 되면  
1. 매우 복잡한 솔루션 만들게 됨
2. 추상화를 하여 읽기 어렵게 됨
3. 유지보수가 어렵게 됨
4. 이해하기 어려운 코드를 만들게 됨
의 문제점이 있다.  
그러나 나중에 예상되는 요구 사항이 나타나지 않거나 동작하긴 하지만 다른 방식으로 동작한다고 가정했을시,  
프로그램을 리팩토링하고 확자앟는 것이 더 어렵다는 것이 있다.  
원래 솔루션이 원래 요구 사항을 올바르게 처리 못했고,  
현재의 요구사항도 제대로 처리하지 못하게 된 것인데,  
이는 순전히 추상화를 잘못했기 때문이다.  

유지보수가 가능한 소프트웨어를 만드는 것은 ***미래의 요구사항을 예측하는 것이 아닌***  
오직 현재의 요구사항을 잘 해결하기 위한 소프트웨어를 작성하고 유지보수가 쉽게 작성하는 것.  
### 즉, 굳이 필요 없는 추가 개발을 하지 말자!!!
---
### KIS
- KIS: Keep It Simple  
이전 원칙과 매우 흡사하다.  
소프트웨어 컴포넌트 설계시 **과잉 엔지니어링**을 피해야 한다.  
솔루션: 문제에 적합한 최소한의 솔루션  

최소한의 기능으로 솔루션을 구현하고 복잡하게 만들면 안된다.  
디자인이 단순해야 유지관리가 쉽다!!  
이 디자인 원칙은 모든 추상화 수준에서 염두에 두어야 할 원칙이다.  
##### 높은 수준
- 정말 모든 기능이 필요할까?
- 이 모듈은 정말 지금 당장 완전히 확장 가능해야 할까?  
어쩌면 우리는 해당 컴포넌트를 확장 가능하게 만들고 싶지만 지금은 적절한 시기가 아니거나,  
적절한 추상화를 작성하기 위한 충분한 정보가 없는 경우가 있다.  
그리고 이 시기에 일반적인 인터페이스를 만든다면 더욱 심각한 문제로 이어질 것이라고 한다.  
##### 코드 측면의 단순함이란?
- 문제에 맞는 가장 작은 데이터 구조 사용(대부분 표준 라이브러리에서 찾을 수 있다고 함)  
때로는 코드를 지나치게 복잡하게 만들고 필요한 것보다 더 많은 함수 또는 메서드를 만들 수 있는데,  
다음의 예시가 그렇다고 한다.  
```
class ComplicateNamespace:
    """ 프로퍼티를 가진 객체를 초기화하는 복잡한 예제 """

    ACCEPTED_VALUES = ("id_", "user", "location)

    @classmethod
    def init_with_data(cls, **data):
        instance = cls()
        for key, value in data.items():
            if key in cls.ACCEPTED_VALUES:
                setattr(instance, key, value)
        return instance
```  
위 클래스는 제공된 키워드 파라미터 세트에서 네임스페이스를 작성하지만 다소 복잡한 코드 인터페이스를 가진다.  
객체를 초기화 하기 위해 추가 클래스 메서드를 만드는 것은 꼭 필요해 보이지 않는다.  
반복을 통해 setattr을 호출하는 것은 상황을 더 이상하게 만든다.  
```
cn = ComplicateNamespace.init_with_data(
    id_=42, user="root", location="127.0.0.1", extra="excluded"
)
cn.id_, cn.user, cn.location  
# (42, "root", "127.0.0.1")  

hasattr(cn, "extra")  
# False
```  
사용자는 초기화를 위해 init_with_data라는 일반적이지 않은 메서드의 이름을 알아야 하는데 이 또한 불편한 부분이다.  
파이썬에서 다른 객체를 초기화 할때는 **__init__** 메서드를 사용하는 것이 훨씬 간편할 것이다.  
```
class Namespace:
    """ Create an object from keyword arguments. """

    ACCEPTED_VALUES = ("id_", "user", "location)

    def __init__(self, **data):
        accepted_data = {
            k: v for k, v in data.items() if k in self.ACCEPTED_VALUES
        }
        self.__dict__.update(accepted_data)
```
---
### EAFP/LBYL
- EAFP: Easier to Ask Forgiveness than Permission, 허락보다는 용서를 구하는 것이 쉽다.
- LBYL: Look Befor You Leap, 도약하기 전에 살피라는 뜻이다.  
```
EAFP는 일단 코드를 실행하고 실제 동작하지 않을 경우에 대응한다는 뜻이다.  
일반적으로는 코드를 실행하고 발생한 예외를 catch하고 except블록에서 바로잡는 코드를 실행하게 된다.  
LBYL은 그 반대이다.  
도약하기 전에 먼저 무엇을 사용하려고 하는지 확인하라는 뜻이다.  
예를 들어 파일을 사용하기 전에 먼저 파일을 사용할 수 있는지 확인하는 것이다.  
(오 뭔가 DbC의 사전조건, 사후조건과 연계되는 느낌.....)  
```
```
if os.path.exists(filename):
    with open(filename) as f:
        ...
```
위 방식은 다른 프로그래밍 언어에서는 유용할 수 있으나 파이썬스러운 방식은 아니라고 한다.  
파이썬은 EAFP 방식으로 만들어졌으며, 이렇게 할것을 권한다고 한다.  
```
try:
    with open(filename) as f:
        ...
except FileNotFoundError as e:
    logger.error(e)
```