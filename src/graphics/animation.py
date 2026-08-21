
class Animation:
    """A sequence of frames shown one after another. Build one with
    AssetManager.make_animation(), or from the frames returned by
    AssetManager.load_spritesheet().
    """

    def __init__(self, frames: list, frame_duration: float = 0.1, loop: bool = True) -> None:
        if not frames:
            raise ValueError("Animation needs at least one frame")

        self.frames = frames
        self.frame_duration = frame_duration
        self.loop = loop
        self.current_frame = 0
        self._timer = 0.0
        self.finished = False

    def update(self, dt: float) -> None:
        if self.finished:
            return

        self._timer += dt
        while self._timer >= self.frame_duration:
            self._timer -= self.frame_duration
            self.current_frame += 1
            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.finished = True
                    break

    def reset(self) -> None:
        self.current_frame = 0
        self._timer = 0.0
        self.finished = False

    def get_current_frame(self) -> "pygame.Surface":
        return self.frames[self.current_frame]