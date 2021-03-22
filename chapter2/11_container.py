"""
컨테이너 객체

컨테이너는 __contains__ 메서드를 구현한 객체로 이 메서드는 일반적으로 Boolean 값을 반환한다.
이 메서드는 파이썬에서 in 키워드가 발견될 떄 호출된다.

예) element in container
    continer.__contains__(element)
위 두개는 동일한 의미이다.

이 메서드를 잘 사용하면 매우 가독성이 높고 파이썬스럽게 코드를 짤 수 있다고 한다.

저자는 여기서 "2차원 게임 지도에서 특정 위치 표시"에 대한 예를 들었는데, 다음과 같은 경우다
"""
def mark_coordinate(grid, coord):
    if 0 <= coord.x < grid.width and 0 <= coord.y < grid.height:
        grid[coord] = MARKED
"""
위 코드의 if문을 보면 의도가 무엇인지 이해하기 어렵고 역시 직관적이지 않기까지 하다.
도한 매번 경계선을 검사하기 위해 if문을 중복적으로 호출해야 한다.

1. 지도에서 자체적으로 grid라 부르는 영역 판단
2. 이 일을 더 작은 객체에 위임(응집력 향상)
으로 구현하면 어떻게 될까?
"""

class Boundaries:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height

    def __contains__(self, coord):
        x, y = coord
        return 0 <= x < self.width and 0 <= y < self.height

class Grid:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.limits = Boundaries(width, height)

    def __contains__(self, coord):
        return coord in self.limits

"""
위 코드만으로 훨씬 효과적이 구현이다.
1. 구성이 간단
2. 위임을 통해 문제 해결
3. 두 객체 모두 최소한의 논리 사용
4. 메서드는 짧고 응집력이 있음

또한 외부에서 사용할 때도 이점이 있는데 다음 코드를 보자.
"""
def mark_coordinate(grid, coord):
    if coord in grid:
        grid[coord] = MARKED