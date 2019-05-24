from .phantom_config import PhantomConfig


def read_phantom(filename):
    return PhantomConfig(filename=filename, filetype='phantom')


def read_json(filename):
    return PhantomConfig(filename=filename, filetype='json')


__all__ = ['PhantomConfig', 'read_phantom', 'read_json']
