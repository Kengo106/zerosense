#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zerosence.settings')
    name = os.environ.get('DATABASE_NAME')
    user = os.environ.get('DATABASE_USER')
    password = os.environ.get('DATABASE_PASSWORD')
    host = os.environ.get('DATABASE_HOST')
    port = os.environ.get('DATABASE_PORT')

    # 環境変数の内容を出力して確認
    print('DATABASE_NAME:', name)
    print('DATABASE_USER:', user)
    print('DATABASE_PASSWORD:', password)
    print('DATABASE_HOST:', host)
    print('DATABASE_PORT:', port)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
