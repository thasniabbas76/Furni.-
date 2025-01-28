#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.core.management import execute_from_command_line

def main():
    """Run administrative tasks."""
    settings_module = 'ecom.deployment' if 'WEBSITE_HOSTNAME' in os.environ else 'ecom.settings'
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
