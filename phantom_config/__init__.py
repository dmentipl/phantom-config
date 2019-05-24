from .phantom_config import PhantomConfig


def read(filename):
    return PhantomConfig(filename=filename, filetype='phantom')


def read_json(filename):
    return PhantomConfig(filename=filename, filetype='json')


__all__ = ['PhantomConfig', 'read', 'read_json']
