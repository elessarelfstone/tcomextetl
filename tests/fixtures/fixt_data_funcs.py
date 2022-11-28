import pytest


@pytest.fixture()
def fixture_save_csvrows():

    data = [
        [
            (1, '2022-10-30 23:55:45', 56.7, 'This is "first string'),
            (2, '"2022-11-05 12:35:00"', 102.3, 'This is \r\n broken string'),
            (3, '2022-12-31 23:59:59', 1533.56, 'This is another\r broken string'),
            (4, '2022-01-01 01:01:01', 3.14, 'This is just another \n broken string'),
            (5, '2022-03-22 13:00:00', 10000000.0, 'This is string ; with delimiter'),
            (6, '2022-07-08 02:00:00', 0.34, '"This is quoted string" ; with delimiter"')
        ],
        [
            ('1', '2022-10-30 23:55:45', '56.7', 'This is "first string'),
            ('2', '2022-11-05 12:35:00', '102.3', 'This is  broken string'),
            ('3', '2022-12-31 23:59:59', '1533.56', 'This is another broken string'),
            ('4', '2022-01-01 01:01:01', '3.14', 'This is just another  broken string'),
            ('5', '2022-03-22 13:00:00', '10000000.0', 'This is string ; with delimiter'),
            ('6', '2022-07-08 02:00:00', '0.34', "This is quoted string' ; with delimiter")
        ]
    ]

    return data
