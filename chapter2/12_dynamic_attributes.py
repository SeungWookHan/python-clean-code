"""
객체의 동적인 속성

__getattr__ 매직 메서드를 사용해 객체에서 속성을 얻는 방법을 제어할 수 있다.
<object>.<attribute>를 호출하면 파이썬은 객체의 사전에서 <attribute>를 찾아서 __getattribute__를 호출한다.

객체에 찾고 있는 속성이 없는 경우 attribute의 이름을 파라미터로 전달,
__getattr__ 이라는 추가(extra) 메서드가 호출된다.
이 값을 사용하여 반환 값을 제어 및 새로우 속성을 만들 수 있다.
"""

class DynamicAttributes:
    def __init__(self, attribute) -> None:
        self.attribute = attribute
    
    def __getattr__(self, attr):
        if attr.startswith("fallback_"):
            name = attr.replace("fallback_", "")
            return f"[fallback resolved] {name}"
        raise AttributeError(f"{self.__class__.__name__}에는 {attr} 속성이 없음.")

dyn = DynamicAttributes('value')
print(dyn.attribute) # value

print(dyn.fallback_test) # [fallback resolved] test

dyn.__dict__["fallback_new"] = "new value"
print(dyn.fallback_new) # new value

print(getattr(dyn, "something", "default")) #default

"""
첫번쨰 호출: 객체에 있는 속성을 요청하고 그 결과 값 반환
두번째 호출: 객체에 없는 fallback_test라는 메서드를 호출하기에 __getattr__이 호출되어 값을 변환
세번째 호출: fallback_new 라는 새로운 속성이 생성된다.
            이는 dyn.fallback_new = "new value"와 동일
            이때 __getattr__ 로직이 적용되지 않는데, 그 이유는 단순히 메서드가 호출되지 않았기 때문이다.
마지막 호출: 

__getattr__에서 값을 검색할 수 없는 경우 AttributeError 예외가 발생하는 것에 유의해야 한다.
이는 예외 메시지를 포함해 일관성 유지 및 내장 getattr() 함수에서도 필요한 부분이다.
이 예외가 없으면 기본 값을 반환한다고 한다.

그렇기에 __getattr__ 같은 동적인 메소드를 구현할때는 AttributeError를 발생시켜야 한다.
"""