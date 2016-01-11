

def includeme(config):
    if 'dbsession' not in config.registry.settings:
        config.include('pyramid_tm')
    config.include('pyramid_services')
    config.include('pyramid_exclog')
