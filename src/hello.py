#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
Main application.
"""


def main():
    """
    Main
    """
    from app.acclaim.badges.GetAll import GetAll
    get_all_badges = GetAll('ibm')
    get_all_badges._max_workers = 256000
    if get_all_badges.execute():
        badges = get_all_badges.get_badges_id
        print('# Badges:', len(badges))
        # print(badges)
        # print('\n'.join(badges))


if __name__ == '__main__':
    main()
