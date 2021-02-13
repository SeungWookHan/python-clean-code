"""
docstring은 소스 코드에 포함된 문서.
이와 같이 큰 따옴표 3개와 3개 사이에 작성.
코드에 주석(comment)을 다는 것은 나쁜 습관이라고 저자는 말한다.
첫째, 주석은 코드로 아이디어를 제대로 표현하지 못했음을 나타냄
둘째, 오해의 소지가 있음, 코드가 어떻게 동작하는지 주석을 확인한 후 실제로 동작하는 것의 다른 점을 파악하는 것?
셋째, 사람들은 코드 변경할 때 주석 업데이트를 깜박하는 경우가 있음

docstring은 주석과는 달리 코드의 컴포넌트(모듈, 클래스, 메서드나 함수)에 대한 문서화.
파이썬의 경우 동적 타이핑며 파라미터의 타입을 체크하거나 강요하지 않기에 가능한 많은 docstring 작성이 권장됨.
"""
print(dict.__doc__)
"""
dict() -> new empty dictionary
dict(mapping) -> new dictionary initialized from a mapping object's
    (key, value) pairs
dict(iterable) -> new dictionary initialized as if via:
    d = {}
    for k, v in iterable:
        d[k] = v
dict(**kwargs) -> new dictionary initialized with the name=value pairs
    in the keyword argument list.  For example:  dict(one=1, two=2)
"""

"""
docstring 내용을 문서화 시켜주는 툴: Sphinx(스핑크스)
"""