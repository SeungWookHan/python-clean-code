### Traceback 노출 금지
이는 보안을 위한 고려 사항인데, 예외를 처리할 때 오류가 너무 중요하다면 전파해도 된다.  
또한 특정 시나리오에서 검토된 내용이거나  
견고함 보다 정확성이 중요한 상황이라면 프로그램을 종료하게 할 수도 있다.  

문제를 효율적으로 해결할 수 있도록  
1. traceback 정보
2. 메시지 및 기타 수집 가능한 정보
를 로그로 남기는 것이 중요하다고 한다.  

하지만 절대로 이러한 세부사항은 사용자에게 보여서는 안된다고 한다.  

파이썬에서 traceback은 매우 유용하고 많은 디버깅 정보를 포함하기에,  
악의적인 사용자에게도 매우 유용한 정보여서 중요 정보나 지적 재산의 유출이 발생할 수 있다고 한다.  

사용자에게는 문제를 알리깅 위해
1. 무엇이 잘못되었다
2. 페이지를 찾을 수 없다
등의 일반적 메시지를 사용해야 한다고 한다.(웹에서 http 오류 발생시 사용하는 기법)  
---
### 비어있는 except 블록 지양
파이선의 안티패턴 중에서도 가장 악마 같은 패턴(REAL 01)이라고 한다.  
일부 오류에 대하여 방어적인 프로그래밍은 좋지만 너무 방어적인 것은 더 심각한 문제로 이어질 수 있다.  
그 중 너무 방어적이어서 아무것도 하지 않은 채로 조용히 지나쳐버리는 것은 가장 안좋은 예라고 한다.  
```
try:
    process_data()
except:
    pass
```
위 코드의 문제는 실패해야할 때 조차도 실패하지 않는다는 것이다.  
에러는 결코 조용히 전달되어서는 안된다는 파이썬의 철학(The Zen of Python)에 위배되며 파이썬스럽지 않다고 한다.  

이러한 코드는 로직에 수정해야 할 에러가 있는지 알수 없기에 유지보수를 더 어렵게 만든다.  
여기서 저자는 두가지 대안을 제시한다.  
- 보다 구체적인 예외 사용(단순 Exception 같이 광범위한 예외 말고)
- except 블록에서 실제 오류 처리를 한다  

가장 좋은 방법은 두가지 동시에 적용하는 것이다.  
Attribute같은 구체적은 예외를 사용하면 사용자는 무엇을 기대하는지 알게 되기에 프로그램을 유지보수하기 쉽다.  
예외를 자체적으로 처리하는 것은 여러가지를 의미할 수 있다는데,  
예로 예외사항을 로깅할 수 있다는 점이다.
(발생한 일의 컨텍스트를 제공하려면 logger.exception, logger.error 사용)  

다른 방법으로는 기본 값을 반환하는 것인데,  
이전에 말했던 값 대체의 `오류를 발견하기 전`이 아닌 오직 오류를 발견한 뒤에만 사용하는 값이다.  
(그렇지 않은 경우 다른 예외 발생시켜야 함...?)  

---
### 원본 예외 포함
오류 처리 과정에서 다른 오류를 발생시키고 메시지를 변경할 수 있다.  
이 경우에는 원래 예외를 포함하는 것이 좋다.  

파이썬3(PEP-3134)에서는  
```
raise <e> from <originam exception>
```
구문을 사용하면 된다고 한다.  

이 경우 원본의 traceback이 새로운 exception의 포함되고 원본 예외는 __cause__ 속성으로 들어간다.  
```
class InternalDataError(Exception):
    """업무 도메인 데이터 예외처리"""

    def process(data_dictionary, record_id):
        try:
            return data_dictionary[record_id]
        except KeyError as e:
            raise InternalDataError("Record not present") from e
```

### 파이썬 assertion 사용하기
어설션 문에 사용된 표현식은 불가능한 조건을 의미한다.
(절대 일어나지 않아야 하는 상황에서 사용)  
이 상태가 된다는 건 소프트웨어에 결함이 있음을 의미한다.  
에러 핸들링과 다르게 여기서는 프로그램을 계속하거나 중단해야 할 가능성이 있는데...??  
이런 오류가 발생하면 프로그램을 중지해야 한다.(결함이 있기에..)  
따라서 해당 결함을 수정하여 새 버전의 배포를 하는 것 외에는 방법이 없다고 한다.  

어설션을 다시 말하면
`잘못된 시나리오에 도달할 경우 프로그램이 더 큰 피해를 입지 않도록 하는것`
이라고 한다.  
때로는 계속하기보다는 프로그램 중단!!!!   

그렇기에 어설션을 비즈니스로직과 섞어 쓰거나,  
소프트웨어 제어 흐름 메커니즘으로 사용해서는 안된다고 한다.  
```
try:
    assert condition.holds(), "조건에 맞지 않음."
except AssertionError:
    alternative_procedure()
```
위에 예제가 좋지 않은 예라고 한다.  
(하지만 나는 뭐가 뭐지 잘 모르겠다아아아아)  

어설션에 실패하면 반드시 프로그램을 종료시켜야 하며  
어설션 문장에 설명이 포함된 오류 메시지를 작성하여 나중에 디버깅 및 수정에 용이하게 해야 한다.  

앞의 예제는 AssertionError를 처리하는 것 외에도 어셜션이 함수 문장이기 때문에 나쁘다고 한다.  
함수 호출은 부작용을 가질수 있으며 항상 반복 가능하지 않기 때문이라고 한다...?   
디버거를 사용해 해당 라인에서 중지하기에 오류 결과를 편리하게 볼 수 없고, 다시 함수를 호출한다 해도  
잘못된 값이었는지 알 방법이 없어서 더더욱 나쁜 코드라고 한다.  
보다 다은 방법은 아래와 같다.  
```
result = conditon.holds()
assert result > 0, "에러 {0}".format(result)
```