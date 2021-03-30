## 소프트웨어 디자인 우수 사례 결론

좋은 소프트웨어 디자인이란?

- 소프트웨어 엔지니어링의 우수 사례를 따르고 언어의 기능이 제공하는 대부분의 장점을 활용하는 디자인
- 하지만 이것을 남용하고 복잡한 기능을 단순한 디자인에 껴 맞추려는 위험도 있음

### 소프트웨어의 독립성(orthogonality)

직교(orthogonality)란 수학적으로는 두 요소가 독립적이라는 것을 의미한다.  
두 벡터가 직교하면 스칼라 곱이 0이 되는데 그들이 전혀 관련이 없다는 것을 의미한다.  
이들 중 하나가 변화해도 다른 하나에는 전혀 영향을 미치지 않다는 것!  
이것이 소프트웨어에서 염두에 두어야 하는 방법이라고 한다.

모듈, 클래스 또는 함수(지겹도록 나오지만...)를 변경하면 수정한 컴포넌트가 외부 세계에 영향을 미치지 않아야 한다.  
항상 가능하지만 않지만 불가능하다 해도 가능한 한 영향을 **최소화**하려고 시도해야 한다.

1. 관심사의 분리
2. 응집력
3. 컴포넌트의 격리  
   위 3개가 디자인 원칙으로 살펴본 것이다.

소프트웨어 런타임 구조 측면에서 직교성은 **변경 또는 부작용을 내부 문제로 만드는 것**이다.  
어떤 객체의 메서드를 호출하는 것은 다른 관련 없는 객체의 내부 상태를 변경해서는 안된다는 것이다.

믹스인 클래스 예제에서 tokenizer 객체를 만들었는데, **iter** 메서드가 새로운 제너레이터를 반환한다는 것은 3개의 기본 클래스, 믹스인 클래스, 구체 클래스 모두가 **독립적**일 가능성이 높다는 것을 의미한다.  
예를 들어 리스트를 반환하는 경우 이것은 나머지 클래스에 종속성이 생기게 하는데,  
리스트를 다른 것으로 변경하는 경우 다른 코드를 업데이트하기 때문이다.  
이는 클래스가 의도와 다르게 독립적이지 않다는 것의 예시다.

파이썬에서는 함수 역시 일반 객체일 뿐이므로 파라미터로 전달할 수 있다.  
독립성을 얻기 위해 이 기능을 활용할 수 있다.

```
# 세금과 할인율을 고려하여 가격을 계산하는 함수 및 최종 계산된 값을 포매팅하고 싶을 시
def calculate_price(base_price: float, tax: float, discount: float) -> float
    return (base_price * (1 + tax)) * (1 - discount)

def show_price(price: float) -> str:
    return "$ {0:,.2f}".format(price)

def str_final_price(
    base_price: float, tax: float, discount: float, fmt_function=str) -> str:
    return fmt_function(calculate_price(base_price, tax, discount))
```

위쪽의 두 개의 함수는 독립성을 갖는다.  
하나는 가격을 계산하는 함수이고,  
다른 하나는 가격을 어떻게 표현할지에 대한 함수이다.  
만약 하나를 변경해도 다른 하나는 변경되지 않으며,  
마지막 함수는 아무것도 전달하지 않으면 문자열 변환을 기본 표현 함수로 사용하고 사용자 정의 함수 전달시 해당 함수를 사용해 포맷한다.  
어느 함수를 변경해도 나머지 함수가 그대로라는 것을 알면 편하게 어느 하나를 변경할 수 있다.

```
str_final_price(10, 0.2, 0.5)
# '6.0'

str_final_price(1000, 0.2, 0.1, fmt_function=show_price)
# '$ 1,080.00'
```

코드의 두 부분이 독립적이라는 것은 다른 부분에 영향을 주지 않고 변경할 수 있다는 것을 뜻한다.  
이는 다시 말하면 **변경된 부분의 단위 테스트가 나머지 단위 테스트와도 독립적**이라는 것을 의미한다.  
두 개의 테스트가 통과하면 전체 회귀 테스트를 하지 않고도 앱에 문제가 없다고 어느 정도 확신이 가능하다.

넓게는 독립성을 기능면에서 생각할 수 있다.  
앱의 두가지 기능이 완전히 독립적이라면 다른 코드를 손상시킬 것에 대한 염려가 없으므로 간단한 테스트 후 배포 가능하다.

예를 들어 프로젝트에 새로운 인증 메커니즘인 oauth2가 필요한데, 동시에 다른 팀도 새로운 보고서 기능을 작성 중이라고 가정하자.  
독립성을 가진다면 서로 기능에 영향을 미치지 않기에 이 중에 어떤것이 먼저 머지되든 상관없이 영향을 미치지 않아야 한다.

---

### 코드 구조

코드를 구조화하는 방법은

1. 팀의 작업 효율성
2. 유지보수성  
   에 영향을 미친다.

특히 여러 정의 즉 여러 클래스, 함수, 상수가 들어있는 큰 파일을 만드는 것은 좋지 않다고 한다.  
극단적으로 **하나의 파일에 하나의 정의만 유지하라는 의미**는 아니지만, 좋은 코드라면 유사한 컴포넌트끼리 정리하여 구조화해야 한다.

파이썬의 경우 대용량 파일을 작은 파일로 나누는 것이 어려운 작업이 아니기에,  
만약 코드의 여러 부분이 해당 파일의 정의에 종속되어 있어도 전체적인 호환성을 유지하며 패키지로 나눌 수 있다.

해결 방법은 **init**.py 파일을 가진 새 디렉토리를 만드는 것이라고 한다.  
이 파일과 함께 특정 정의를 포함하는 여러 파일을 생성하는데 이때는 각각의 기준에 맞춰 보다 **적은 클래스와 함수**를 갖게 된다.  
이후에 **init**.py 파일에 다른 파일에 있던 모든 정의를 가져옴으로서 호환성도 보장할 수 있다.  
또한 이러한 정의는 모듈의 **all** 변수에 익스포트가 가능하도록 표시할수도 있다고 한다.

이거의 장점은 이와 같다.

1. 각 파일을 탐색하고 검색이 쉽다
2. 모듈을 임포트할때 구문을 분석하고 메모리에 로드할 객체가 줄어든다
3. 의존성이 줄었기 때문에 더 적은 모듈만 가져오면 된다
4. 프로젝트를 위한 컨벤션을 갖는데 도움이 된다  
   4번의 경우 예를 들어 모든 파일에서 상수를 정의하는 대신 프로젝트에서 사용할 상수 값을 저장할 특정한 파일을 만들고 다음과 같이 임포트하면 된다.

```
from myproject.constants imporrt CONNECTION_TIMEOUT
```

이와 같이 정보를 중앙화하면 코드 재사용이 쉬워지고 실수로 인한 중복을 피할 수 있다.