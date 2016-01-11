from pyramid.config import Configurator


def get_config(global_config, **settings):
    """
    Control configurations state
    """
    merged_settings = {}
    merged_settings.update(global_config)
    merged_settings.update(settings)
    config = Configurator(settings=merged_settings)
    config.include('homework.api.settings.extension')
    config.include('homework.api.settings.logger')
    config.include('homework.api.settings.service')
    config.include('homework.api.routes')
    config.include('homework.api.settings.adapter')
    config.scan('homework.api')
    return config
