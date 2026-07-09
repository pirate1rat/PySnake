from models.game_api import GameContext, Tile, Snake, vec2, register
from collections import deque
from threading import Lock
from PyQt6.QtCore import Qt, QObject, QEvent
from PyQt6.QtWidgets import QApplication

@register
class Human(QObject):
    def __init__(self, ctx: GameContext):
        super().__init__()
        self._queue: deque[vec2] = deque(maxlen=2)
        self._last_move: vec2 = vec2(0, -1)
        self._lock = Lock()
        QApplication.instance().installEventFilter(self)

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Type.KeyPress:
            direction = self._key_to_vec(event.key())
            if direction is not None:
                with self._lock:
                    last = self._queue[-1] if self._queue else self._last_move
                    if direction != vec2(-last.x, -last.y):
                        self._queue.append(direction)
                return True
        return False

    def get_move(self, ctx: GameContext) -> vec2:
        with self._lock:
            if self._queue:
                self._last_move = self._queue.popleft()
        return self._last_move

    def __del__(self):
        app = QApplication.instance()
        if app:
            app.removeEventFilter(self)

    @staticmethod
    def _key_to_vec(key: Qt.Key) -> vec2 | None:
        return {
            Qt.Key.Key_Up:   vec2(0, -1),
            Qt.Key.Key_W:    vec2(0, -1),
            Qt.Key.Key_Down: vec2(0,  1),
            Qt.Key.Key_S:    vec2(0,  1),
            Qt.Key.Key_Left: vec2(-1, 0),
            Qt.Key.Key_A:    vec2(-1, 0),
            Qt.Key.Key_Right: vec2(1,  0),
            Qt.Key.Key_D:    vec2(1,  0),
        }.get(key)