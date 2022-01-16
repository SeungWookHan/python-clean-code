### 파이썬의 데코레이터
- PEP-318에서 소개됨

```
def original(...):
  ...
  original = modifier(original)
```  
이러한 방식의 효율성을 위해 새로운 구문을 추가  
```
@modifier
def original(...):
  ...
```  
#### 데코레이터란?
- 데코레이터 @ 이후에 나오는 것을 데코레이터의 첫 번째 파라미터로 하여 데코레이터의 결과 값을 반환하게 하는 Syntax Sugar(동일한 기능이지만 타이핑의 수고를 덜어주기 위해 다른 표현으로 코딩할 수 있게 하는 기능)
- 위의 예제에서 modifier는 decorator, original 함수를 decorated 또는 wrapped 객체라고 함