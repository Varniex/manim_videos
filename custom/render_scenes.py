from manimlib.config import get_custom_config
from screeninfo import get_monitors


def render_scene(scene_name, **kwargs):
    """
    This is used to render scene to pyglet window from a script file.
    :param scene_name: Scene Class
           kwargs: Scene kwargs
    """

    # from 3b1b's manimgl config.py file
    custom_config = get_custom_config()
    monitors = get_monitors()
    mon_index = custom_config["window_monitor"]
    monitor = monitors[min(mon_index, len(monitors) - 1)]
    window_width = monitor.width // 2
    window_height = window_width * 9 // 16
    default_kwargs = {
        "window_config": {
            "size": (window_width, window_height)
        }
    }

    default_kwargs.update(**kwargs)
    scene_name(**default_kwargs).run()
