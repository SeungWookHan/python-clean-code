"""
파이썬의 예외와 관련된 몇가지 권장 사항

올바른 수준의 추상화 단계에서 예외 처리
- 예외는 오직 한 가지 일을 하는 함수의 한 부분이어야 한다.  
- 함수가 처리하는 예외는 캡슐화된 로직과 일치해야 한다.  
"""
class DataTransport:
    """다른 레벨에서 예외를 처리하는 객체의 예"""
    
    retry_threshold: int = 5
    retry_n_time: int = 3

    def __init__(self, connector) -> None:
        self._connector = connector
        self.connection = None
    
    def deliver_event(self, event):
        try:
            self.connect()
            data = event.decode()
            self.send(data)
        except ConnectionError as e:
            logger.info("연결 실패: %s", e)
            raise
        except ValueError as e:
            logger.error("%r 잘못된 데이터 포함: %s", event, e)
            raise
    
    def connect(self):
        for _ in range(self.retry_n_time):
            try:
                self.connection = self._connector.connect()
            except ConnectionError as e:
                logger.info(
                    "%s: 새로운 연결 시도 %is",
                    e,
                    self.retry_threshold,
                )
                time.sleep(self.retry_threshold)
            else:
                return self.connection
        raise ConnectionError(
            f"{self.retry_n_time} 번째 재시도 연결 실패"
        )

    def send(self, data):
        return self.connection.send(data)

"""
위 예제에서 deliver_event 메서드가 예외를 처리하는 방법을 분석  
ValueError와 ConnectionError는 별로 관계가 없다.
이렇게 매우 다른 유형의 오류를 살펴봄으로써 책임 분산에 대한 아이디어를 얻을 수 있다고 한다.

ConnectionError는 connect 메서드 내엣 처리되어야 한다.
이 메서드가 재시도를 지원하는 경우 이 안에서 처리를 할수 있다.

반대로 ValueError는 event의 decode에 속한 에러이다.

deliver_event에서는 예외를 catch할 필요가 없다.
따라서 deliver_event 메서드는 다른 메서드나 함수로 분리해야만 한다.
연결 관리는 작은 함수로 충분하고 이는 연결을 맺고, 발생 가능한 예외를 처리하고 로깅을 담당한다.
"""
    def connect_with_retry(connector, retry_n_times, retry_threshold=5):
        """connector와 연결을 맺는다. <retry_n_times> 재시도.
        연결에 성공하면 connection 객체 반환
        재시도까지 모두 실패하면 ConnectionError 발생

        :param connector: '.connect()' 메서드를 가진 객체
        :param retry_n_times int: ''connector.connect()''를 호출 시도하는 횟수
        :param retry_threshold int: 재시도 사이의 간격
        """

        for _ in range(retry_n_times):
            try:
                return connector.connect()
            except ConnectionError as e:
                logger.info(
                    "%s: 새로운 연결 시도 %is", e, retry_threshold
                )
                time.sleep(retry_threshold)
        
        exc = ConnectionError(f"{retry_n_times} 번째 재시도 연결 실패")
        logger.exception(exc)
        raise exc

    """
    이를 원래 deliver_event 메서드에서 호출되게 함
    """

class DataTransport:
    """추상화 수준에 따른 예이 분리를 한 객체의 예제"""
    
    retry_threshold: int = 5
    retry_n_time: int = 3

    def __init__(self, connector) -> None:
        self._connector = connector
        self.connection = None

    def deliver_event(self, event):
        self.connection = connect_with_retry(
            self._connector, self.retry_n_time, self.retry_threshold
        )
        self.send(event)
    def send(self, event):
        try:
            return self.connection.send(event.decode())
        except ValueError as e:
            logger.error("%r 잘못된 데이터 포함: %s", event, e)
            raise