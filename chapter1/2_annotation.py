"""
변수의 예상 타입이나 변수를 이해하는데 도움이 되는 형태의 메타데이터를 지정하여
코드 사용자에세 함수 인자로 어떤 값이 와야하는지 등에 대한 힌트를 주는 것.
이는 추후 공부할 타입 힌팅(type hinting)을 활성화 함.
"""


class Point:
    lat: float
    long: float

    def __init__(self, lat, long):
        self.lat = lat
        self.long = long


def locate(latitude: float, longitutd: float) -> Point:
    """맵에서 좌표에 해당하는 객체를 검색"""


# 하지만 파이썬이 타입을 검사하거나 강제하지는 앟음.


print(locate.__annotations__)
# {'latitude': <class 'float'>, 'longitutd': <class 'float'>, 'return': <class '__main__.Point'>}
# 이를 통해 문서 생성, 유효성 검증, 타입 체크가 가능

"""
PEP-484은 타입 힌팅의 기본 원리를 정의한 것으로
"파이썬은 여전히 동적인 타입의 언어로 남을 것이다. 타입 힌트를 필수로 하자거나 심지어 관습으로 하자는 것은 전혀 아니다"
타입 힌팅은 인터프리터와 독립된 도구를 사용하여 코드 전체에 올바를 타입이 사용되었는지, 안되었는지 이에 대한
힌트를 주는 것이다. 이는 도구인 Mypy에 대해서는 추후 다룰 예정.

정리하자면 코드의 시맨틱이 보다 의미 있는 개념을 갖게 되면 코드를 이해하고 예측하기 쉽다는 의미
"""

print(Point.__annotations__)
# {'lat': <class 'float'>, 'long': <class 'float'>}

"""
docstring을 annotation이 대체하는 것으로 생각할 수 있는데,
이 둘은 보완적인 개념이다.
docstring의 일부를 이동시킬 수 있겠지만 이는 보다 나은 문서화를 위해 남겨야 한다.
"""


def data_from_response(response: dict) -> dict:
    """response에 문제가 없다면 response의 payload를 반환
    - response의 사전의 예제::
    {
        "status": 200 # <int>
        "timestamp": "....", # 현재 시간의 ISO 포맷 문자열
        "payload": {...} # 반환하려는 사전 데이터
    }
    - 반환 사전 값의 예제::
    {"data": {..}}
    - 발생 가능한 예외:
    - HTTP status가 200이 아닌 경우 ValueError 발생
    """

    if response["status"] != 200:
        raise ValueError
    return {"data": response["payload"]}


# 이러한 문서는 입출력 값을 더 잘 이해하기 위해서 뿐 아닌 단위 테스트에서도 유용하게 사용됨.